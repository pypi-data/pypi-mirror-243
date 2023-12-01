
def link(url, text, new_tab = None):
    """Converts a url and text into a html link
    """
    if new_tab:
        link = f'<a href="{url}" target="_blank">{text}</a>'
    else:
        
        link = f'<a href="{url}">{text}</a>'
    return link
