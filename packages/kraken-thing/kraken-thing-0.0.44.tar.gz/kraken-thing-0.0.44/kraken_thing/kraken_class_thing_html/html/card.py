

def card(title, content = '', url = None):
    """content - html fo the content
    title - text
    url - url for link
    """

    
    #card body
    card_body = ''
    if title:
        card_body = '''
            <p class="card-text">{title}</p>  
            '''.format(title=title)

    #card link
    card_link = ''
    if url:
        card_link = '''
        <a href="{url}" class="card-link">{url}</a>
        '''.format(url=url)

    # assemble
    image_card = '''
        <div class="card h-100">
            <div class="card-body">
                {content}
                {card_body}
                {card_link}
            </div>
        </div>    '''.format(content=content, card_body=card_body, card_link=card_link)

    return image_card



