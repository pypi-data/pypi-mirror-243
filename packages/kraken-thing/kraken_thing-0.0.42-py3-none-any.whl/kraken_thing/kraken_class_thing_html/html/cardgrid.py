


def cardgrid(cards):

    card_html = ''
    for card in cards:
        card_html += '<div class="col mb-3"> {card} </div>'.format(card=card)


    grid_card = '<div class="row">{card_html}</div>'.format(card_html = card_html)

    return grid_card


#row-cols-1 row-cols-md-4 row-cols-auto