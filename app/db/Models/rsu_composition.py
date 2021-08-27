from app.db.document import Document


class RsuComposition(Document):
    __TABLE__ = "rsu"

    def createIndex(self):
        self.db().create_index({"location": "2dsphere"})

    created_on = None
    modified_on = None
    composition = None

