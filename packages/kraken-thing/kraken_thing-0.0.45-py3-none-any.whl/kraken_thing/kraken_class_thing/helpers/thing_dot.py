"""
Methods to manipulate records that uses dot notation ({'parent.name': 'bob'} --> {'parent': {'name': 'bob'}})

"""


    
def from_dot(record):
    if isinstance(record, list):
        return [from_dot(x) for x in record]

    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            keys = k.split('.')
            current_dict = new_record

            for key in keys[:-1]:
                current_dict = current_dict.setdefault(key, {})

            current_dict[keys[-1]] = v

        return new_record
    else:
        return record