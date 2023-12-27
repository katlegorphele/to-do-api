#!/usr/bin/env python3
'''
    Swagger doc for the API
'''

import os
from loguru import logger
from fastapi.openapi.utils import get_openapi

ROOT_URL = os.environ.get('ROOT_URL')

def init_openapi(app):
    '''
        Initialize the openapi
    '''
    openapi_schema = get_openapi(
        title="To-Do API",
        version=os.environ.get('RELEASE_VERSION', '1.0.0'),
        description="To-Do API",
        routes=app.routes,
    )

    app.openapi_schema = openapi_schema

