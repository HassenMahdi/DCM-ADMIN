from flask import request
from flask_restplus import Resource

from app.main.service.auth_helper import Auth
from ..service.doms_service import get_all_domains, save_domain
from ..service.fields_service import get_all_fields, save_field
from ..util.dto import DomainDto, FieldsDto

api = FieldsDto.api
user_auth = FieldsDto.field


@api.route('/<domain_id>/fields')
@api.param('domain_id', 'Domain ID')
class Fields(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    @api.marshal_list_with(user_auth)
    def get(self, domain_id):
        return get_all_fields(domain_id)

    @api.doc('Create/Update Domain Fields')
    @api.response(201, 'Field successfully created/updated.')
    @api.expect(user_auth, validate=True)
    @api.marshal_with(user_auth)
    def post(self, domain_id):
        # get the post data
        post_data = request.json
        return save_field(data=post_data, domain_id = domain_id)