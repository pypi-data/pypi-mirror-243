
import uuid

def db_record(base_url, system, table, record_id):
    """Shortcut to create metadata for a system record
    """

    record = {}

    record['observationAbout'] = {
        '@type': 'dataFeedItem',
        '@id': uuid.uuid4(),
        'url': base_url + '/' + system + '/' + table + '/' + record_id, 
        'sameAs': base_url + '/' + system + '/' + table + '/' + record_id
        
        }
    
    record['source'] = {
            '@type': 'softwareApplication',
            '@id': uuid.uuid4(),
            'url': base_url + '/' + system 
        }

    return record
    

def web_api(self, base_url, system, entity, record_id):
    """Shortcut to create a system record
    """

    record = {}
    
    record['observationAbout'] = {
        '@type': 'dataFeedItem',
        '@id': uuid.uuid4(),
        'url': base_url + '/' + system + '/' + entity + '/' + record_id, 
        'sameAs': base_url + '/' + system + '/' + entity + '/' + record_id
    }
    
    record['source'] = {
        '@type': 'webAPI',
        '@id': uuid.uuid4(),
        'url': base_url + '/' + system 
    }
    return record