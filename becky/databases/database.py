import shelve
import time

class ShelveDatabase:

    def __init__(self, path, identifier=None):
        self.path = path
        self.identifier = identifier
        self.retry_count = 10


    def get_backup_db(self, backup_name):
        """
        Opens a DB connection.
        Has a hacky retry attempt if the db opening fails (resource busy etc.)
        """
        for i in range(0, self.retry_count):
            try:
                db = ShelveDatabase(self.path, backup_name)
                return db
            except:
                time.sleep(2)
        raise ValueError

    def _open_db(self):
        db = shelve.open(self.path, writeback=True)
        return db

    def add(self, key, value):
        data = self.get(key)
        data = data + value
        self.save(key, data)

    def save(self, key, value):
        db = self._open_db()
        if self.identifier:
            data = db.get(self.identifier)
            data[key] = value
            db[self.identifier] = data
        else:
            db[key] = value
        db.close()

    def get(self, key):
        db = self._open_db()
        if self.identifier:
            data = db.get(self.identifier)
            data = data.get(key)
        else:
            data = db.get(key, None)
        db.close()
        return data

