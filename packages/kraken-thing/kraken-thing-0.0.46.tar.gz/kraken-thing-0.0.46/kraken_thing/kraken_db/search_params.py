import datetime
import json

def get(params):
    """convert list of truple to mongodb params format
    """

    items = []
    for key, operator, value in params:

        o = _get_operator(operator)
        v = _get_value(o, value)

        search_string = {o: v}
        
        # Convert eq to regex if string and add /i option (case insensitive)
        if o == '$eq' and isinstance(v, str):
            #o = '$regex'
            #search_string = {o: v, '$options': 'i'}
            search_string = {o: v}

        if o == '$in' and isinstance(v, str):
            o = '$regex'
            search_string = {o: v, '$options': 'i'}
            #search_string = {o: v}
            
        # Case: specific record
        if key in ['record_type', 'record_id']:
            
            item = {
                key: search_string
            }

        # Case search all fields
        elif key == 'ALL':
            item = { 
                'observations': {
                    '$elemMatch':{
                        'value': search_string
                    }
                }
            }

        # Case search db fields
        elif key in ['datasource', 'datasource_id']:
            item = { 
                'observations': {
                    '$elemMatch':{
                        key: {'$eq': v}
                    }
                }
            }
            items.append(item)

            
        # Case: search specific field
        else:
            item = { 
                'observations': {
                    '$elemMatch':{
                        'measuredProperty': {'$eq': key},
                        'value': search_string
                    }
                }
            }
        items.append(item)

    query_record = {'$and': items}
    #print('qr', query_record)
    return query_record



def _get_operator(operator):

    if operator in ['eq', '=', '==']:
        return '$eq'
    if operator in ['in']:
        return '$in'    
    if operator in ['gt', '>']:
        return '$gt'
    if operator in ['ge', '>=', 'gte']:
        return '$gte'
    if operator in ['lt', '<']:
        return '$lt'
    if operator in ['le', '<', 'lte']:
        return '$lte'
    if operator in ['!=', 'not', 'ne']:
        return '$ne'
    if operator in ['nin']:
        return '$nin'


def _get_value(o, value):
    """Convert value into its proper type
    """

    if o == '$nin':
        if not isinstance(value, list):
            value = [value]

        values = []
        for i in value:
            values.append(_get_value(None, i))
        
        return values

    
    try:
        new_value = int(value)
        return new_value
    except:
        a=1
            
    try:
        new_value = float(value)
        return new_value
    except:
        a=1

    try:
        new_value = datetime.datetime.fromisoformat(value)
        return new_value
    except:
        a=1

    try:
        new_value = json.loads(value)
        if isinstance(value, (dict, list)):
            return new_value
    except:
        a=1

    return value