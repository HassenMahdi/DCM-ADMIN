import datetime

import jwt

from app.db.Models.black_list_tokem import BlacklistToken
from app.db.Models.field import TargetField
from app.db.document import Document
from app.main import flask_bcrypt
from app.main.config import key


class ReferenceType(Document):
    __TABLE__ = "reference_types"

    label = None
    description = None
    properties = None
    domain_ids = None
    created_on = None
    modified_on = None
    shared = False

    parent_id = None
    version_label = None

    versions = None

    def is_used_in_domain(self, domain_id):
        return TargetField().db(domain_id=domain_id).find_one({'ref_type_id': self.id})



