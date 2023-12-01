
"""
Methods to deal with dicts 


"""



def from_list(record):
    """Remove empty lists and lists of one
    """

    if isinstance(record, list):
        new_records = []
        for i in record:
            result = from_list(i)
            if result:
                new_records.append(result)        
        
        new_records = new_records[0] if new_records and len(new_records) == 1 else new_records
        new_records = None if new_records and len(new_records) == 0 else new_records         
        return new_records

    
    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            v = [v] if not isinstance(v, list) else v
            result = from_list(v)
            if result:
                new_record[k] = result
        return new_record
    
    else:
        return record




def to_list(record):
    """Convert all items in a dict (or ist of dict) into lists
    """

    if isinstance(record, list):
        new_records = []
        for i in record:
            new_records.append(to_list(i))
        return new_records

    elif isinstance(record, dict):
        new_record = {}
        for k, v in record.items():
            v = [v] if not isinstance(v, list) else v
            new_record[k] = to_list(v)
        return new_record
    else:
        return record



