import asyncio
import aiohttp
import json
from kraken_thing.kraken_actions.action_methods import action_api, action_status

"""
Runs an action on a given record
"""


def run(action, record):
    """Dispatch for the actions
    """

    result = False
    
    if action == 'scrape':
        url = 'https://scraper.krknapi.com'
        result = action_api.action_api(record, url)

    return result



def get(record):
    """Retrieves available actions for record
    """
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    url = record.get('url', None)
    email = record.get('email', None)
    address = record.get('address', None)

    actions = []
    action = {"@type": "action", "target": f"/{record_type}/{record_id}/action/scrape"}
    actions.append(action)
    
    return actions

def run_api(action, record):
    """
    """



async def run_api_async(action, record):
    """
    """

    object = action.get('object', None)

    instrument = action.get('instrument', {})
    url = instrument.get('url', None)
    
    if not object or not instrument or not url:
        return False


    headers = {'content-type': "application/json"}
    data = json.dumps(object, default=str)
    
    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.get(url, data=data) as response:
            html = await response.text()
            result = await response.json()
            status =  response.status

    
    
    print('task finished')

    return result