
from kraken_thing.kraken_class_thing_html import html
from kraken_thing.kraken_class_thing_html import helpers


class Things_html:
    """Contains html widgets related to thing

    Methods:
    - records() : returns enhanced values (link, etc) of things
    - table() : Returns a 2 column table with key / values
    - cards() : returns cards for things
   
    
    """

    def __init__(self, things):
        """
        """
        self._things = things

    
    def records(self):
        #Returns dict with enhanced values (link, etc)
        records = [helpers.html_record(x.dump()) for x in self._things.things]
        return records

    
    def table(self, keys=None, limit=20, offset=0):
        #Returns dict with enhanced values (link, etc)

        if not keys:
            keys = ['@type', '@id', 'name', 'url']

        records = self.records()[offset:(offset+limit)]
        
        return html.table(records, keys)
        
    
    def cards(self):
        #Returns cards for things    

        cards = []
        for i in self._things._things:
            cards.append(i.html.card())

        content = html.cardgrid(cards)
            
        return content
    

