

def video(url, text = None, thumbnail_url = None):

    
    if isinstance(url, list):
            url = url[0]
        
    if not url or len(url) < 5:
        return ''

   

    html_thumb = '''
        <video class="video-fluid card-img-top z-depth-1" poster="{thumbnail_url} playsinline controls>
        <source src="{url}#t=2">
        </video>
        
    '''.format(url=url, text=text, thumbnail_url = str(thumbnail_url))
   




    return html_thumb