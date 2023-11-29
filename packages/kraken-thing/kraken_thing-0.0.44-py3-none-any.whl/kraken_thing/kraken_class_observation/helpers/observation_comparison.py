


def compare_gt(attr, obs1, obs2):
    """
    """

    v1 = getattr(obs1, attr, None)
    v2 = getattr(obs2, attr, None)

    if not v1 and not v2:
        return False
    elif v1 and not v2:
        return True
    elif not v1 and v2:
        return False
    elif v1 > v2:
        return True

    return False



def compare_lt(attr, obs1, obs2):
    """
    """

    return compare_gt(attr, obs2, obs1)
