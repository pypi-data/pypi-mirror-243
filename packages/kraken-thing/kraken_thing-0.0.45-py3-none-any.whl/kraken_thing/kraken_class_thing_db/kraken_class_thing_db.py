
from kraken_thing.kraken_db.class_kraken_db import Kraken_db


class Kraken_thing_db:

    def __init__(self, thing):

        self._thing = thing

    
    def db_get(self, record_type, record_id):
        #
        db = Kraken_db()
        records = db.get(record_type, record_id)
        record = records[0] if len(records) > 0 else None
        self._thing._db_load(record)
        return

    def db_post(self):
        #
        db = Kraken_db()
        db.post(self._thing._db_dump())
        return