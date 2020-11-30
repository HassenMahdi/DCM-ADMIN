import datetime

import jwt

from app.db.Models.black_list_tokem import BlacklistToken
from app.db.document import Document
from app.main import flask_bcrypt
from app.main.config import key


class ReferenceData(Document):
    __TABLE__ = "reference_data"

    code = None
    alias = None
    ref_type_id = None
    created_on = None
    modified_on = None
    properties = None

    def has_unique_code(self):
        return not self.db().find_one({"_id": {"$ne": self.id}, "code": self.code}, {"_id":1, "code": 1})

    def has_unique_alias(self):
        return not self.db().find_one({"_id": {"$ne": self.id}, "$or": [{"alias": a} for a in self.alias]}, {"_id": 1, "code": 1})





