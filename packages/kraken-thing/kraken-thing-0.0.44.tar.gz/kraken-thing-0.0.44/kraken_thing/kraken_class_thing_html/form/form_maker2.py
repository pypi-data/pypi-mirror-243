from kraken_schema_org import kraken_schema_org as kraken_schema
import requests
from kraken_thing.kraken_class_thing_html import html


def form_maker2(record_type, input_record=None, keys=None, translation=None, prefix=None, level=0):
    """Returns form

    parameters:
    - schema: the schema of the thing
    - input_record: the initial values 
    - fields: the fields to keepin form and in order required
    - translation: a dict containing the values to replace the harmonized field name with
    """

    # Get keys for the record_type
    keys = _get_base_keys(record_type) if not keys else keys
    keys = kraken_schema.get_keys(record_type) if not keys else keys

    if not keys:
        return None

    form_items = []
    
    for k in keys:
        
        k = k.replace('schema:', '')
        
        name = k
        auto = None

        
        # Get input_type
        datatype = kraken_schema.get_datatype(record_type, k)
        if not datatype:
            continue

        if len(datatype) > 1 and 'schema:Text' in datatype:
            datatype.remove('schema:Text')

            
        input_type = _get_input_type_from_datatype(k, datatype[0])

        
        # Get display title
        title = None
        if translation:
            title = translation.get(k, None)
        
        if not title:
            title = _get_base_translation(k)

        if not title:
            # Convert from camel case
            title = ''
            for l in k:
                if not l == l.lower():
                    title += ' ' 
                title += l
            title = title.capitalize()

            
        
        # Get value
        value = input_record.get(k, None) if input_record else None

        # Get form item, call itself if object

        if not input_type and level < 1:
            form_item = form_maker2(datatype[0], value, None, None, k, level + 1)

        elif not input_type:
            form_item = None
        
        else:
            form_item = _get_form_item(value, prefix, name, title, auto, input_type)

        if form_item:
            form_items.append(form_item)

    content = ''.join(form_items)
    return content




def _get_input_type_from_datatype(key, datatype):


    datatype = datatype.replace('schema:', '').lower()

    if datatype == 'country':
        return 'text'
    
    
    if datatype == 'text':
        if 'email' in key:
            return 'email'
        if 'telephone' in key:
            return 'tel'
        return 'text'
        
    if datatype == 'url':
        return 'url'
    if datatype == 'number':
        return 'number'

    if datatype in ['datetime']:
        return 'datetime-local'

    if datatype in [ 'date']:
        return 'date'
    
    if datatype in ['time']:
        return 'time'
        
    
    return None
    

def _get_form_item(value, prefix, name, title, auto, type):
    """Returns a form_item 
    """
    
    value = value if not isinstance(value, list) else value[0]
    
    input_name = name if not prefix else str(prefix) + '.' + name 

    #form_input = value, prefix, name, title, auto, type
    form_input = html.form_input(input_name, title, value, auto, '', type)
    return form_input




def _get_base_keys(record_type):

    record_type = record_type.replace('schema:', '').lower()
    
    base_keys = {
        'postaladdress': ['streetAddress', 'addressLocality',  'addressRegion', 'addressCountry','postalCode'],

        'person': ['givenName', 'familyName', 'address', 'phone', 'email'],
        'organization': ['name', 'legalName', 'url', 'email', 'address', 'telephone']
        
    }

    return base_keys.get(record_type, None)

def _get_base_translation(key):


    key = key.replace('schema:', '')
    
    base_translation = {
        'streetAddress': 'Street',
        'addressLocality': 'City',
        'addressRegion': 'Province',
        'addressCountry': 'Country',
        'postalCode': 'Postal code',
        'givenName': 'First name',
        'familyName': 'Family name'
    }

    return base_translation.get(key, None)

keys = None #translation.keys()

record = {}

form_maker2('person', record, keys, None)






'''
<input type="button">
<input type="checkbox">
<input type="color">
<input type="date">
<input type="datetime-local">
<input type="email">
<input type="file">
<input type="hidden">
<input type="image">
<input type="month">
<input type="number">
<input type="password">
<input type="radio">
<input type="range">
<input type="reset">
<input type="search">
<input type="submit">
<input type="tel">
<input type="text">
<input type="time">
<input type="url">
<input type="week">
'''