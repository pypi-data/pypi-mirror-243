
from kraken_thing.kraken_class_thing_html import html


def form_maker(config, record, prefix):

    # Compile form inputs
    form_inputs = []

    for i in config:
        name = i.get('name', None)
        title = i.get('title', None)
        auto = i.get('auto', None)
        type = i.get('type', None)
        value = record.get(name, None)

        form_input = form_item(value, prefix, name, title, auto, type)
        
        form_inputs.append(form_input)


    content = ''.join(form_inputs)
    
    return content



def form_item(value, prefix, name, title, auto, type):
    """Returns a form_item 
    """
    
    value = value if not isinstance(value, list) else value[0]
    
    input_name = name if not prefix else str(prefix) + '.' + name 
    
    form_input = html.form_input(input_name, title, value, auto, '', type)

    return form_input