#!/usr/bin/env python3
'''
    Main entry point for the application
'''

import os
import aioredis
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from loguru import logger
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import RedirectResponse
from config import settings
from openapi import init_openapi
from routers import router

# Create the FastAPI app
app = FastAPI()

# Add CORS middleware
origins = ['http://localhost:3000']

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

# Connect to the database
@app.on_event('startup')
async def startup_event():
    '''
    Connect to Mongodb and Redis
    '''

    try:
        app.mongodb_client = AsyncIOMotorClient(settings.MONGODB_URL)
        app.mongodb = app.mongodb_client[settings.MONGODB_NAME]
    except Exception as e:
        logger.error(f'Error connecting to Mongodb: {e}')
    else:
        logger.info('Connected to Mongodb')

    try:
        redis = await aioredis.create_redis_pool(settings.REDIS_URL)
        app.redis = redis
    except Exception as e:
        logger.error(f'Error connecting to Redis: {e}')
    else:
        logger.info('Connected to Redis')

# Disconnect from the database
@app.on_event('shutdown')
async def shutdown_event():
    '''
    Disconnect from Mongodb and Redis
    '''
    logger.info('Shutting down server')

    try:
        app.mongodb_client.close()
    except Exception as e:
        logger.error(f'Error disconnecting from Mongodb: {e}')
    else:
        logger.info('Disconnected from Mongodb')

    # try:
    #     app.redis.close()
    #     await app.redis.wait_closed()
    # except Exception as e:
    #     logger.error(f'Error disconnecting from Redis: {e}')
    # else:
    #     logger.info('Disconnected from Redis')
        
# Root redirect
@app.get('/', include_in_schema=False)
async def get_root():
    '''
    Redirect to the docs
    '''
    if (root_url := os.environ.get('ROOT_URL')) is None:
        return {
            'api_docs': {
                'openapi': f'{root_url}/docs',
                'redoc': f'{root_url}/redoc'
            }
        }
    
    response = RedirectResponse(url=f'{root_url}/docs')
    return response

# Add the routers
app.include_router(router, tags=['To-Do'], prefix='/api/v1/task')

init_openapi(app)

if __name__ == '__main__':
    uvicorn.run(
        'main:app',
        host=settings.HOST,
        reload = settings.DEBUG_MODE,
        port = settings.PORT,
    )