"""
Provides summary records for each thing types

small: to be used for cards, short sumamry
medium: to be used for profile page

"""


def get(input_record, default_value=False):
    """Provides summary records for each thing types
    """

    record_type = input_record.get('@type', None)
    record_id = input_record.get('@id', None)
    
    records = get_summary_keys_small()

    print(records)
    r = [x.get('attributes', []) for x in records if x.get('record_type', None) == record_type]

    print(r)
    if not r or len(r) < 1:
        if default_value:
            return input_record
        else:
            return None

    keys = r[0]
    
    record = {'@type': record_type, '@id': record_id}
    for k in keys:
        record[k] = input_record.get(k, None)
        
    return record






def get_summary_keys_small():
    
    
    records = [
        
        {"record_type": "postalAddress", "attributes":['streetAddress', 'addressLocality', 'addressRegion', 'addressCountry', 'postalCode']},
        
        {"record_type": "person", "attributes": ['givenName', 'familyName']},
        
        {"record_type": "organization", "attributes":['name',  'url']}

    ]

    return records

def get_summary_keys_medium(record_type):
    
    record = [    
  
        {"record_type": "organization", "attributes": ['name', 'legalName', 'url', 'email', 'telephone', 'address', 'legalName', 'numberOfEmployees', 'parentOrganization']},
    
    {"record_type": "person", "attributes": ['givenName', 'familyName', 'jobTitle', 'worksFor',  'email', 'telephone', 'address']}
    
    ]
    return record