"""Methods to facilitate the analysis of several observations
"""




def analysis(observations):
    """
    """

    properties = list(set([c.measuredProperty for c in observations]))

    results = []
    for i in properties: 
        obs = [x for x in observations if x.measuredProperty == i]
        results.append(analysis_single_property(obs))




def analysis_single_property(observations):

    if not observations:
        return None

    best = max(observations)
    
    record = {}
    record['measuredProperty'] = best.measuredProperty
    record ['maxValue'] = best.value
    record['quantity'] = len(observations)
    record['confidence'] = analysis_confidence(observations)
    
    
def analysis_confidence(observations):
    '''Returns confidence in value
    Measures dispersion of valid values
    '''

    values = []
    for i in observations:
        if i.v not in values:
            values.append(i.v)

    records = []
    for i in values:
        obs = [x for x in observations if x.value == i]
        sources = list(set([x.source_ref for x in obs]))

        record = {}
        record['value'] = i
        record['n'] = len(obs)
        record['c'] = max([x.c for x in obs])
        record['d'] = max([x.d for x in obs])
        record['sources'] = len(sources)
        records.append(record)
    
    return records