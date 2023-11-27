#
# Copyright (c) 2015-2021 Thierry Florac <tflorac AT ulthar.net>
# All Rights Reserved.
#
# This software is subject to the provisions of the Zope Public License,
# Version 2.1 (ZPL).  A copy of the ZPL should accompany this distribution.
# THIS SOFTWARE IS PROVIDED "AS IS" AND ANY AND ALL EXPRESS OR IMPLIED
# WARRANTIES ARE DISCLAIMED, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED
# WARRANTIES OF TITLE, MERCHANTABILITY, AGAINST INFRINGEMENT, AND FITNESS
# FOR A PARTICULAR PURPOSE.
#

"""PyAMS_chat_ws.server module

This module defines main chat server application.
"""

# pylint: disable=logging-fstring-interpolation

import asyncio
import json

import aioredis
import async_timeout
import httpx
from starlette.applications import Starlette
from starlette.routing import Route, WebSocketRoute
from starlette.websockets import WebSocket

from pyams_chat_ws import LOGGER
from pyams_chat_ws.chat import WSChatEndpoint
from pyams_chat_ws.monitor import MonitorEndpoint


__docformat__ = 'restructuredtext'


class ChatApp(Starlette):
    """Main chat application"""

    redis = None

    sessions = {}
    sessions_lock = asyncio.Lock()

    @classmethod
    async def create(cls, config):
        """Application factory"""
        app = cls(config)
        app.redis = await aioredis.from_url(config.get('redis_host'),
                                            encoding='utf-8',
                                            decode_responses=True)
        asyncio.create_task(app.start_chat())
        return app

    def __init__(self, config):
        super().__init__(routes=[
            Route(config.get('monitor_endpoint', '/monitor'),
                  MonitorEndpoint),
            WebSocketRoute(config.get('ws_endpoint', "/ws/chat"),
                           WSChatEndpoint)
        ])
        self.config = config

    async def start_chat(self):
        """Chat application starter"""
        psub = self.redis.pubsub()
        await psub.subscribe(self.config.get('channel_name', "chat:main"))
        LOGGER.debug('Redis channel subscription enabled')
        async with psub as p:  # pylint: disable=invalid-name
            while True:
                try:
                    async with async_timeout.timeout(1):
                        msg = await p.get_message(ignore_subscribe_messages=True)
                        if msg is not None:
                            LOGGER.debug(f'Loaded Redis message: {msg!r}')
                            await self.dispatch(msg)
                        await asyncio.sleep(0.01)
                except asyncio.TimeoutError:
                    pass

    async def add_session(self, ws: WebSocket):  # pylint: disable=invalid-name
        """Add session from given websocket"""
        context_url = self.config.get('context_url')
        LOGGER.debug(f'>>> Adding new websocket session...')
        LOGGER.debug(f'  > client: {ws.client}')
        LOGGER.debug(f'  > context URL: {context_url}')
        token = ws.user.access_token
        LOGGER.debug(f'  > token: {token}')
        async with httpx.AsyncClient(verify=self.config.get('ssl_verify', True)) as client:
            result = await client.get(context_url, headers={
                'Authorization': f'Bearer {token}',
                'Content-type': 'application/json'
            })
            LOGGER.debug(f'  > got context: {result}')
            if result.status_code != httpx.codes.OK:
                return None
            context = result.json()
            LOGGER.debug(f'  > context data: {context}')
            async with self.sessions_lock:
                self.sessions[ws.client] = {
                    'ws': ws,
                    'host': ws.headers.get('origin'),
                    'context': context,
                    'principal_id': ws.user.username,
                    'channels': [self.config.get('channel_name', "chat:main")]
                }
                LOGGER.debug(f'>>> users sessions count: {len(self.sessions)}')

    def drop_session(self, ws: WebSocket):  # pylint: disable=invalid-name
        """Drop session from given websocket"""
        LOGGER.debug(f'>>> dropping session for {ws.client}...')
        self.sessions.pop(ws.client, None)

    async def dispatch(self, message):
        """Dispatch received message"""
        LOGGER.debug(">>> dispatching message...")
        if isinstance(message, (str, bytes)):
            try:
                message = json.loads(message)
            except ValueError:
                return
        message = message.get('data')
        if isinstance(message, (str, bytes)):
            try:
                message = json.loads(message)
            except ValueError:
                return
        if message:
            async with self.sessions_lock:
                principals = set(message.pop('target', {}).get('principals', []))
                for session in self.sessions.values():
                    LOGGER.debug(f"  > checking session: {session}")
                    # don't send messages to other hosts
                    if session['host'] != message.get('host'):
                        continue
                    # don't send messages to message emitter
                    if session['principal_id'] == message.get('source', {}).get('id'):
                        continue
                    # filter message targets
                    try:
                        if set(session['context']['principal']['principals']) & principals:
                            LOGGER.debug(f"  > sending message: {message}")
                            await session['ws'].send_json(message)
                    except KeyError:
                        continue
            # update Redis notifications queue
            cache_key = self.config.get('notifications_key')
            if cache_key:
                cache_key = f"{cache_key}::{message.get('host', '--')}"
                cache_length = self.config.get('notifications_length', 50)
                LOGGER.debug(f"   > adding message to Redis queue {cache_key}")
                async with self.redis.pipeline(transaction=True) as pipe:
                    await pipe \
                        .lpush(cache_key, json.dumps(message)) \
                        .ltrim(cache_key, 0, cache_length - 1) \
                        .execute()
