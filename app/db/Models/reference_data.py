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
    created_on=None
    modified_on= None
    properties = None




