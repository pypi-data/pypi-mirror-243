def div(html, alignment=None, minimum_height=0, padding=0):

    minimum_height = str(minimum_height)
    
    if alignment == 'right':
        content = f'''
        <div class="container-fluid d-flex justify-content-end min-vh-{minimum_height} {'p-' + str(padding) if padding else ''}">
            {html}
        </div>
        '''

    else:
        content = f'''
            <div class="container-fluid min-vh-{minimum_height} {'p-' + str(padding) if padding else ''}">
                {html}
            </div>
            '''

    return content

