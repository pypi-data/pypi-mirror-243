
import uuid
import datetime
from dateutil.parser import parse
import copy
import hashlib
from kraken_thing import kraken_thing_methods as kr

from kraken_thing.kraken_class_observation.helpers import value_conversion
from kraken_thing.kraken_class_observation.helpers import observation_comparison
from kraken_schema_org import kraken_schema_org as kraken_schema
import requests
from kraken_thing.kraken_class_observation.helpers import observation_normalization as n
from kraken_thing.kraken_class_observation.helpers import observation_output 
#from kraken_thing.kraken_class_observation.helpers import observation_json 
from kraken_thing.kraken_class_observation.helpers import observation_hash


class Observation:


    def __init__(self, measuredProperty=None, value=None, metadata=None):
        """Observation class to store the values of a thing.
        
        Attributes
        ----------
        measuredProperty: str
            The property
        value:
            The value of the property
        unitCode: str
            The UN 3 char representatio nof unit code
        observationCredibility : float
            (credibility, c) The credibility of the observation from 0 to 1
        observationDate : datetime
            (date, d) The date of the observation as datetime. 
        validFrom : datetime
            The date where the value starts being effective
        validThrough : datetime
            The date where the value is no longer effective
        validProperty : Bool
            Returns True if property is valid
        validValue : Bool
            Returns True if value is valid type

        Methods
        -------
        summary() :
            A string representation of the content
        value_str() :
            A string representation fo the value
        load_metadata(record) :
            Loads metadata into object
        dump_metadata() :
            Returns a dict with all metadata
        load(record) :
            Load a record with all values
        dump() :
            Returns a dict with all values
        json() : 
            Returns a formatted json version of dump()
        things() :
            returns all things in nested values
        
    
        Returns
        -------
        list
            a list of strings used that are the header columns
        """
       
            
        self._keys = ['context', 'type', 'id', 'measuredPropertyContext', 'measuredProperty', 'value', 'unitCode', 'language', 'observationCredibility', 'observationDate', 'validFrom', 'validThrough', 'observationAbout', 'source', 'instrument' , 'agent', 'dateCreated', 'validProperty', 'validValue', 'hash']

        self._metadata_keys = ['measuredPropertyContext', 'language', 'observationCredibility', 'observationDate', 'validFrom', 'validThrough', 'observationAbout', 'source', 'instrument' , 'agent']

        self._summary_keys = ['type/id', 'measuredProperty', 'value', 'length', 'valid', 'lang','c', 'd', 'source', 'validFrom', 'validThrough']
        

        
        self._context =  'https://schema.org/'
        self._type = 'schema:observation'
        self._id = str(uuid.uuid4())
        
        self.observationAbout = {}                        # The thing at the origin of the observation
        self.source = {}                                  # The source of the observation (system, user, gov source)
        self.instrument = {}                              # The instrument used to gather observation
        self.agent = {}                                   # The person doing the observation
        
        self._measuredProperty = measuredProperty          # Property being referenced
        self._measuredPropertyContext = None
        self._value = None                                # Value of the property
        self.unitCode = None                              # The UN 3 char unit code

        self.language = None                              # The language of the value (if relevant)
        
        self._observationCredibility = None               # The credibility from 0 to 1 of the observation
        self._observationDate = None                      # Date the observation was measured

        self._validFrom = None                             # The date where value starts being valid
        self._validThrough = None                          # The date where value is no longer valid

        self.dateCreated = datetime.datetime.now()        # The date obs was created 
        self.dateModified = datetime.datetime.now()       # The date obs was modified
        self.dateDeleted = datetime.datetime.now()        # The date obs was deleted

        self.validProperty = None
        self.validValue = None

        # Attributes to track database state
        self._db = None                                   # True if obs exist in database
        

        
        if measuredProperty:
            self.measuredProperty = measuredProperty
        if value:
            self.value = value
        if metadata:
            self.load_metadata(metadata)
        

    
    def __str__(self):
        return self.summary()


    def __repr__(self):
        return self.summary()
    
    def __eq__(self, other):

        if not other:
            return False
            
        return True if self.hash == other.hash else False
        
    
    def __gt__(self, other):

        if not isinstance(other, Observation):
            return False
        
        # Check if same property, return True if self property > other property
        if self.measuredProperty != other.measuredProperty:
            return True if self.measuredProperty > other.measuredProperty else False

        # Check if deleted
        if not self.dateDeleted and other.dateDeleted:
            return True
        if self.dateDeleted and not other.dateDeleted:
            return False
        
        # Check if values are valid
        if not self.validValue and other.validValue:
            return False
        if self.validValue and not other.validValue:
            return True
        
        # Check if from - through dates are valid:
        if self.is_valid_date_from_through() and not other.is_valid_date_from_through():
            return True
        if not self.is_valid_date_from_through() and other.is_valid_date_from_through():
            return False

        # Check if credibility is lower
        if observation_comparison.compare_gt('observationCredibility', self, other):
            return True
        if observation_comparison.compare_lt('observationCredibility', self, other):
            return False

        # Check observationDate
        if observation_comparison.compare_gt('observationDate', self, other):
            return True
        if observation_comparison.compare_lt('observationDate', self, other):
            return False

        # Check dateCreated
        if observation_comparison.compare_gt('dateCreated', self, other):
            return True
        if observation_comparison.compare_lt('dateCreated', self, other):
            return False
        
        # Return False
        return False
        

    def __lt__(self, other):
            
        return other > self


    """String
    """

    def record_ref(self):
        """Returns type and id in a dict
        """
        return {'@type': self._type, '@id': self._id}

    def summary_record(self):
        """Returns a dict with summary info
        """
        return observation_output.get_summary_record(self.dump())
       
    def summary(self):
        """Returns a string containing the summary of the observation.
        """
        return observation_output.get_summary_string(self.dump())
       
    def value_str(self):
        """Returns the value of the observation as a formatted string.
        """
        value = value_conversion.value_conversion_to_string(self.value)
        return value
        
    
    """Hash
    """
    @property
    def hash(self):
        """Returns a hash of the record
        """
        return observation_hash.hash(self.dump(True))
        
    @hash.setter
    def hash(self, value):
        # sink
        return 

    # Keys
    def keys(self):
        """Returns the keys of the observation.
        """
        return self._keys


    """Metadata
    """

    @property
    def metadata(self):
        return self.dump_metadata()

    @metadata.setter
    def metadata(self, value):
        self.load_metadata(value)
        return
    
    def dump_metadata(self):
        """Returns a dict with metadata key/values
        """
        record = {}
        for i in self._metadata_keys:
            if getattr(self, i, None):
                record[i] = getattr(self, i, None)
                try:
                    record[i] = record[i].record_ref()
                except:
                    a=1
        return record

    def load_metadata(self, record:dict):
        """Load metadata into observation from metadata or dump of other observation
        """

        for k, v in record.items():
            if k not in ['measuredProperty', 'value']:
                k = k.replace('@', '')
                setattr(self, k, v)
        return
    
    """Load and dump values
    """
    def load(self, record):
        """Load dict into object
        """
        if not record:
            return
            
        # Convert from json if string
        if isinstance(record, str):
            print('r', record)
            record = kr.json.loads(record)

                
        # Deal with list
        if isinstance(record, list):
            if len(record) == 1:
                record = record[0]

        
        self._record_type = record.get('@type', self._type)
        self._record_id = record.get('@id', self._id)
        
        for k, v in record.items():
            # Skip if @
            if k.startswith('@'):
                k = k.replace('@', '')
            
            # Set
            setattr(self, k, v)

        return
        
    def dump(self, remove_hash = False):
        """Returns a dict with key/values of all properties
        """
        record = {
            'context': self._context, 
            'type': self._type,
            'id': self._id
        }
        for k in self._keys:
            #Skip if remove_has was selected
            if k == 'hash' and remove_hash:
                continue
            
            if getattr(self, k, None) not in [None, {}, []]:
                record[k] = getattr(self, k, None)
                try:
                    #record[k] = record[k].record_ref()
                    record[k] = record[k].dump()
                except:
                    a=1
        return record

    def json(self):
        """Returns a json version of dump()
        """
        return kr.json.dumps(self.dump())
        

    """Related items
    """
    def things(self):
        """
        """
        
        try:
            return self.value.things()
        except Exception as e:
            return []

    
    
    
    """Normalization
    """
    def get_normalized_observation(self):
        """Returns a new observation with normalized property and value
        """
        record = n.normalize(self.dump())
        o = Observation()
        o.load(record)

        return o 

        
        
    """Validity tests
    """
    
    def _test_valid(self):
        """Sets validProperty and validValue to True if valid. 
        """

        self.validProperty, self.validValue = n.test_valid(self.dump())
        
        return
        

    def is_valid_date_from(self, date=None):
        """Returns True if validFrom within date or Null
        """
        if not self.validThrough:
            return True
        date = date if date else datetime.datetime.now()        
        result = self.validFrom and self.validFrom < date
        return result

    
    def is_valid_date_through(self, date=None):
        """Returns True if validFrom within date or Null
        """
        if not self.validThrough:
            return True
        date = date if date else datetime.datetime.now()        
        result = self.validThrough and self.validThrough > date
        return result

    def is_valid_date_from_through(self, date=None):
        """
        """
        return self.is_valid_date_from(date) and self.is_valid_date_through(date)
        
    def is_valid(self):
        """Returns True if both valid property and value
        """
        c = self.validValue and self.validProperty and self.dateDeleted is None
        return c


    """Main properties
    """

    @property
    def observationCredibility(self):
        return self._observationCredibility

    @observationCredibility.setter
    def observationCredibility(self, value):

        
        value = value_conversion.value_conversion_to_float(value)
        
        # BR: Divide by zero if suspect it is percentage
        if value and value > 1 and value <=100:
            value = value / 100
        
        self._observationCredibility = value
        
        return
    
    @property
    def observationDate(self):
        return self._observationDate

    @observationDate.setter
    def observationDate(self, value):
            
        value = value_conversion.value_type_conversion(value)
        if isinstance(value, datetime.datetime):
            self._observationDate = value
        return
    

    @property
    def measuredProperty(self):
        return self._measuredProperty

    @measuredProperty.setter
    def measuredProperty(self, value):

        if not value:
            return
        
        if value.startswith('schema:'):
            value = value.replace('schema:', '')
            self.measuredPropertyContext = 'https://schema.org/'
        
        # Convert to correct type
        self._measuredProperty = value
        
        # Verify validity
        if self.value:
            self._test_valid()
        
        return
    
    @property
    def measuredPropertyContext(self):
        return self._measuredPropertyContext

    @measuredPropertyContext.setter
    def measuredPropertyContext(self, value):
        self._measuredPropertyContext = value
        return


    @property
    def value(self):
        return self._value

    @value.setter
    def value(self, value):

        if not value:
            return
            
        # Convert to correct type
        self._value = value_conversion.value_type_conversion(value)
        
        # Verify validity
        if self.measuredProperty:
            self._test_valid()
        
        return

    @property
    def validFrom(self):
        return self._validFrom

    @validFrom.setter
    def validFrom(self, value):
        # Convert to correct type
        self._validFrom = value_conversion.value_conversion_to_datetime(value)
        return

    @property
    def validThrough(self):
        return self._validThrough

    @validThrough.setter
    def validThrough(self, value):
        # Convert to correct type
        self._validThrough = value_conversion.value_conversion_to_datetime(value)
        return



    
    """Shortcuts
    """

    @property 
    def key(self):
        return self.measuredProperty

    @key.setter
    def key(self, value):
        self.measuredProperty = value

    @property 
    def k(self):
        return self.measuredProperty

    @k.setter
    def k(self, value):
        self.measuredProperty = value

    @property 
    def v(self):
        return self.value

    @v.setter
    def v(self, value):
        self.value = value
    
    @property 
    def credibility(self):
        return self.observationCredibility

    @credibility.setter
    def credibility(self, value):
        self.observationCredibility = value
    
    @property 
    def c(self):
        return self.observationCredibility

    @c.setter
    def c(self, value):
        self.observationCredibility = value

    @property 
    def d(self):
        return self.observationDate

    @d.setter
    def d(self, value):
        self.observationDate = value

    @property 
    def date(self):
        return self.observationDate

    @date.setter
    def date(self, value):
        self.observationDate = value


    @property
    def t(self):
        return self.observationAbout.get('@type', None)

    @t.setter
    def t(self, value):
        value = value.replace('schema:', '')
        self.observationAbout['@type'] = value
        return

    @property
    def n(self):
        return self.get_normalized_observation()

    @property
    def source_ref(self):
        t = self.source.get('@type', None)
        i = self.source.get('@id', None)
        return str(t) + '/' + str(i)