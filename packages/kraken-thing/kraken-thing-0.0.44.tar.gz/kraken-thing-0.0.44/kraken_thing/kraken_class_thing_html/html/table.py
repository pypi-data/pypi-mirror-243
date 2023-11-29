




def get_table_row(header, record, thumbnail= False):
     #Return html table line from record and header
        
    # Build row
    row = '<tr>'
    for h in header:
        # Build cell

        # Get data
        value = record.get(h, '')


        if isinstance(value, list):
            
            if thumbnail:
                if len(value) > 0:
                    value = value[0]
                else:
                    value = ''
            else:
                value = str(len(value)) + ' entities'

        content = value

        cell = '<td>' + str(content) + '</td>'
        row += cell

    row += '</tr>'

    return row




def table(records, header = None, header_title = None,thumbnail = True):
    """Converts json records to html table
    """

    if records is None:
        return ''
    
    if not header:
        header = []
        for record in records:
            if record is None:
                continue
            for k in record.keys():
                if k not in header:
                    header.append(k)
        header.sort()
    
    if not header_title:
        header_title = header


    if 1==0:
        if 'schema:contentUrl' in header:
            header.remove('schema:contentUrl')
            header.insert(0,'schema:contentUrl')
    
        if 'schema:contenturl' in header:
            header.remove('schema:contenturl')
            header.insert(0,'schema:contenturl')


    # Build rows
    rows = ''
    for record in records:
        rows += get_table_row(header, record, thumbnail)
        
    table_rows = '<tbody>' + rows + '</tbody>'

    # Build header

    header_text = '<thead class="table-dark"><tr>'
    for h in header_title:
        cell = '<th>' + h + '</th>'
        header_text += cell
    header_text += '</tr></thead>'


    # Build table
    table = f'<div class="table-responsive"><table class="table table-sm table-responsive"> {header_text} {table_rows} </table></div>'


    return table
