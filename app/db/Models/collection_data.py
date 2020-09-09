from app.db.connection import mongo
from app.db.document import Document


class CollectionData(Document):

    __TABLE__ = "collection_data"

    def db(self, **kwargs):
        domain_id = kwargs['domain_id']
        return mongo.db[f"{domain_id}.{self.__TABLE__}"]

