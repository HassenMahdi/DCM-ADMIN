from flask_restplus import Namespace, fields


class NullableString(fields.String):
    __schema_type__ = ['string', 'null']
    __schema_example__ = 'nullable string'

class UserDto:
    api = Namespace('user', description='user related operations')
    user = api.model('user', {
        'email': fields.String(required=True, description='user email address'),
        'username': fields.String(required=True, description='user username'),
        'password': fields.String(required=True, description='user password'),
        'public_id': fields.String(description='user Identifier')
    })


class AuthDto:
    api = Namespace('auth', description='authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email address'),
        'password': fields.String(required=True, description='The user password '),
    })


class DomainDto:
    api = Namespace('domain', description='us-er related operations')
    domain = api.model('domain', {
        'name': fields.String(required=True, description='user email address'),
        'identifier': NullableString(description='user username'),
        'description': fields.String(description='user username'),
        'id': NullableString(description='user password'),
        'created_on': fields.DateTime(description='user Identifier')
    })


class FieldsDto:
    api = Namespace('domain', description='domain specific fields')
    field = api.model('field', {
        'id': NullableString(description='user password'),
        'name': fields.String(description='user email address'),
        'label': fields.String(description='user username'),
        'description': NullableString(description='user username'),
        # 'category': fields.String(description='user username'),
        'type': fields.String(description='user username'),
        'mandatory': fields.Boolean(description='user username'),
        'editable': fields.Boolean(description='user username'),
        'created_on': fields.DateTime(description='user Identifier'),
        'rules': fields.List(fields.Raw, description='list of rules')
    })


class ChecksDto:
    api = Namespace('domain', description='domain specific checks')
    check = api.model('field', {
        'id': NullableString(description='user password'),
        'name': fields.String(description='user email address'),
        'label': fields.String(description='user username'),
        'description': NullableString(description='user username'),
        # 'category': fields.String(description='user username'),
        'type': fields.String(description='user username'),
        'mandatory': fields.Boolean(description='user username'),
        'editable': fields.Boolean(description='user username'),
        'created_on': fields.DateTime(description='user Identifier'),
        'rules': fields.List(fields.Raw, description='list of rules')
    })
