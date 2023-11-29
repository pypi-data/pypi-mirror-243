


def is_equal(thing1, other):
    """Given two Things, returns True if equal
    """
    if type(thing1) != type(other):
        return False

    # Case: Share smae type and id
    if thing1.type == other.type and thing1.id == other.id:
        return True

    # Case: Share common old record ids
    for i in thing1.record_refs():
        for x in other.record_refs():
            if x == i:
                return True

    # Case: Share common sameAs
    common_sameAs = [x for x in thing1.sameAs if x in set(other.sameAs)] 
    if thing1.type == other.type and len(common_sameAs) > 0:
        return True

    return False


def is_gt(thing1, other):
    """Given two Things, returns True if gt
    """
    if str(thing1.type) > str(other.type):
        return True
    elif str(thing1.type) == str(other.type):
        if str(thing1.id) > str(other.id):
            return True
    return False


def is_lt(thing1, other):
    """Given two Things, returns True if gt
    """
    return is_gt(other, thing1)