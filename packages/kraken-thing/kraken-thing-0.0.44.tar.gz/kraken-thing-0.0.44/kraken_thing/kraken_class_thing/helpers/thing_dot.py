"""
Methods to manipulate records that uses dot notation ({'parent.name': 'bob'} --> {'parent': {'name': 'bob'}})

"""


def from_dot(record):
    '''Convert a dot record to standard nested json
    '''

    if isinstance(record, list):
        return [from_dot(x) for x in record]

    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            if '.' in k:
                keys = k.split('.')
                key1 = keys[0]
                if key1 not in new_record.keys():
                    new_record[key1] = {}
                tmp_record = {'.'.join(keys[1:]): v}
                new_record[key1] = new_record[key1] | from_dot(tmp_record)
            else:
                new_record[k] = from_dot(v)
        return new_record
    else:
        return record
