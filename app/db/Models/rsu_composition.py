from app.db.document import Document
import pymongo


class RsuComposition(Document):
    __TABLE__ = "rsu"

    def createIndex(self):
        self.db().create_index([("location", pymongo.GEOSPHERE)])

    created_on = None
    modified_on = None
    composition = None

