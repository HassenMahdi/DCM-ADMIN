import datetime

import jwt

from app.db.Models.black_list_tokem import BlacklistToken
from app.db.document import Document
from app.main import flask_bcrypt
from app.main.config import key


class User(Document):
    __TABLE__ = "users"

    email = None
    password_hash = None
    first_name = None
    last_name = None

    created_on = None
    modified_on = None

    admin = None
    roles = None

    @staticmethod
    def remove_domain_for_users(domain_id):
        User().db().update_many(
            {'roles.domain_id':domain_id},
            {'$pull': {'roles': { "domain_id": domain_id} } }
        )

    @staticmethod
    def decode_auth_token(auth_token):
        """
        Decodes the auth token
        :param auth_token:
        :return: integer|string
        """
        try:
            payload = jwt.decode(auth_token, key)
            is_blacklisted_token = BlacklistToken.check_blacklist(auth_token)
            if is_blacklisted_token:
                return 'Token blacklisted. Please log in again.'
            else:
                return payload['sub']
        except jwt.ExpiredSignatureError:
            return 'Signature expired. Please log in again.'
        except jwt.InvalidTokenError:
            return 'Invalid token. Please log in again.'

    def __repr__(self):
        return "<User '{} {}'>".format(self.first_name,self.last_name)


