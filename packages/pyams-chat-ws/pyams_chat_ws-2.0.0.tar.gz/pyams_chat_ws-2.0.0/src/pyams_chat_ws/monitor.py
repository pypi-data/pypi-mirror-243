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

"""PyAMS_*** module

"""

__docformat__ = 'restructuredtext'

import sys
try:
    from importlib.metadata import PackageNotFoundError, distribution
except ImportError:
    from importlib_metadata import PackageNotFoundError, distribution

from starlette.endpoints import HTTPEndpoint
from starlette.responses import JSONResponse


versions = [
    f'Python/{sys.version_info.major}.{sys.version_info.minor}'
]
for package in ('websockets', 'Starlette'):
    versions.append(f'{package}/{distribution(package).version}')

try:
    distribution = distribution('pyams-chat-ws')
except PackageNotFoundError:
    distribution = None

versions.append(f'''PyAMS-chat-ws/{distribution.version 
    if distribution is not None else "development"}''')


class MonitorEndpoint(HTTPEndpoint):
    """Application monitoring endpoint"""

    async def get(self, request):
        """Default monitor endpoint"""
        return JSONResponse({
            'status': 'OK',
            'sessions_count': len(self.scope['app'].sessions),
            'server': ' '.join(versions)
        })
