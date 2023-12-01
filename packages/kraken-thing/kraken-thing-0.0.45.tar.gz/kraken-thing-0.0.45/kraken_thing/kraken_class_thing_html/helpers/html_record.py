
"""
Transforms record into html record (where values are html elements)
"""


from kraken_thing.kraken_class_thing_html import html
import uuid

def html_record(value, key=None):
    # Returns dict with enhanced values


    if not value:
        return None
        
    if isinstance(value, list):
        new_v = [html_record(x, key) for x in value]
        return new_v

    
    # Buidld new dict
    new_record = {}
    for key, values in value.items():

        new_record[key] = []
        values = [values] if not isinstance(values, list) else values
        
        for v in values:

            new_value = v
            
            if isinstance(v, dict):
                if '@type' in v.keys() and key:
                    new_value = html_value_record_ref(v)
            
            elif key and 'thumbnailUrl' in key:
                new_value = html_value_thumbnail(v)
            
            elif key and 'url' in key:
                new_value = html_value_url(v)
                
            elif key == '@type':
                new_value = html_value_type(v)

            elif key == '@id':
                new_value = html_value_id(value)
            
            else:
                new_v = v
                new_value = new_v
                
            new_record[key] = new_value

    return new_record



def html_value_record_ref(value):
    t = value.get('@type', None)
    i = value.get('@id', None)
    
    

    t = t if not isinstance(t, list) else t[0]
    i = i if not isinstance(i, list) else i[0]
    
    link = '/' + str(t) + '/' + str(i)

    name = value.get('name', None)
    name = name if name else link
    
    new_v = html.link(link, name)
    return new_v
    

def html_value_type(record_type):
    # Add link to types
    if isinstance(record_type, list) and len(record_type) > 0:
        record_type = record_type[0]
    new_v = html.link('/' + str(record_type), record_type)
    return new_v

def html_value_id(record):
    # Add link to types
    record_type = record.get('@type', None)
    if isinstance(record_type, list) and len(record_type) > 0:
        record_type = record_type[0]
    record_id = record.get('@id', None)
    if isinstance(record_id, list) and len(record_id) > 0:
        record_id = record_id[0]
    
    # Escape record id

    
    new_v = html.link('/' + str(record_type) + '/' + str(record_id), str(record_id))
    return new_v
    
def html_value_url(value):
    # Add link to url
    new_v = html.link(value, value)
    return new_v

def html_value_thumbnail(url):
    # Returns image with a link

    modal_id = 'ref_' + str(uuid.uuid4())
    image = html.image(url, None, 'xxs', None, modal_id)

    modal_content = html.image(url, None, 'xxl')
    modal = html.get_modal(modal_id, modal_content)

    content = image + modal
    

    
    return content