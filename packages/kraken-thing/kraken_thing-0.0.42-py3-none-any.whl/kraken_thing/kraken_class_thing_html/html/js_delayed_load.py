

import uuid

def js_delayed_load(url):
    """Returns component for delayed load
    """
    
    div_id = str(uuid.uuid4()).replace('-', '')

    content = '''
        <div id="{div_id}"> </div>
        <script>
        
        async function load_{div_id}() {{
            try {{
                const response = await fetch("{url}")
                const text = await response.text()
                document.getElementById("{div_id}").innerHTML = text
            }}
            catch(err) {{
                document.getElementById("{div_id}").innerHTML = "Error " + err
            }}
            }}
             
            
        load_{div_id}()
        
       
       
         </script>
         '''.format(div_id=div_id, url=url)
    return content