


def get_modal(modal_id, content):
    

    content = '''
        <!-- Modal -->
                <div class="modal fade" id="{modal_id}" tabindex="-1" aria-labelledby="exampleModalLabel" aria-hidden="true" role="dialog">
                  <div class="modal-dialog modal-lg">
                    <div class="modal-content">
                      {content}
                     
                    </div>
                  </div>
                </div>

    '''.format(
        modal_id = modal_id, 
        content=content
    )
    return content