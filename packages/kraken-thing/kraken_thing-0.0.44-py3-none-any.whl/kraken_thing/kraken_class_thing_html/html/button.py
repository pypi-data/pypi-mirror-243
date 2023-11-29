



def button(url, action_id=None, action_value=None, text=None):
    
    new_url = url

    if action_id and action_value:
        new_url = str(url) + '?' + str(action_id) + '=' + str(action_value)
    
    link = f'<form action="{new_url}" method="post"><button class="btn btn-primary" name="{action_id}" value="{action_value}">{text}</button></form>'


    
    return link
