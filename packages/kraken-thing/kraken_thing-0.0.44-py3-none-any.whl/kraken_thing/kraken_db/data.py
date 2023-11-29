import datetime
import json

def convert_db_record_to_observations(records):
    """Takes a record and convert to observations
    """

    return records
    
    if not records:
        return []
    
    if not isinstance(records, list):
        records = [records]

    
    
    observations = []

    for i in records:
        if i:
            o = i.get('observations', None)
            observations += o

    # Convert from json if needed
    for i in observations:
        value = i.get('value', None)
        if isinstance(value, str) and "{" in value:
            try:
                new_value = value.replace("'", '"')
                new_value = json.loads(new_value)
                i['value'] = new_value
    
            except Exception as e:
                #print(e)
                a=1

    
    return observations

def convert_observations_to_db_record(observations):
    """Convert obs to record
    """

    return observations
    
    if not isinstance(observations, list):
        observations = [observations]


    # Clean observations
    new_observations = []
    for i in observations:
        o = {
            'record_type': i.get('record_type', None),
            'record_id': i.get('record_id', None),
            'key': i.get('key', None),
            'value': i.get('value', None)
        }

        for k, v in i.items():
            if v:
                o[k] = v
        
        new_observations.append(o)
    
    observations = new_observations

    
    records = {}

    # Group observation by type / id
    for i in observations:
        record_type = i.get('record_type', None)
        record_id = i.get('record_id', None)

        record_ref = record_type + '/' + record_id

        if not records.get(record_ref, None):
            records[record_ref] = {}
            records[record_ref]['record_type'] = record_type
            records[record_ref]['record_id'] = record_id
            records[record_ref]['observations'] = []

        records[record_ref]['observations'].append(i)


    # Assemble into individual records
    record_list = []
    for key, value in records.items():

        record = {
            'record_type': value.get('record_type', None),
            'record_id': value.get('record_id', None),
            'observations': value.get('observations', None)
        }
        record_list.append(record)
        

    return record_list
