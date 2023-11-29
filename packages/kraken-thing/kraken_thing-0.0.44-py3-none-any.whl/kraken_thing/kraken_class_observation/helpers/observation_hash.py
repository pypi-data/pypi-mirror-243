
import hashlib
import json

def hash(record):

    hash_keys = ['measuredProperty', 'value', 'measuredPropertyContext', 'language', 'observationCredibility', 'observationDate', 'validFrom', 'validThrough', 'observationAbout', 'source', 'instrument' , 'agent']

    new_record = {}
    for i in hash_keys:
        value = record.get(i, None)
        if isinstance(value, dict):
            value = {
                '@type': value.get('@type', None),
                '@id': value.get('@id', None)
            }        
        new_record[i] = value

    dhash = hashlib.md5()
    encoded = json.dumps(new_record, sort_keys=True, default=str).encode()
    dhash.update(encoded)
    return dhash.hexdigest()
