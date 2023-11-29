


def carousel(content_items):
    """
    """

    carousel_content = ''
    for i in content_items:
        carousel_content += carousel_item(i)
    
    content = '''
    <div id="carouselExampleControls" class="carousel slide" data-bs-ride="carousel">
      <div class="carousel-inner">
        {carousel_content}
      <button class="carousel-control-prev" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="prev">
        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Previous</span>
      </button>
      <button class="carousel-control-next" type="button" data-bs-target="#carouselExampleControls" data-bs-slide="next">
        <span class="carousel-control-next-icon" aria-hidden="true"></span>
        <span class="visually-hidden">Next</span>
      </button>
    </div>
    '''.format(carousel_content=carousel_content)

    return content

def carousel_item(item_content):
    """
    """

    content = '''
    <div class="carousel-item active">
          {item_content}
    </div>
    '''.format(item_content=item_content)

    return content