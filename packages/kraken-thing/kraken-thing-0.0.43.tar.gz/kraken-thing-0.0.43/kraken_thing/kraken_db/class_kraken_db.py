from kraken_thing.kraken_db import db

class Kraken_db:

    def __init__(self, db_name='test_schema_01'):
        """
        """

        self.db_name = db_name
        self.db = db.get_database(self.db_name)
        self.container_name = 'schema_objects'
        #self.init()

    def init(self):
        """
        """
        db.init_db(self.db, self.container_name)


    def list_record_types(self):
        return db.list_record_types(self.db, self.container_name)

    
    def get(self, record_type = None, record_id = None):
        """
        """

        return db.get(self.db, self.container_name, record_type, record_id)

    def get_many(self, records):
        """
        """

        return db.get_many(self.db, self.container_name, records)


    def get_observations(self, filter = {}, order_by = None, order_direction =None, limit = 100, offset = 0):
        """
        """

        return db.search(self.db, self.container_name, filter, order_by, order_direction, limit, offset)
    
    def count(self, filter={}):
        """
        """
        return db.count(self.db, self.container_name, filter)


    def get_new_records(self):
        """
        """
        return db.get_new_records()


    
    def search(self, filter = {}, order_by = None, order_direction =None, limit = 100, offset = 0):
        """sort params lis tof tuples ()
        """
        return db.search(self.db, self.container_name, filter, order_by, order_direction, limit, offset)


    
    
    def post(self, items):
        """
        """

        return db.post(self.db, self.container_name, items)

    