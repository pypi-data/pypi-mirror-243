



def localize(record, language='EN-US'):
    """Localize a record
    """

    if isinstance(record, dict):
        record_type = record.get('@type', None)
        new_record = {}
        for k,v in record.items():
            new_k = get_attribute(record_type, k, language, True)
            new_record[new_k] = localize(v)
        return new_record
    if isinstance(record, list):
        new_record = []
        for i in record:
            new_record.append(localize(i))
        return new_record
    else:
        return record

    


def get_attribute(record_type, attribute, language='EN-US', default_value=False):
    """Given a record_type, attribute and ISO 639-1 standard language codes, return's attribute equivalent 
    """

    records = _get_records()
    
    values = [x.get('value', None) for x in records if x.get('attribute', None) == attribute and language in x.get('languages', None) and (x.get('record_type', None)) in [None, record_type]]
    
    if values and len(values) > 0:
        return values[0]
    else:
        if default_value:
            return attribute
        else:
            return None


def _get_records():

    records = [

        {"record_type": None, "attribute": "sameAs", "languages": ["EN-CA", "EN-US"], "value": "Same as"},
        {"record_type": None, "attribute": "subjectOf", "languages": ["EN-CA", "EN-US"], "value": "Subject of"},
        
        {"record_type": None, "attribute": "addressCountry", "languages": ["EN-US"], "value": "Country"},
        {"record_type": None, "attribute": "addressLocality", "languages": ["EN-US"], "value": "City"},
        {"record_type": None, "attribute": "addressRegion", "languages": "EN-US", "value": "State"},
        {"record_type": None, "attribute": "postalCode", "languages": ["EN-US"], "value": "ZIP code"},
        {"record_type": None, "attribute": "streetAddress", "languages": ["EN-US"], "value": "Street"},
        {"record_type": None, "attribute": "postOfficeBoxNumber", "languages": ["EN-US"], "value": "PO box"},


        {"record_type": None, "attribute": "addressCountry", "languages": ["EN-CA"], "value": "Country"},
        {"record_type": None, "attribute": "addressLocality", "languages": ["EN-CA"], "value": "City"},
        {"record_type": None, "attribute": "addressRegion", "languages": ["EN-CA"], "value": "Province"},
        {"record_type": None, "attribute": "postalCode", "languages": ["EN-CA"], "value": "Postal code"},
        {"record_type": None, "attribute": "streetAddress", "languages": ["EN-CA"], "value": "Street"},
        {"record_type": None, "attribute": "postOfficeBoxNumber", "languages": ["EN-US"], "value": "PO box"},


        {"record_type": None, "attribute": "givenName", "languages": ["EN-US", "EN-CA"], "value": "First name"},
        {"record_type": None, "attribute": "familyName", "languages": ["EN-US", "EN-CA"], "value": "Last name"},


        {"record_type": "organization", "attribute": "legalName", "languages": ["EN-US", "EN-CA"], "value": "Legal name"},
        {"record_type": "organization", "attribute": "telephone", "languages": ["EN-US", "EN-CA"], "value": "Phone"},
        {"record_type": "organization", "attribute": "parentOrganization", "languages": ["EN-US", "EN-CA"], "value": "Parent organization"}
        
    ]
    return records