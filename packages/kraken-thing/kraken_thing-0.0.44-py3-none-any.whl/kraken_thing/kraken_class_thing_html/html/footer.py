import datetime

def footer(legal_name, brand, item_links):
    '''
    '''


    # Get current year
    today = datetime.date.today()
    year = today.year

    # Transform links
    links = get_footer_links(item_links)

    # Combine content
    
    
    content = f'''

        <div class="container-fluid">
          <footer class="d-flex flex-wrap justify-content-between align-items-center py-3 my-4 border-top">
            
            <p class="col-md-4 mb-0 text-body-secondary">&copy; 2023 {legal_name}</p>
        
            <a href="/" class="col-md-4 d-flex align-items-center justify-content-center mb-3 mb-md-0 me-md-auto link-body-emphasis text-decoration-none">
              
            </a>
        
            <ul class="nav col-md-4 justify-content-end">
              {links}
            </ul>
          </footer>
        </div>

    '''
    return content


def get_footer_links(item_links):
    '''
    '''
    content = ''
    for link in item_links:
        content += footer_link(link.get('text'), link.get('url'))
    return content
        
    

def footer_link(text, url):
    '''
    '''

    content = f'''
        <li class="nav-item">
            <a href="{url}" class="nav-link px-2 text-body-secondary">
                {text}
            </a>
        </li>
    '''
    return content