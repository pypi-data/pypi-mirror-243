import uuid

def accordion(title, content, expanded = False):
    """
    """

    component_id1 = 's' + str(uuid.uuid4())
    component_id2 = 's' + str(uuid.uuid4())
    component_id3 = 's' + str(uuid.uuid4())

    #component_id1 = 'aaa'
    #component_id2 = 'bbb'

    if expanded == True:
        expanded = 'aria-expanded="true"'
        collapsed = ''
        show = 'show'
    else:
        expanded = 'aria-expanded="false"'
        collapsed = 'collapsed'
        show = ''


    content = '''

            <div class="accordion" id="{component_id1}">
                <div class="accordion-item">
                    <h2 class="accordion-header" id="{component_id3}">
                        <button 
                            class="accordion-button {collapsed}" 
                            type="button" 
                            data-bs-toggle="collapse" 
                            data-bs-target="#{component_id2}" 
                            aria-controls="{component_id2}"
                            {expanded}
                            >
                            
                                {title}
                        </button>
                    </h2>
                    <div 
                        id="{component_id2}" 
                        class="accordion-collapse collapse {show}" 
                        aria-labelledby="{component_id2}" 
                        >
                        
                        <div class="accordion-body">
                            
                            {content}
                        </div>
                    </div>
                </div>
            
            </div>

    
        '''.format(
            title = title,
            content = content,
            component_id1 = component_id1,
            component_id2 = component_id2,
            component_id3 = component_id3,
            expanded = expanded,
            collapsed = collapsed,
            show = show
            )

    return content

