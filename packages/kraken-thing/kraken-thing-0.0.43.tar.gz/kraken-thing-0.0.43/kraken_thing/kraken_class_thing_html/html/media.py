



def get_image(url, title = None, size = None, action_id=None):

    if isinstance(url, list):
        url = url[0]


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

    
    content = '<img loading="lazy" class="img-fluid" src="{url}" {size_html} {action_html}>'.format(url=url, title=title, size_html=size_html, action_html=action_html)

    return content


def get_video(url, text = None):

    if isinstance(url, list):
        url = url[0]
    
    if not url:
        return ''
    if len(url) < 5:
        return ''

    html_thumb = '''
            <video class="video-fluid z-depth-1" playsinline controls>
            <source src="{url}#t=2" type="video/mp4">
            <source src="{url}#t=2" type="video/ogg">
            </video>
            
        '''.format(url=url, text=text)

    html_thumb = '''
            <video class="video-fluid z-depth-1" playsinline controls>
            <source src="{url}#t=2">
            </video>
            
        '''.format(url=url, text=text)
    zzhtml_thumb = '''
            <div class="embed-responsive embed-responsive-21by9">
        <iframe class="embed-responsive-item" loading="lazy" src="{url}" allowfullscreen></iframe>
        </div>
            
        '''.format(url=url, text=text)




    #html = '<a href="{url}">{html_thumb}</a>'.format(url=url, html_thumb=html_thumb)


    return html_thumb
