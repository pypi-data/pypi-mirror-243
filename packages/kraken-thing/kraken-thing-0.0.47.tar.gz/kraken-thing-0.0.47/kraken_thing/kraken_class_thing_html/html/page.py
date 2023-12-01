


def page(title, head_content, body_content, foot_content):
    """Wraps html content into web page
    """
    content = f'''
        <!DOCTYPE html>
            <title>
                {title}
            </title>
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-T3c6CoIi6uLrA9TneNEoa7RxnatzjcDSCmG1MXxSR1GAsXEV/Dwwykc2MPK8M2HN" crossorigin="anonymous">
            <meta charset="utf-8">
            <head>
                {head_content}
                
            </head>
            <body>
                <div class="container-fluid">
                    {body_content}
                </div>
            <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.3.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-C6RzsynM9kWDrMNeT87bh95OGNyZPhcTNXj1NW7RuBCsyN/o0jlpcV8Qyq46cDfL" crossorigin="anonymous"></script>
            </body>
            <footer>
                {foot_content}
            </footer>
        </html>
        '''

    return content


