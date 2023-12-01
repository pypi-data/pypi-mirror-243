


from kraken_thing.kraken_class_thing_html.form.form_maker import form_maker

def url(record={}, prefix=''):




    config = [
        {'name': '@type', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': '@id', 'title': '', 'auto': '', 'type': 'hidden'},
        {'name': 'url', 'title': 'URL', 'auto': 'url', 'type': 'url'},
       
    ]


    return form_maker(config, record, prefix)
    
   

