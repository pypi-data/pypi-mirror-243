


def schema_markup(json_record):
    """returns a schema markup
    """

    content = f'''
    
    <script type="application/ld+json">
    {json_record}
    </script>
    '''

    return content