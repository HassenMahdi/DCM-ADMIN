from app.db.connection import mongo
from app.db.document import Document


class TargetField(Document):

    __TABLE__ = "fields"

    def db(self, **kwargs):
        domain_id = kwargs['domain_id']
        return mongo.db[f"{domain_id}.{self.__TABLE__}"]

    name = None
    description = None
    label = None
    created_on = None
    modified_on = None
    type = None
    category = None
    rules = None
    editable = None
    mandatory = None
    ref_type_id = None

    def is_used(self, domain_id):
        if TargetField().db(domain_id=domain_id).find_one({'rules.property': self.name, '_id': {"$ne": self.id}}):
            return True

        return False
