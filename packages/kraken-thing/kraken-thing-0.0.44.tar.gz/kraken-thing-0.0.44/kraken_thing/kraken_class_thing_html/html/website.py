
from kraken_thing.kraken_class_thing_html.html.html_nav import html_nav
from kraken_thing.kraken_class_thing_html.html.footer import footer
from kraken_thing.kraken_class_thing_html.html.page import page


def website(config, page_title, main_content):
    """Given a config file, returns a webpage
    """
    

    # Get menu
    organization = config.get('subjectOf', {})
    brand = organization.get('brand', {})
    brand_name = brand.get('name', None)
    menu_items = config.get('menu', [])
    menu_content = html_nav(brand_name, menu_items)


    # Get footer
    organization = config.get('subjectOf', None)
    legal_name = organization.get('legalName', None)
    brand_name = brand.get('name', None)
    footer_items = config.get('footer', [])
    footer_content = footer(legal_name, brand_name, footer_items)

    # aggregate content
    content = menu_content + main_content 
    
    # Get page 
    page_content = page(page_title, menu_content, main_content, footer_content)

    return page_content

def get_config():
    """Returns a sample config file
    """
    
    record= {
        '@type': 'website',
        'name': 'Name of the website',
        'subjectOf': {
            '@type': 'organization',
            'name': 'Test_org_name',
            'legalName': 'Test_legal_name',
            'brand': {
                '@type': 'brand',
                'name': 'brand_name',
                'logo': 'http://logo_url.com'
            }
        },
        'menu': [
            {'text': 'Home', 'url': '/'},
            {'text': 'Products', 'url': '/products'},
            {'text': 'About us', 'url': '/about_us'}
        ],
        'footer': [
            {'text': 'Home', 'url': '/'},
            {'text': 'Products', 'url': '/products'},
            {'text': 'About us', 'url': '/about_us'}
        ]
    }

