from kraken_thing.kraken_class_thing_html import html



def name(record={}, prefix=None):


    
    # Compile form inputs
    form_inputs = []

    name1 = 'givenName' 
    title1 = 'First name'
    auto1 = 'given-name'
    type1 = 'text'
    value1 = record.get(name1, None)

    name2 = 'familyName' 
    title2 = 'Last name'
    auto2 = 'family-name'
    type2 = 'text'
    value2 = record.get(name2, None)

    
    form_input = html.form_input_two(name1, title1, value1, auto1,  name2,title2, value2, auto2, '', type2)
    
    form_inputs.append(form_input)


    content = ''.join(form_inputs)
    
    return content
