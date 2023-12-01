import requests
from kraken_thing import kraken_thing_methods as kr

#from kraken_thing.kraken_class_things.kraken_class_things import Things

def action_api(record, url):
    """
    """

    headers = {'content-type': 'application/json'}
    data = kr.json.dumps(record)
    
    r = requests.post(url, headers=headers, data=data)

    results = kr.json.loads(r.text)

    #things = Things()
    #things.load(results)
    #things.api_post()

    
    return results