
"""
Methods to deal with dot notation

"""


def get(record, dots):
    """Return values using dot notation form dict
    """

    # Error handling
    if not dots or not record:
        return None
    
    # Deal with list
    if isinstance(record, list):
        results = []
        for i in record:
            results.append(get(i, dots))
        return results

    #Error handling 
    if not isinstance(record, dict):
        return None
    
    # Retrieve keys
    path = dots.split('.')

    key = path[0]

    value = record.get(key, None)

    # Return if end of path
    if len(path) == 1:
        return value

    else:
        return get(value, '.'.join(path[1:]))



def set(record, dots, value):
    """Set a value in dict using dot notation. Add value to list if list
    """
    # Error handling
    if not dots:
        return None

    
    # Deal with list
    if isinstance(record, list):
        results = []
        for i in record:
            results.append(get(i, dots))
        return results
    
    #Error handling 
    if not isinstance(record, dict):
        return None


    # Retrieve keys
    path = dots.split('.')
    key = path[0]

    if len(path) == 1:
        # Deal with list
        if isinstance(record.get(key, None), list):
            value = [value] if not isinstance(value, list) else value
            record[key] += value
        else:
            record[key] = value

    else:
        # Create dict if not exist
        if not record.get(key, None):
            record[key] = {}

        # Set value
        if isinstance(record.get(key, None), list):
            new_records = []
            for v in record.get(key, None):
                new_records.append(set(v, '.'.join(path[1:]), value))
            record[key] = new_records
        else:
            record[key] = set(record.get(key, None), '.'.join(path[1:]), value)
    
    return record





def to_dot(record, path=[]):
    """Returns record in dot notation
    """


    # Deal with list
    if isinstance(record, list):
        results = []
        level = 0
        for i in record:
            new_path = path + [f'[{level}]']
            results += to_dot(i, new_path)
            level += 1
        return results

    # Deal with non dict
    if not isinstance(record, dict):
        results = [{'key': '.'.join(path), 'value': record}]
        return results


    # Deal with dict
    results = []
    for k, v in record.items():
        new_path = path + [k]
        results += to_dot(v, new_path)
        
    return results


