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

"""PyAMS_chat_ws.auth module

This module provides JWT authentication backend.
"""

# pylint: disable=logging-fstring-interpolation

import httpx
from starlette.authentication import AuthCredentials, AuthenticationBackend, SimpleUser
from starlette.requests import HTTPConnection

from pyams_chat_ws import LOGGER


__docformat__ = 'restructuredtext'


class JWTUser(SimpleUser):
    """JWT authenticated user"""

    def __init__(self, username: str, access_token: str):
        super().__init__(username)
        self.access_token = access_token


class JWTAuthenticationBackend(AuthenticationBackend):
    """JWT authentication backend"""

    def __init__(self, config: dict):
        super().__init__()
        self.config = config

    async def authenticate(self, request: HTTPConnection):  # pylint: disable=arguments-renamed
        """Request authentication"""
        protocol = request.headers.get('sec-websocket-protocol')
        if not protocol:
            LOGGER.debug('No WebSocket security protocol, authentication refused!')
            return None
        proto, token = protocol.split()
        if ',' in proto:
            proto, _ = proto.split(',', 1)
        if not proto.startswith(self.config.get('ws_protocol', 'accessToken')):
            LOGGER.debug('Unknown security protocol, authentication refused!')
            return None
        authority = self.config.get('jwt_authority')
        LOGGER.debug(f'Checking JWT authority {authority}')
        async with httpx.AsyncClient(verify=self.config.get('ssl_verify', True)) as client:
            result = await client.get(authority, headers={
                'Authorization': f'Bearer {token}',
                'Content-type': 'application/json'
            })
            if result.status_code != httpx.codes.OK:
                LOGGER.debug(f'JWT status code: {result.status_code}')
                return None
            username = result.json().get('sub')
            if username:
                LOGGER.debug(f'JWT username: {username}')
                return AuthCredentials(['authenticated']), \
                    JWTUser(username, token)
        LOGGER.debug("Can't get valid credentials from authentication token!")
        return None
