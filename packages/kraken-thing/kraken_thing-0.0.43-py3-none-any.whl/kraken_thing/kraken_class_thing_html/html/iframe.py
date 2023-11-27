

def iframe(url, width=510, height=400):
    """
    """

    if width and height:
        size_content = 'width="{width}" height="{height}"'.format(width=width, height=height)
    
    content = '''
        <iframe src="{url}" frameborder="0" {size_content} allowfullscreen="allowfullscreen"></iframe>
    '''.format(url=url, size_content = size_content)

    return content

    '''
    <iframe src="http" frameborder="0" width="510" height="400" scrolling="no" allowfullscreen="allowfullscreen"></iframe>
    
    '''