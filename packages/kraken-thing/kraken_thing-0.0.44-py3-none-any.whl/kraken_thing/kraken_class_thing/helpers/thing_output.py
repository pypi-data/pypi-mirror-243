
import tabulate



def get_summary_string(type, id, observations):

    # Thing header
   
    content = f'{str(type)}/{str(id)}\n'

    # Values
    records = []
    # Get attributes
    attr = list(set([o.k for o in observations]))
    attr.sort()
    
    # Get observations for each attribute        
    for k in attr:
        obs = [x for x in observations if x.k == k]
        for i in obs:
            records.append(i.summary_record())

    # Format into table
    header = records[0].keys()
    rows =  [x.values() for x in records]
    table = str(tabulate.tabulate(rows, header))

    content += table + '\n'

    return content