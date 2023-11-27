

def form(content, action):
    

    content = f'''
    <form action="{action}" method="post">
     {content}
     <input type="submit" value="Submit">
    </form>
    '''

    return content


