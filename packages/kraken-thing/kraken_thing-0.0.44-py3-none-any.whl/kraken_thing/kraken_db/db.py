import pymongo
from pymongo import MongoClient
from dateutil import parser
from bson.objectid import ObjectId
import datetime
from pymongo import InsertOne, DeleteOne, ReplaceOne, UpdateOne, UpdateMany
import json
from kraken_thing.kraken_db import search_params
from kraken_thing.kraken_db import data


new_records = []    # Contains record_ref (or _id) of records newly created


def get_database(db_name):

   
    CONNECTION_STRING = "mongodb+srv://db_connect_01:Q7V6J9D74gRdzJOq@serverlessinstance0.dzqstz9.mongodb.net/?retryWrites=true&w=majority"

    client = MongoClient(CONNECTION_STRING)
    return client[db_name]


def create_index(db, container_name, keys_order, unique = False):
    """
    keys_order [('key', 'pymongo.ASCENDING')]
    """

    if not isinstance(keys_order, list):
        keys_order = [keys_order]

    collection = db[container_name]
    collection.create_index(keys_order, unique)


def init_db(db, container_name):
    """
    """

    # Base indexes
    index = [('record_type', pymongo.ASCENDING)]
    create_index(db, container_name, index, False)

    return
    
    index = [('record_id', pymongo.ASCENDING)]
    create_index(db, container_name, index, False)

    index = [('db_date_created', pymongo.ASCENDING)]
    create_index(db, container_name, index, False)
    
    index = [('db_date_created', pymongo.DESCENDING)]
    create_index(db, container_name, index, False)

    index = [('db_date_updated', pymongo.ASCENDING)]
    create_index(db, container_name, index, False)
    
    index = [('db_date_updated', pymongo.DESCENDING)]
    create_index(db, container_name, index, False)
    
    # Compound indexes
    index = [
        ('record_type', pymongo.ASCENDING), 
        ('record_id', pymongo.ASCENDING)
    ]
    create_index(db, container_name, index, True)

    index = [
        ('record_type', pymongo.ASCENDING), 
        ('record_id', pymongo.ASCENDING),
        ('db_date_created', pymongo.DESCENDING)
    ]
    create_index(db, container_name, index, False)

    index = [
        ('record_type', pymongo.ASCENDING), 
        ('db_date_created', pymongo.DESCENDING)
    ]
    create_index(db, container_name, index, False)
    
def list_record_types(db, container_name):

    result = db[container_name].aggregate(
        [
            { 
                '$sortByCount': '$record_type'
            }
        ]
    )


    records = []
    for i in result:
        record = {
            'record_type': i.get('_id', None),
            'count': i.get('count', None)
        }
        records.append(record)
    records = sorted(records, key=lambda d: d['record_type']) 

    
    return records


def get(db, container_name, record_type = None, record_id = None):
    """Get
    """
    collection_name = db[container_name]

    records = []
    
    if record_type and record_id:
        filter = {
            'type': record_type,
            'id': record_id
        }
        item = collection_name.find_one(filter)
        #print(record_type, record_id,item)
        records.append(item)

    else:
        records = list(collection_name.find())

    observations = []
    if records:
        observations = data.convert_db_record_to_observations(records)
    
    return observations

def get_many(db, container_name, records):
    """Get
    """

    collection_name = db[container_name]

    record_refs = []
    for record in records:
        record_type = record.get('@type', record.get('record_type', None))
        record_id = record.get('@id', record.get('record_id', None))
        if record_type and record_id:
            record_ref = '/'.join([record_type, record_id])
            record_refs.append(str(record_ref))

    filter = {
        '_id': { '$in': record_refs}
    }
    records = list(collection_name.find(filter))
    
    observations = []
    if records:
        observations = data.convert_db_record_to_observations(records)
    
    return observations



def search(db, container_name, filter = {}, order_by = None, order_direction = None, limit = 100, offset = 0):
    """Query_items list of key, value to search tuples
    

            https://pymongo.readthedocs.io/en/stable/api/pymongo/cursor.html#pymongo.cursor.Cursor.sort
        [
        ('field1', pymongo.ASCENDING),
        ('field2', pymongo.DESCENDING)])
    """

    if filter:
        filter = search_params.get(filter)

    if not offset:
        offset = 0

    #print(filter)
    
    collection_name = db[container_name]
    if order_by:

        if order_by == 'created_date':
            order_by = 'db_date_created'
        if not order_by:
            order_by = 'db_date_created'
        
        if not order_direction:
            order_direction = 'D'
        
        if order_direction.startswith('A') or order_direction.startswith('a') :
            #sort_params = [(order_by, 'pymongo.ASCENDING')]
            sort_params = [[order_by, 1]]
        else:
            #sort_params = [(order_by, 'pymongo.DESCENDING')]
            sort_params = [[order_by, -1]]
        items = collection_name.find(filter).sort(sort_params)
    else:
        items = collection_name.find(filter)

    if offset:

        try:
            offset=int(offset)
        except:
            offset=0

        if offset < 0:
            offset = 0
        items = items.skip(offset)

        
    if limit:
        try:
            limit=int(limit)
        except:
            limit=100
        
        
        items = items.limit(limit)
    
    records = []
    for i in items:
        records.append(i)

    
    observations = data.convert_db_record_to_observations(records)
    
    return observations


def count(db, container_name, filter = {}):
    collection_name = db[container_name]
    no_items = collection_name.count_documents(filter)
    return no_items


def post(db, container_name, items):
    """Post to database
    returns record_ref of new records
    """

    global new_records

    if not isinstance(items, list):
        items = [items]

    #items = data.convert_observations_to_db_record(items)
    

    # Build request
    requests = []
    for i in items:
        record_type = i.get('type', None)
        record_id = i.get('id', None)
        sameas = i.get('sameAs', i.get('record_id', None))
        record_ref = '/'.join([str(record_type), str(record_id)])
        observations = i.get('observations', [])

        for o in observations:
            hash = o.get('hash', None)
            rec = {
                '_id': record_ref,
                'type': record_type, 
                'id': record_id,
                #'hash': {"$ne": hash}
            }
            rec_value = {
            '$setOnInsert': {'db_date_created': datetime.datetime.now()},
            '$set': {'db_date_updated': datetime.datetime.now()},
            '$addToSet': {
                'observations': o,
                'hash': hash
                },
           
            }
            requests.append(UpdateOne(rec, rec_value, upsert=True))
    
    # Execute requests                                     
    result = db[container_name].bulk_write(requests)

    # Identify and store new records and process
    for i in result.bulk_api_result.get('upserted', []):
        new_records.append(i.get('_id', None))
    
    return 

def get_new_records():
    """Retrieves list of new records and flush cache
    """
    global new_records

    records = []

    for i in new_records:
        try:
            record_type = i.split('/')[0]
            record_id = i.split('/')[1]
            record = {
                '@type': record_type,
                '@id': record_id
            }
            records.append(record)
        except:
            a=1

    #new_records = []
    return records