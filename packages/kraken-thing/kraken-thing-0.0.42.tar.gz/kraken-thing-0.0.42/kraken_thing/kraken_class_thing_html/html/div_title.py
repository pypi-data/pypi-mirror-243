def div_title(html, alignment = 'None', minimum_height=0):

    minimum_height = str(minimum_height)
    
    if alignment == 'right':
        content = f'''
        <div class="container-fluid d-flex pt-2 justify-content-end min-vh-{minimum_height}">
            {html}
        </div>
        '''

    else:
        content = f'''
            <div class="container-fluid pt-2 min-vh-{minimum_height}">
                {html}
            </div>
            '''

    return content

