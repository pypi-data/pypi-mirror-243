
import datetime

def potential(thing):

    thing.set('actionStatus', 'potentialActionStatus')
    thing.set('startTime', None)
    
    return True


def active(thing):

    thing.set('actionStatus', 'activeActionStatus')
    thing.set('startTime', datetime.datetime.now())
    return True

def completed(thing):

    thing.set('actionStatus', 'completedActionStatus')
    thing.set('endTime', datetime.datetime.now())
    return True
    

def failed(thing):
    
    thing.set('actionStatus', 'failedActionStatus')
    thing.set('endTime', datetime.datetime.now())
    return True