"""
Methos to interact with api

"""
import os
import asyncio
import aiohttp
import json




def get(url, params):
    return asyncio.run(get_async(url, params))

def post(url, content):
    return asyncio.run(post_async(url, content))

def delete(url, record_type, record_id):
    return asyncio.run(delete_async(url, record_type, record_id))






async def get_async(url, params):
    """Given a record_type and id, retrieves record from url and return content as-is
    """
    headers = {'content-type': "application/json"}

    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.get(url, params=params) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - get ', e)
        return False

    if response.status == 200:
        return content
    else:
        print('content', content)
        return False



async def post_async(url, json_content):
    """Given content, post as-is
    """
    headers = {'content-type': "application/json"}
    data = json_content
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.post(url, data=data) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - post ', e)
        return False

    if response.status == 200:
        return content
    else:
        return False




async def delete_async(url, record_type, record_id):
    """Given content, post as-is
    """
    headers = {'content-type': "application/json"}
    params = {'@type': record_type, '@id': record_id}
    data = json.dumps(params)
    try:
        async with aiohttp.ClientSession(headers=headers) as session:
            async with session.delete(url, data=data) as response:
                content = await response.text()
    except Exception as e:
        print('Error kraken_api - delete ', e)
        return False

    if response.status == 200:
        return True
    else:
        return False



