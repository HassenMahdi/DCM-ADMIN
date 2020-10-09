from app.db.connection import mongo
from app.db.document import Document


class Mapping(Document):

    __TABLE__ = "mappings"

    domain_id = None
    mappings = None

    @staticmethod
    def is_using_field(field_name, domain_id):
        return True if Mapping().db().find_one({"rules.target": field_name, 'domainId': domain_id}) else False

