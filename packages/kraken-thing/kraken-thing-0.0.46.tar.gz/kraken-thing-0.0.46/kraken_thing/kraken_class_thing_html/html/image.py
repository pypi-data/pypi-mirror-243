



def image(url, title = None, size = None, card = False, action_id=None):


    if not url:
        return ''

    if not isinstance(url, str):
        return ''
    
    if url.startswith('<'):
        return ''
    
    if isinstance(url, list):
        url = url[0]

    class_items = ''
    if card == True:
        class_items = 'card-img-top'
    
    size_html = ''
    if size == 'xxs':
        size_html = 'style="max-height:50px"'
    if size == 'xs':
        size_html = 'style="max-height:100px"'
    if size == 'sm':
        size_html = 'style="max-height:300px"'
    if size == 'md':
        size_html = 'style="max-height:600px"'
    if size == 'lg':
        size_html = 'style="max-height:1200px"'


    action_html = None
    if action_id:
        action_html = 'data-bs-toggle="modal" data-bs-target="#{action_id}"'.format(action_id=action_id)

    
    content = '<img loading="lazy" class="img-fluid {class_items}" src="{url}" {size_html} {action_html}>'.format(url=url, title=title, size_html=size_html, action_html=action_html, class_items=class_items)

    return content


