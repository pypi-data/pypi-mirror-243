

def deduplicate(things):
    """Given a list of things, returns a list of unduplicated things
    
    When a duplicate is found, it merges the observations together.
    """

    new_related_things = []
    for i in things:
        if i in new_related_things:
            for c in [x for x in new_related_things if x==i]:
                c.add(i)
        else:
            new_related_things.append(i)

    return new_related_things
    


def harmonize_ids(things):
    """Verify all the ids for a related things
    Ensure that if a thing changed id, all references are changed as well
    """
    
    # Gather all changes of ids
    id_list = []
    for i in things:
        
        # Get current record_refs
        current_record_ref = i.record_ref()
        # Get previous record_refs
        old_record_refs = i.record_refs()

        for i in old_record_refs:
            if i == current_record_ref:
                continue
            
            rec = {'old': i, 'new': current_record_ref}
            if rec not in id_list:
                id_list.append(rec)
        
    for i in id_list:
        old = i.get('old', None)
        new = i.get('new', None)
        replace_id(things, old, new)

        

def replace_id(things, old_id_ref, new_id_ref):
    """Replace all instances of old id by new id
    """
    
    old_id = old_id_ref.get('@id', None)
    new_id = new_id_ref.get('@id', None)

    # Cycle through things
    for thing in things:
        
        # Replace self @id and references
        for i in thing.observations:
            # Replace @id 
            if i.k == '@id' and i.value == old_id: 
                i.value = new_id
            # Replace record_refs
            elif i.value == old_id_ref:
                i.value = new_id_ref
    
    return things


