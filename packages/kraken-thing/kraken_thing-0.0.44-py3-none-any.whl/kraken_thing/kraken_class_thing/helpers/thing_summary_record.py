"""
Provides summary records for each thing types

small: to be used for cards, short sumamry
medium: to be used for profile page

"""


def get(record):
    """Provides summary records for each thing types
    """

    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    
    keys = get_summary_keys(record_type)

    record = {'@type': record_type, '@id': record_id}
    for i in keys:
        record[k] = record.get(k, None)
        
    return record


def get_summary_keys(record_type):
    
    records = {}
    
    records['postalAddress_small'] = ['streetAddress', 'addressLocality', 'addressRegion', 'addressCountry', 'postalCode']


    records['organization_small'] = ['name', 'legalName', 'url', 'email', 'telephone', 'address']
    
    records['organization_medium'] = ['name', 'legalName', 'url', 'email', 'telephone', 'address', 'legalName', 'numberOfEmployees', 'parentOrganization']


    records['person_small'] = ['givenName', 'familyName', 'jobTitle']
    
    records['person_medium'] = ['givenName', 'familyName', 'jobTitle', 'worksFor',  'email', 'telephone', 'address']


    return records.get(record_type, None)