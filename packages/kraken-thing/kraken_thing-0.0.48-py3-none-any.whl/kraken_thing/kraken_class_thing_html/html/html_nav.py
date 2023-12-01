

def html_nav(brand, item_links):
    """

    Takes input as ist of dict with text, url
    """

    # Generate menu items
    menu_items_content = get_menu_items(item_links)


    # Geneate full menu
    content = full_menu(brand, menu_items_content)

    return content


def get_menu_items(item_links):

    menu_items_content = ''
    
    for item_link in item_links:
        menu_items_content += get_menu_item_content(item_link['text'], item_link['url'])

    return menu_items_content

def get_menu_item_content(item, link):

    content = '''
        <li class="nav-item">
            <a class="nav-link active" aria-current="page" href="{link}">
                {item}
            </a>
        </li>
        '''.format(
            item = item, 
            link = link
            )
    return content


def full_menu(brand, menu_items_content):
    # Geneate full menu
    content = '''
        <nav class="navbar navbar-expand-md navbar-dark bg-dark">

            <div class="container-fluid">

                <a class="navbar-brand" href="/">
                    {brand}
                </a>

                <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#navbarNav" aria-controls="navbarNav" aria-expanded="false" aria-label="Toggle navigation">
                    <span class="navbar-toggler-icon"></span>
                </button>

                <div class="collapse navbar-collapse" id="navbarNav">
                    <ul class="navbar-nav">
                
                        {menu_items_content}

                    </ul>
                </div>
            </div>

            <!-- Navbar content -->
        </nav>
        '''.format(
            brand = brand, 
            menu_items_content = menu_items_content
            )

    return content