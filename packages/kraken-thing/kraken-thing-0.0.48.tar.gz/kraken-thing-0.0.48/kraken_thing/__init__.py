'''
import os
try:
    import kraken_thing_methods as k
except:
    
    
    package = 'github.com/tactik8/krakenthingmethods'
    token = 'REMOVETHIS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'
    token = token.replace('REMOVETHIS', '')
    string = 'pip install --upgrade git+https://{token}@{package}.git'.format(token = token, package = package)
    os.system(string)
    import kraken_thing_methods as k
    



from .kraken_class_observation import Observation
from .kraken_class_thing import Thing
from .kraken_class_things import Things

'''

from kraken_thing.kraken_class_things.kraken_class_things import Things
#import kraken_class_things.Thing as Thing
from kraken_thing.kraken_class_thing.kraken_class_thing import Thing
from kraken_thing.kraken_class_observation.kraken_class_observation import Observation