
from kraken_thing.kraken_class_thing_html import form


def person(record=None, prefix=''):

    """Returns html form for a person object

    parameters
        record: the record with initial values ot populate form fields with
        prefix: the prefix to add to field names (useful when part of a hierarchy)
    
    """
    
    
    content = []

    # Add name
    name_record = record if record else None
    content.append(form.name(name_record, prefix))

    # Add address
    address_record = record.get('address', {}) if record else None
    content.append(form.address(address_record, prefix ))

    # Add fields
    config = [
        {'name': '@type', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': '@id', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': 'telephone', 'title': 'Phone', 'auto': '', 'type': 'text'},
        {'name': 'email', 'title': 'Email', 'auto': 'email', 'type': 'email'},
    ]

    content.append(form.form_maker(config, record, prefix))

    return ''.join(content)





   