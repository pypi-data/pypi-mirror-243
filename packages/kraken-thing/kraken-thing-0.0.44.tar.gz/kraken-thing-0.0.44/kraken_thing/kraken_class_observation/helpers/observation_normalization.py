
from kraken_schema_org import kraken_schema_org as kraken_schema

import copy



def test_valid(record):
    """Returns tuple of bool with validity of measuredProperty and value
    """

    if not record or not isinstance(record, dict):
        return
        
    norm = normalize(record)

    record_prop = record.get('measuredProperty', None)
    norm_prop = norm.get('measuredProperty', None)
    validProperty = True if record_prop == norm_prop else False

    record_value = record.get('value', None)
    norm_value = norm.get('value', None)
    validValue = True if record_value == norm_value else False

    return validProperty, validValue

def normalize(record):
    """Returns an observation record with normalized key and value
    """

    if not record:
        return None


    new_record = copy.deepcopy(record)
    new_record = normalize_type(new_record)
    new_record = normalize_key(new_record)
    new_record = normalize_value(new_record)
    new_record = normalize_id(new_record)

    new_record['source'] = {
        '@type': record.get('type', None),
        '@id': record.get('id', None)
    }
    new_record['instrument'] = {
        '@type': 'WebAPI',
        '@id': 'a1ab3ea2-e912-4959-9389-839748bd2beb',
        'name': 'Kraken_schema v2 value normalization'
    }
    
    
    return new_record


def normalize_type(record):

    if not record.get('observationAbout', None):
        record['observationAbout'] = {}
    
    # Normalize type
    about_type = record.get('observationAbout', {}).get('@type', None)
    
    try:
        record['observationAbout']['@type'] = kraken_schema.normalize_type(about_type)
    except Exception as e:
        a=1
    return record

def normalize_key(record):

    if not record:
        return None
    
    original_key = record.get('measuredProperty', None)
    
    # Normalize thing key
    k = record.get('measuredProperty', None)
    try:
        record['measuredProperty'] = kraken_schema.normalize_key(k)
        record['measuredProperty'] = record['measuredProperty'].replace('schema:', '')
    except:
        record['measuredProperty'] = None
    
    record['validProperty'] = True if record['measuredProperty'] is not None else False
    
    return record

def normalize_value(record):

    if not record:
        return None
    
    original_key = record.get('measuredProperty', None)
    original_value = record.get('value', None)
    about_type = record.get('observationAbout', {}).get('@type', None)
    about_type = about_type if about_type else 'thing'
    
    if not about_type or not original_key or not original_value:
        return record

    if not about_type.startswith('schema:'): 
        about_type = 'schema:' + about_type
    
    try:
        record['value'] = kraken_schema.normalize_value(about_type, original_key, original_value)
        #print('rv', original_value, record['value'])
        
    except Exception as e:
        record['value'] = None
    
    record['validValue'] = True if record['value'] is not None else False
        
    return record
        
 

def normalize_id(record):

    if not record:
        return None
        
    original_value = record.get('value', None)
    original_key = record.get('measuredProperty', None)

    if not original_key or not original_value:
        return record
    
    if original_key == '@id':
        try:
            uuid.UUID(str(original_value))
            record['validValue'] = True
        except ValueError:
            record['validValue'] = False

    return record