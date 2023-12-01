
import uuid

def flatten(record, top_level=True):
    """Removes embedded things from record, leaving in place a reference (record_ref)
    returns tuple: simplified original record and list of childs
    """

    if isinstance(record, list):
        results = []
        childs = []
        
        for i in record:
            result, child = flatten(i, False)
            result = [result] if not isinstance(result, list) else result
            child = [child] if not isinstance(child, list) else child
            results += result
            childs += child

        return results, childs

    elif isinstance(record, dict):

        # Iterate through k, v
        new_record = {}
        childs = []
        for k, v in record.items():
            new_value, child = flatten(v, False)
            child = [child] if not isinstance(child, list) else child
            new_record[k] = new_value

            child = [child] if not isinstance(child, list) else child
            childs += child

        # Handle things
        if top_level or '@type' not in new_record.keys():
            return new_record, childs

        else:
            record_type = new_record.get('@type', None)
            record_id = new_record.get('@id', str(uuid.uuid4()))

            new_record['@id'] = record_id
                                       
            ref_record = {
                '@type': record_type,
                '@id': record_id
            }
            return ref_record, [new_record] + childs
            
    
    else:
        return record, []



def get_record_ref(record):
    """
    """

    if isinstance(record, list):
        results = []
        for i in record:
            results.append(get_record_ref(i))
        return results

    
    record_ref = {
        "@type": record.get('@type', None),
        '@id': record.get('@id', None)
    }
    return record_ref

