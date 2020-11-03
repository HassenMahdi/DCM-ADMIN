import datetime

import jwt

from app.db.Models.black_list_tokem import BlacklistToken
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



