
import tabulate



def get_summary_string(things):

    # Thing header
    content = (40 * '-') + '\n' 

    # Values
    records = []
    # Get attributes

    for i in things:
        record = {
            'type': i.type,
            'id': i.id,
            'name': i.name,
            'url': i.url
        }
        records.append(record)

    keys = ['type', 'id', 'name', 'url']

    # Format into table
    header = keys
    rows =  [x.values() for x in records]
    table = str(tabulate.tabulate(rows, header))

    content += table + '\n'

    return content