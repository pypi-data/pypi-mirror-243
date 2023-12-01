
from kraken_thing.kraken_class_thing_html import helpers
from kraken_thing.kraken_class_thing_html import html
import uuid
import html as python_html

class Thing_html:
    """Contains html widgets related to thing

    Methods:
    - record() : returns dict with enhanced values (link, etc)
    - full() : Returns a 2 column table with key / values
    - card() : returns a card
    - media() : returns the media (video or pic)
    - video() : returns video
    - image() : returns image
    - link (): returns link with internal value
    - record_ref(): returns link with record_ref
    - modal () : 
    - title () :
    - record_table() : Values in two columns
    """

    def __init__(self, thing):
        """
        """
        self._thing = thing

    def record(self):
        #Returns dict with enhanced values (link, etc)
        record = helpers.html_record(self._thing.dump())
        if not self._thing.name:
            record['name'] = self._thing.get_name()
        return record
        
    def record_table(self):
        #Returns dict with enhanced values (link, etc)
        headers = ['key', 'value']
        records = []

        
        
        base_record = self.record()
        
        for k, v in base_record.items():
            v = v if isinstance(v, list) else [v]
            for v1 in v:
                records.append({'key': k, 'value': v1})
        
        return html.table(records, headers)

    def observations_table(self):
        # Returns html table with observations

        keys = self._thing.metadata._summary_keys
        obs = [x.summary_record() for x in self._thing.observations]
        
        return html.table(obs, keys)
    
        
    
    def card(self):
        #Returns dict with enhanced values (link, etc)
        
        modal_id = 'ref_' + str(uuid.uuid4())
        url = self._thing.get_thumbnail()
        content = html.image(url, None, 'xxs', True, modal_id)
        name = self.record_name_link()
        card = html.card(name, content)
        
        card += self.modal(modal_id)
        return card


    def modal(self, action_id=None):
        """Return modal with image and record
        """

        content= self.record_page()
        

        modal = html.div(html.get_modal(action_id, content))
        return modal
    
    
    def media(self):
        #Returns dict with enhanced values (link, etc)
        return

    def video(self):
        #Returns dict with enhanced values (link, etc)
        return

    def thumbnail(self):
        #Returns dict with enhanced values (link, etc)

        url = self._thing.get_image()
        content = html.image(url, None, 'xxs')
        return content

    
    def image(self):
        #Returns dict with enhanced values (link, etc)

        url = self._thing.get_image()
        content = html.image(url, None, 'xxl')
        return content


    def observations(self):
        """Returns observations in table
        """
        #obs = self._thing.dump_observations()
        records = [o.summary_record() for o in self._thing.observations]
        obs = helpers.html_record(records)

        for i in obs:
            i['value'] = python_html.escape(i.get("value", ""))
            
        header = ['measuredProperty', 'value', 'valid', 'c', 'd', 'validFrom', 'validThrough'] 
        header_title = ['Property', 'Value', 'Valid', 'Credibility', 'Date', 'From', 'Through']
        table_content = html.table(obs, header, header_title)
        return table_content
    

    def record_page(self):
        """Returns title, image and record in table
        """
        content= ''
        content += html.div(self.title(), None, 0, 2)
        content += html.div(self.image(), None, 0 , 2)
        content += html.div(self.action_buttons())
        content += html.div(self.record_table(), None, 0, 2)
        content += html.div(html.accordion('Observations', self.observations()), None, 0 , 2)
        content += html.schema_markup(self._thing.get_record())

        return content

    
    def record_link(self):
        # returns link for the record
        link = f'/{self._thing.type}/{self._thing.id}'
        html_link = html.link(link, link)
        return html_link

    def record_name_link(self):
        """Return html link to record using name as text
        """
        name = self._thing.get_name()
        link = f'/{self._thing.type}/{self._thing.id}'
        html_link = html.link(link, name)
        return html_link

    
    def record_ref(self):
        #Returns dict with enhanced values (link, etc)
        return

    def title(self):
        """
        """
        content = html.title(self._thing.get_name(), 'h1')
        content += html.title(self._thing.record_type_id(), 'h6')
        return content


    def schema_markup(self):
        """Returns js script with schema markup data
        """
        record = self._thing.get_record()
        html_content = html.schema_markup(record)
        return html_content


    def action_buttons(self):
        """
        """
        buttons = ''
                
        for i in self._thing.potential_actions:
            try:
                i = i.dump()
            except:
                a=1
                
            name = i.get('name', None)
            name = name if not isinstance(name, list) else name[0]
            url = i.get('target', None)
            url = url if not isinstance(url, list) else url[0]
            action_id = 'action_id'
            action_value = i.get('@id', None)
            action_value = action_value if not isinstance(action_value, list) else action_value[0]
            button = html.button(url, action_id, action_value, name)
            button = f'<div class="col-auto">{button}</div>'
            buttons += button

        buttons = f'''

            <div class="container-fluid text-end">
              <div class="row gx-1 justify-content-end">
                {buttons}
              </div>
            </div>
        '''
        return buttons

    def get_website(self, config, title, content):

        return html.website(config, title, content)
