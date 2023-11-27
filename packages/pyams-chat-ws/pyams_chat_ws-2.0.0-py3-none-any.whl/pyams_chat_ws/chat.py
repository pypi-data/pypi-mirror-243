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

"""PyAMS_chat_ws.chat module

This module defines a websocket endpoint used for chat.
"""

# pylint: disable=logging-fstring-interpolation

from starlette.authentication import UnauthenticatedUser
from starlette.endpoints import WebSocketEndpoint
from starlette.websockets import WebSocket

from pyams_chat_ws import LOGGER


__docformat__ = 'restructuredtext'


class WSChatEndpoint(WebSocketEndpoint):
    """Main chat endpoint"""

    encoding = 'text'

    async def on_connect(self, ws: WebSocket):  # pylint: disable=arguments-renamed
        """Websocket connection handler"""
        await ws.accept('accessToken')
        if 'authenticated' in ws.auth.scopes:
            app = self.scope.get('app', None)
            if app is not None:
                LOGGER.debug(f'Adding user session for {ws.user.username}...')
                await app.add_session(ws)
        else:
            await ws.send_json({
                'action': 'logout',
                'status': 'FORBIDDEN'
            })

    async def on_disconnect(self, ws: WebSocket, close_code: int):  # pylint: disable=arguments-renamed
        """Websocket disconnection handler"""
        app = self.scope.get('app', None)
        if app is not None:
            if isinstance(ws.user, UnauthenticatedUser):
                LOGGER.debug(f'Dropping session for unauthenticated user...')
            else:
                LOGGER.debug(f'Dropping user session for {ws.user.username}...')
            app.drop_session(ws)

    async def on_receive(self, ws: WebSocket, data):  # pylint: disable=arguments-renamed
        """Websocket message handler"""
        LOGGER.debug(f'Received message: {data}')
        if data == 'PING':
            await ws.send_text('PONG')
            return
        if 'authenticated' in ws.auth.scopes:
            app = self.scope.get('app', None)
            if app is not None:
                await app.dispatch(data)
