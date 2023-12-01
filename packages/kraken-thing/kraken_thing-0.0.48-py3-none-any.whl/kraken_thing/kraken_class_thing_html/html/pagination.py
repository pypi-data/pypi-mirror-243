


def pagination(url, offset = 0, limit = 20, url_args = {}):

    
    try:
        offset = int(offset)
    except:
        a=1

    try:
        limit = int(limit)
    except:
        a=1

    buttons = []

    current_page = int((offset / limit ) + 1)
    
    # Back button (<<)
    url_args['limit'] = limit    
    
    url_args['offset'] = (int(offset) - int(limit)) if current_page > 1 else 0
    url_button = get_url_with_args(url, url_args)
    name = '&laquo;'
    active = False  
    buttons.append(get_nav_button(url_button, name, active))

    # 1 button
    url_args['limit'] = limit    
    url_args['offset'] = 0
    url_button = get_url_with_args(url, url_args)
    name = '1'
    active = False
    if offset == 0:
        active = True    
    buttons.append(get_nav_button(url_button, name, active))

    # ... button
    if current_page > 3:
        url_args['limit'] = limit    
        url_args['offset'] = 0
        url_button = '#'
        name = '...'
        active = False
        if offset == 0:
            active = True    
        buttons.append(get_nav_button(url_button, name, active))

    # -1 button
    if current_page > 2:
        url_args['limit'] = limit    
        url_args['offset'] =  offset - limit
        url_button = get_url_with_args(url, url_args)
        name = current_page - 1
        active = False
        if offset == 0:
            active = True    
        buttons.append(get_nav_button(url_button, name, active))

    # current button
    if current_page > 1:
        url_args['limit'] = limit    
        url_args['offset'] = offset
        url_button = get_url_with_args(url, url_args)
        name = current_page
        active = True 
        buttons.append(get_nav_button(url_button, name, active))

    # +1 button
    url_args['limit'] = limit    
    url_args['offset'] = offset + limit
    url_button = get_url_with_args(url, url_args)
    name = current_page + 1
    active = False
    buttons.append(get_nav_button(url_button, name, active))

    # +2 button
    if current_page ==1:
        url_args['limit'] = limit    
        url_args['offset'] = offset + (2 * limit)
        url_button = get_url_with_args(url, url_args)
        name = current_page + 2
        active = False
        buttons.append(get_nav_button(url_button, name, active))
        
    # Next button (>>)
    url_args['limit'] = limit    
    url_args['offset'] = int(offset) + int(limit)
    url_button = get_url_with_args(url, url_args)
    name = '&raquo;'
    active = False    
    buttons.append(get_nav_button(url_button, name, active))
    

    buttons_html = ' '.join(buttons)

    content = '''
                <div class="d-flex justify-content-end">
                    <nav aria-label="Page navigation example">
                    <ul class="pagination">
                        {buttons}
                    </ul>
                    </nav> 
                </div>
            '''.format(
                buttons=buttons_html
                )

    return content


def get_url_with_args(base_url, url_args):

    args = []
    for key in url_args:
        arg = key + '=' + str(url_args[key])
        args.append(arg)

    full_url = base_url + '?' + '&'.join(args)

    return full_url


def get_nav_button(url, name, active=False):
        """
        """

        active_class = ''
        if active:
            active_class = 'active'
        
        
        nav_button = '''
        <li class="page-item"><a class="page-link {active_class}" href="{url}">{name}</a></li>
        '''.format(url=url, name=name, active_class = active_class)
    
        return nav_button
