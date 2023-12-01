
from kraken_thing.kraken_db.class_kraken_db import Kraken_db


class Kraken_things_db:

    def __init__(self, things):

        self._things = things

    
    def get(self, filter=None, order_by=None, order_direction=None, limit=None, offset=None):
        #
        db = Kraken_db()
        records = db.search(filter, order_by, order_direction, limit, offset)
        self._things._db_load(records)
        return
    

    def post(self):
            # Posts things to db
            db = Kraken_db()
            new_records = db.post(self._things._db_dump())
            return new_records
    
