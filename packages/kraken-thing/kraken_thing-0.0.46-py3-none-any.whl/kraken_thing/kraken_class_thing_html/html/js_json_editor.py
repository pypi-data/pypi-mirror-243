


def json_editor():

    content = '''

        <script src="https://cdnjs.cloudflare.com/ajax/libs/ace/1.13.0/ace.js" integrity="sha512-btmS7t+mAyZXugYonCqUwCfOTw+8qUg9eO9AbFl5AT2zC1Q4we+KnCQAq2ZITQz1c9/axyUNYaNhGWqxfSpj7g==" crossorigin="anonymous" referrerpolicy="no-referrer"></script>
        
        <div id="editor-container" class="app_editor_wrapper">
            <div id="editor" class="app_editor">
{
    "@type": "schema:WebPage",
    "schema:url": "https://"
}
            </div>
        </div>
        <div>
        <button type="button" class="btn btn-primary" onclick="buttonClick()">Post</button>
        </div>

        
        
        <script>            
            var editor = ace.edit("editor");
            editor.setTheme("ace/theme/dawn");
            editor.session.setMode("ace/mode/json");

            editor.showCommandLine = function(val) {
                this.cmdLine.focus();
                if (typeof val == "string")
                    this.cmdLine.setValue(val, 1);
            };

        </script>


        <script>
        function buttonClick() {
            console.log('Button clicked')
            
            //var json_object = JSON.stringify(editor.getValue())
            var json_object = editor.getValue()
            console.log('json:');
            console.log(json_object);
            return new Promise(resolve => {
        
                fetch('https://engine.vlln.co/api', {
                    method: 'POST', // or 'PUT'
                    headers: {
                        'Content-Type': 'application/json',
                    },
                    body: json_object,
                })
                    .then((response) => response.json())
                    .then((data) => {
                        console.log('Success post record');
                    })
                    .catch((error) => {
                    });
                console.log('post');
                //console.log(data);
                resolve('Done');
            });

        }

        </script>
        

    '''
    return content

