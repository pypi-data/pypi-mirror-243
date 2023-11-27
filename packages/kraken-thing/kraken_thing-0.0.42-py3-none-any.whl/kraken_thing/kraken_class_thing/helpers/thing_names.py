"""
Obtain the name of the thing based on convention if name is missing

"""





def get(record):
    """Obtain the name of the thing based on convention if name is missing

    """

    
    record_type = record.get('@type', None)
    record_id = record.get('@id', None)
    name = record.get('name', None)
    url = record.get('url', None)

    # Return name if exists in record
    if name:
        return name
    
    if not record_type:
        return None

    # Get name based on type
    if record_type == 'person':
        name = _get_name_from_person(record)
    if record_type == 'address':
        name = _get_name_from_address(record)

    # If empty, use url
    if not name:
        url = record.get('url', None)
        name = url

    # If empty, use type / id
    if not name:
        name = f'{record_type}/{record_id}'

    return name



def _get_name_from_person(record):
    """
    """
    fname = record.get('givenName', None)
    lname = record.get('familyName', None)
    
    name = ' '.join([fname, lname])

    return name



def _get_name_from_address(record):
    """
    """

    values = []
    for k in ['streetAddress', 'addressLocality', 'addressRegion', 'addressCountry', 'postalCode']:
        v = record.get(k, None)
        if v:
            values.append(v)
    name = ','.join(values)

    return name