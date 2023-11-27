


def breadcrumb(path):
    """
    """

    if not isinstance(path, list):
        path = [path]

    new_path = path

    items = []

    # Add home
    item_home = '<li class="breadcrumb-item"><a href="/">Home</a></li>'
    items.append(item_home)
    
    # Add items
    url = ''
    while new_path:
        item = new_path.pop(0)
        url = url + '/' + item
        if len(new_path) >= 1:
            item = '<li class="breadcrumb-item"><a href="{url}">{item}</a></li>'.format(item=item, url=url)
        else:
            item = '<li class="breadcrumb-item active" aria-current="page">{item}</li>'.format(item=item)
            
        items.append(item)

    # Merge items
    item_content = ' '.join(items)

    # Generate content
    content = '''
        <nav aria-label="breadcrumb">
          <ol class="breadcrumb">
            {item_content}
          </ol>
        </nav>
    
    '''.format(item_content=item_content)
    
    return content