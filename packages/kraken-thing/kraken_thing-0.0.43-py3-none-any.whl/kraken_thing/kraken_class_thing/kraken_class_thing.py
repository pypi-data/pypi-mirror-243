import copy
from re import L
import uuid
import hashlib
import tabulate
import datetime
import asyncio 

import os
from kraken_thing import kraken_thing_methods as kr



from kraken_thing.kraken_class_observation.kraken_class_observation import Observation
from kraken_thing.kraken_class_thing.templates import metadata_templates as template
from kraken_thing.kraken_class_thing.helpers import things_manipulation
#from kraken_thing.kraken_class_thing.helpers import thing_json
from kraken_thing.kraken_class_thing.helpers import thing_output
from kraken_thing.kraken_class_thing.helpers import thing_comparison
from kraken_thing.kraken_class_thing.helpers import thing_api
from kraken_thing.kraken_class_thing.helpers import thing_names
from kraken_thing.kraken_class_thing.helpers import thing_summary_record
from kraken_thing.kraken_class_thing.helpers import thing_dot



from kraken_thing.kraken_class_thing_html.kraken_class_thing_html import Thing_html
from kraken_thing.kraken_class_thing_db.kraken_class_thing_db import Kraken_thing_db



class Thing:
    """Thing class to store observations of a thing.

    thing.get_test_record(record_type, record_id) return a test record to help 

    Attributes
    ----------
    type: str
        The type of the thing
    id:
        The id of the thing. Defaults to uuid4
    metadata: Observation
        An object to store metadata used to create new observations.
    name: str
        The best name value
    url: str:
        The best url value
    sameAs: list
        List of all sameAs values
    
    first_name : str
        Alternative to Get / sets field givenName
    last_name : str
        Alternative to Get / sets field familyName
    city : str
        Alternative to Get / sets field addressLocality
    state : str
        Alternative to Get / sets field addressRegion
    province : str
        Alternative to Get / sets field addressRegion
    postal_code : str
        Alternative to Get / sets field postalCode
    country : str
        Alternative to Get / sets field addressCountry


    Methods
    -------
    get(property) : 
        Returns all observations for a given property
    get_best() :
        Returns the best observations for a property
    set(attribute, value): bool
        Creates a new observation with given attribute and value, using metadata as default
    load(record) :
        Load a record
    dump() :
        Dump the value of thing and sub things in json record
    get_json : str
        Returns content of object as json
    load_json : bool
        Loads content of json in object
    summary():
        Returns a text representation of the thing
    db_load(record):
        Load a record
    db_dump():
        Dump the value of thing and sub things in full json record with metadata
    deduplicate_things(): 
        Removes duplicates in related things
    get_thumbnail : url
        Returns best thumbnail value
    get_image : url
        Returns best image value

    api_url(url): 
        Sets url for the api (only have to do this once)
    api_get(): 
        Get record from api with given id and type
    api_post(): 
        Post record to api
    api_get_async(): 
        Get record from api async with given id and type
    api_post_async(): 
        Post record to api async
        

    Returns
    -------
    list
        a list of strings used that are the header columns
    """

    def __init__(self, record_type = None, record_id=None, metadata=None):
        

        
        self._o = []                        # List of all observations
        self._metadata = Observation()      # An observation used to store metadata  

        self._things = []                   # store sub records


        self.set('@context', 'https://schema.org/')

        self.template = template
        
        # Add html module
        self.html = Thing_html(self)

        # Add db module
        self.db = Kraken_thing_db(self)

        
        # value initiation
        if record_type:
            self.type = record_type
        if record_id:
            self.id = record_id
            
        # Load metadata if provided
        if metadata:
            self._metadata.load_metadata(metadata)

        # Basic types, these should not be their own thing when exporting
        self._basic_types = ['monetaryAmount', 'quantitativeValue']

    
    def __str__(self):
        return self.get_summary()

    def __repr__(self):
        return self.get_summary()

    def __eq__(self, other):
        if not isinstance(other, Thing):
            return False
        return thing_comparison.is_equal(self, other)
                    
    def __gt__(self, other):
        if not isinstance(other, Thing):
            return False
        return  thing_comparison.is_gt(self, other)

    def __lt__(self, other):
        if not isinstance(other, Thing):
            return False
        return  thing_comparison.is_lt(self, other)

    
    def __add__(self, other):
        if not isinstance(other, Thing):
            return False

        new_thing = Thing()
        for i in self._o:
            if i not in new_thing._o:
                new_thing._o.append(i)
            
        for i in other._o:
            if i not in new_thing._o:
                new_thing._o.append(i)
        return new_thing

    
    def __sub__(self, other):
        """Removes observations in other from self  
        """
        if not isinstance(other, Thing):
            return False
            
        t = Thing()
        for i in self._o:
            if i.k.startswith('@') or i not in other._o:
                t.add(i)
        return t


    def keys(self):
        """Returns all measuredProperty in ordered list
        """
        return sorted(list(set([x.measuredProperty for x in self._o])))
        
    
    def record_ref(self):
        """Return type and id in a dict
        """
        return {'@type': self.type, '@id': self.id}

    def record_refs(self):
        """Returns all possible record_ref (old data)
        """
        records = []
        types = [x.value for x in self.get('@type')]
        ids = [x.value for x in self.get('@id')]
        for type in types:
            for id in ids:
                record = {'@type': type, '@id': id}
                records.append(record)
        return records

    
    
    def get_record(self, in_json=False):
        """Returns thing as dict with all nested things as dict
        """

        record = self.dump(True)
        if in_json:
            return kr.json.dumps(record)
        else:
            return record

    @property
    def record(self):
        """Returns thing as dict with all nested things as dict
        """
        return self.dump()

    @record.setter
    def record(self, value):
        """Returns thing as dict with all nested things as dict
        """
        record = kr.json.loads(value)
        return self.load(record)

    
    def get_summary(self):
        """Return string with summary info on the thing
        """
        return thing_output.get_summary_string(self.type, self.id, self._o)
        
    @property
    def summary(self):
        """Return string with summary info on the thing
        """
        return self.get_summary()

    def get_summary_record(self):
        """Returns summary record based on type
        """
        return thing_summary_record.get(self.dump(False))

    @property
    def summary_record(self):
        """Return summary record based on type
        """
        return self.get_summary_record()
    
    def get(self, parameter=None):
        """Retrieves all observations for a given parameter
            Parameters:
                    parameter (str): The name of the attribute    
            Returns:
                    Observations (Observation): The observations for this attribute
        """
        obs = [o for o in self._o if o.k == parameter] if parameter else [o for o in self._o]
        obs.sort(reverse=True)
        return obs

    
    def get_best(self, parameter):
        """Returns best observation for given parameter
        """
        obs = self.get(parameter)
        return obs[0] if len(obs) > 0 else None
    
    
    def set(self, parameter, value, credibility=None, date=None):
        """Adds an observation with parameter and value.
        Uses default metadata if c and d not provided.
        """
        # Handle lists
        if isinstance(value, list):
            return all([self.set(parameter, x, credibility, date) for x in value])
            
        # Handle dict
        if isinstance(value, dict) and '@value' in value.keys():
            v = value.get('@value', [])
            v = v if isinstance(v, list) else [v]
            for i in v:
                o = Observation(parameter, value, self.metadata.metadata)
                o.load(value)
                o.value = i
                
                if isinstance(o.value, dict) and '@type' in o.value.keys():
                    t = Thing()
                    t.load(o.value)
                    o.value = t
                    self.add_related_thing(t)
            
                self.add(o)
            return
            
        if isinstance(value, dict) and '@type' in value.keys():
        
            t = Thing()
            t.metadata.metadata = self.metadata.metadata

            t.load(value)
            # Add to related if not basic type
            if t.type not in self._basic_types:
                self.add_related_thing(t)
            value = t
        
        
        
        # Handle things
        if isinstance(value, Thing):
            self.add_related_thing(value)
            #value = value.record_ref()
        
        # Convert to observation
        o = Observation(parameter, value, self.metadata.metadata)
        if credibility:
            o.c = credibility
        if date:
            o.d = date
                
        self.add(o)

        # if not valid, add valid version
        if not o.validValue:
            norm_o = o.get_normalized_observation()
            if norm_o.validValue:
                self.add(norm_o)

        
        return True

    def add(self, observation):
        """Add an observation to the thing
            Parameters:
                    observation (Observation): An observation to add    
            Returns:
                    result (bool): True if succeeded
        """
        # Handle error
        if not observation:
            return False
            
        # Handles list
        if isinstance(observation, list):
            return all([self.add(x) for x in observation])
            
        # If things, copies other thing observations into this one
        if isinstance(observation, Thing):
            self.add(observation.observations)
            return True

        # Handles observation
        if isinstance(observation, Observation):
            if observation not in self._o:
                self._o.append(observation)
            return True

        return True


    
    """Related things
    """

    def add_related_thing(self, t):
        """Add a related thing to the list
        """
        if not t:
            return False

        # Handles list
        if isinstance(t, list):
            return all([self.add_related_thing(x) for x in t])
        
        # Add sub things
        for i in t.related_things():
            self.add_related_thing(i)

        # Add to itself if equal
        if t == self:
            self.add(t)

        else:
            self._things.append(t)
        
        return True
        
    def related_things(self):
        """Return all nested things excluding itself
        """

        things = []
        for i in self._things:
            things += i.things()
        things = things_manipulation.deduplicate(things)
        things.sort()
        return things
        
    def things(self):
        """Return all the nested things, including itself
        """
        things = [self] + self.related_things()
        things = things_manipulation.deduplicate(things)
        things.sort()
        
        return things
    
    def deduplicate_things(self):
        """Deduplicate all related_things
        """
        # Todo: delete this method
        self._related_things = things_manipulation.deduplicate(self.related_things)
        return

    """ ID management
    """

    def harmonize_ids(self):
        """Verify all the ids for a related things
        Ensure that if a thing changed id, all references are changed as well
        """

        things_manipulation.harmonize_ids(self.things())
        return
        
        
    
    """Methods to load and dump records as dict (json)
    """

    def load(self, record):
        """Load dict (json) into thing.
        Uses values in @metadata else uses defaults 
        """

        # Deal with json
        if isinstance(record, str):
            record = kr.json.loads(record)

        # Deal with list of 1
        if isinstance(record, list):
            if len(record) == 1:
                record = record[0]

        if not record:
            return False

        # Convert from dot notation (if required)
        record = thing_dot.from_dot(record)

        
        if '@metadata' in record.keys():
            self.metadata.load_metadata(record.get('@metadata', {}))
        for k, v in record.items():
            
            if not k == '@metadata':
                self.set(k, v)
           
        return True


    def dump(self, retrieve_all=True):
        """Dump the content into a dict record
        if retrieve_all, returns all values, not just the best
        """

        # Harmonize ids across all things
        self.harmonize_ids()

        # Get list of attributes
        record = {}
        attr = list(set([o.k for o in self._o]))
        attr.sort()

        # Retrieve values for attributes
        for k in attr:
            if retrieve_all:
                record[k] = []
                values = [o.v for o in self.get(k)]
    
                for v in values:
                    if isinstance(v, Thing):
                        v = v.dump()
                    if v not in record[k]:
                        record[k].append(v)
            else:
                record[k] = self.get_best(k).v
                if isinstance(record[k], Thing):
                    record[k] = record[k].dump(retrieve_all)
        
        return record

    def dump_observations(self):
        """Returns observations as dict
        """
        records = []
        for i in self.observations:
            records.append(i.dump())
        return records

    def get_json(self):
        """Return a json record of thing without metadata
        """
        return kr.json.dumps(self.dump())

    def load_json(self, value):
        """Load json content into object
        """
        record = kr.json.loads(value)
        return self.load(record)
        
    def json(self):
        """Return a json record of thing without metadata
            same as get_json()
        """
        return self.get_json()

    

    def jsons(self):
        """Return a json record of all things without metadata
        """
        records = [x.dump() for x in self.things()]
        
        return kr.json.dumps(records)
    
    """Methods to load / dump records in database format
    """
    
    def _db_load(self, record):
        """Load record from database format (with metadata)
        """
            
        if isinstance(record, list) and len(record)==1:
            record = record[0]
        if not record:
            return False
        
        observations = record.get('observations',[])
        for i in observations:
            o = Observation()
            o.load(i)
            self.add(o)
        return True
    
    def _db_dump(self, new_only=False):
        """Dump records in database format (with metadata)
        """
        # Harmonize ids across all things
        self.harmonize_ids()

        records = []

        for i in self.things():
            # Skip for basic types
            if i.type in self._basic_types:
                continue
            
            # Export self
            record = {
                '@type': self.type,
                '@id': self.id,
                'observations': []
            }

            record['observations'] = [x.dump() for x in sorted(self._o) if x._db or not new_only]

            records.append(record)
        
        return records


    def db_json(self):
        """
        """
        return kr.json.dumps(self._db_dump())


    """
    API
    """

    def api_url(self, url):
        """Sets env var for api url
        """
        os.environ["API_URL"] = url
        return
        
    def api_get(self):
        API_URL = os.getenv('API_URL')
        content = thing_api.get(API_URL, self.record_type, self.record_id)
        if not content or content is False:
            return False
        record = kr.json.loads(content)
        return self._db_load(record)

    def api_get_all(self):
        """Gets record and sub records
        """   
        self.api_get()
        tasks = []
        for i in self.related_things():
            tasks.append(asyncio.run(i.api_get()))

        results = asyncio.gather(*tasks)
        return True
            
    
    def api_post(self):
        API_URL = os.getenv('API_URL')
        record = self._db_dump()
        content = kr.json.dumps(record)
        return thing_api.post(API_URL, content)

    def api_delete(self):
        API_URL = os.getenv('API_URL')
        return thing_api.delete(API_URL, self.record_type, self.record_id)

    async def api_get_async(self):
        API_URL = os.getenv('API_URL')
        content = await thing_api.get_async(API_URL, self.record_type, self.record_id)
        if not content or content is False:
            return False
        record = kr.json.loads(content)
        return self._db_load(record)

    async def api_post_async(self):
        API_URL = os.getenv('API_URL')
        record = self._db_dump()
        content = kr.json.dumps(record)
        return await thing_api.post_async(API_URL, content)
    
    async def api_delete_async(self):
        API_URL = os.getenv('API_URL')
        return await thing_api.delete_async(API_URL, self.record_type, self.record_id)



    
    """Shortcuts
    """
    @property
    def metadata(self):
        return self._metadata

    @metadata.setter
    def metadata(self, value):
        self._metadata.load_metadata(value)
        return
        
    @property
    def observations(self):
        obs = []
        for i in self.keys():
            obs += self.get(i)
        return obs

    
    
    @property
    def type(self):
        o = self.get_best('@type')
        value = o.value if o else None
        if value and isinstance(value, str):
            value = value.replace('schema:', '')
        return value

    @type.setter
    def type(self, value:str):
        value = value.replace('schema:', '')
        self.set('@type', value)
        return

    @property
    def record_type(self):
        return self.type

    @record_type.setter
    def record_type(self, value):
        self.type = value
        return True

    
    @property
    def id(self):
        o = self.get_best('@id')
        if o and o.validValue:
            return o.value

        # Create new if None
        if not o or not o.value:
            o = Observation('@id', str(uuid.uuid4()))
            o.observationCredibility = 0
            self.add(o)

        # Todo: handle cases where id is invalid and needs to be replaced (add source object to uuid)
        return o.value if o else None

    @id.setter
    def id(self, value):
        self.set('@id', value)
        return

    @property
    def record_id(self):
        return self.id

    @record_id.setter
    def record_id(self, value):
        self.id = value
        return True
    
    @property
    def name(self):
        o = self.get_best('name')
        return o.value if o else None

    @name.setter
    def name(self, value):
        self.set('name', value)
        return

    @property
    def description(self):
        o = self.get_best('description')
        return o.value if o else None

    @description.setter
    def description(self, value):
        self.set('description', value)
        return
    
    @property
    def url(self):
        o = self.get_best('url')
        return o.value if o else None

    @url.setter
    def url(self, value):
        self.set('url', value)
        return

    @property
    def email(self):
        o = self.get_best('email')
        return o.value if o else None

    @email.setter
    def email(self, value):
        self.set('email', value)
        return

    @property
    def status(self):
        o = self.get_best('actionStatus')
        return o.value if o else None

    @status.setter
    def status(self, value):
        self.set('actionStatus', value)
        return

    @property
    def sameAs(self):
        values = [o.value for o in self.get('sameAs')]
        return values
        
    @sameAs.setter
    def sameAs(self, value):
        self.set('sameAs', value)



    @property
    def first_name(self):
        o = self.get_best('givenName')
        return o.value if o else None

    @first_name.setter
    def first_name(self, value):
        self.set('givenName', value)

    @property
    def last_name(self):
        o = self.get_best('familyName')
        return o.value if o else None

    @last_name.setter
    def last_name(self, value):
        self.set('familyName', value)

    @property
    def street(self):
        o = self.get_best('streetAddress')
        return o.value if o else None
        
    @street.setter
    def street(self, value):
        self.set('streetAddress', value)


    @property
    def city(self):
        o = self.get_best('addressLocality')
        return o.value if o else None
        
        
    @city.setter
    def city(self, value):
        self.set('addressLocality', value)

    @property
    def state(self):
        o = self.get_best('addressRegion')
        return o.value if o else None

        
    @state.setter
    def state(self, value):
        self.set('addressRegion', value)

    @property
    def province(self):
        o = self.get_best('addressRegion')
        return o.value if o else None

    @province.setter
    def province(self, value):
        self.set('addressRegion', value)

    
    @property
    def country(self):
        o = self.get_best('addressCountry')
        return o.value if o else None
        
    @country.setter
    def country(self, value):
        self.set('addressCountry', value)

    @property
    def postal_code(self):
        o = self.get_best('postalCode')
        return o.value if o else None
        
    @postal_code.setter
    def postal_code(self, value):
        self.set('postalCode', value)

    @property
    def potential_action(self):
        o = self.get_best('potentialAction')
        return o.value if o else None

    @potential_action.setter
    def potential_action(self, value):
        self.set('potentialAction', value)

    @property
    def potential_actions(self):
        obs = self.get('potentialAction')
        values = [o.value for o in obs]
        return values


    

    
    """
    Action shortcuts
    """

    def get_duration(self):
        """Returns duration between startTime and endTime
            Returns 0 if no startTime, and duration until now if no endTime
        """
        start = self.get_best('startTime')
        end = self.get_best('endTime')
        if not start:
            return 0
        elif not end:
            return (datetime.datetime.now() - start.value).total_seconds()
        else:
            return (end.value - start.value).total_seconds()

    @property
    def duration(self):
        """Returns duration between startTime and endTime
            Returns 0 if no startTime, and duration until now if no endTime
        """
        return self.get_duration()

    @property
    def is_potential(self):
        """Returns true if actionStatus == potentialActionStatus"""
        status = self.get_best('actionStatus')
        if not status:
            return False
        return True if status.value == 'potentialActionStatus' else False
    
    @property
    def is_new(self):
        return self.is_potential
    
    @property
    def is_active(self):
        """Returns true if actionStatus == activeActionStatus"""
        status = self.get_best('actionStatus')
        if not status:
            return False
        return True if status.value == 'activeActionStatus' else False
    
    @property
    def is_open(self):
        """Returns true if actionStatus == activeActionStatus"""
        return self.is_active
        
    @property
    def is_completed(self):
        """Returns true if actionStatus == completedActionStatus"""
        status = self.get_best('actionStatus')
        if not status:
            return False
        return True if status.value == 'completedActionStatus' else False

    @property
    def is_failed(self):
        """Returns true if actionStatus == failedActionStatus"""
        status = self.get_best('actionStatus')
        if not status:
            return False
        return True if status.value == 'failedActionStatus' else False
    
    @property
    def is_error(self):
        """Returns true if actionStatus == failedActionStatus"""
        return self.is_failed

    def set_status_new(self):
        """Sets actionStatus to potential"""
        self.set('actionStatus', 'potentialActionStatus')
        return True
        
    def set_status_active(self):
        """Sets actionStatus to active"""
        self.set('startTime', datetime.datetime.now())
        self.set('actionStatus', 'activeActionStatus')
        return True
        
    def set_status_failed(self, error_message=None):
        """Sets actionStatus to failed"""
        if error_message:
            self.set('error', error_message)
        self.set('endTime', datetime.datetime.now())
        self.set('actionStatus', 'failedActionStatus')
        return True
        
    def set_status_completed(self):
        """Sets actionStatus to completed"""
        self.set('endTime', datetime.datetime.now())
        self.set('actionStatus', 'completedActionStatus')
        return True
    def set_status_closed(self):
        """Sets actionStatus to completed"""
        return self.set_status_completed()
    """
    
    """
    def get_thumbnail(self):
        # Returns url of thumbnail
        url = None

        # Get thumbnail
        if not url:
            thumbnail = self.get_best('thumbnailUrl')
            if thumbnail:
                url = thumbnail.value
                
        # Get image
        if not url:
            image = self.get_best('image')
            if image: 
                url = image.value.get_image()

        # Get content
        if not url:
            content = self.get_best('contentUrl')
            if content:
                url = content.value
        return url

    def get_image(self):
        # Return url of image

        url = None

        # Get image
        image = self.get_best('image')
        if image: 
            url = image.value.get_image()

        # Get content
        if not url:
            content = self.get_best('contentUrl')
            if content:
                url = content.value

        # Get thumbnail
        if not url:
            thumbnail = self.get_best('thumbnailUrl')
            if thumbnail:
                url = thumbnail.value

        return url

    def get_name(self):
        # Returns Name

        return thing_names.get(self.dump(False))

    
    def record_type_id(self):
        return f'/{self.type}/{self.id}'


    """
    Helpers to help with tests
    """
    def get_test_record(self, record_type='test', record_id='test_01'):
        """Return a test record
        """

        record = {
            '@type': record_type,
            '@id': record_id,
            'name': f'name_{record_id}',
            'url': f'https://www.{record_id}.com',
            'description': f'Description {record_id}',
            'image':{
                '@type': 'imageObject',
                '@id': f'image_{record_id}',
                'url': f'https://www.image.{record_id}.com'
            },
            'identifier': [
                {
                    '@type': 'propertyValue', 
                    '@id': f'sub_0_{record_id}',
                    'name': 'property_0',
                    'value': f'property_0_sub_0_{record_id}'
                },
                {
                    '@type': 'propertyValue', 
                    '@id': f'sub_1_{record_id}',
                    'name': 'property_1',
                    'value': f'property_1_sub_1_{record_id}'
                }
            ]
        }
        return record

    def load_test_record(self, record_type='test', record_id='test_01'):
        """Load test record
        """
        record = self.get_test_record(record_type, record_id)
        self.load(record)
        return True
    
    
        