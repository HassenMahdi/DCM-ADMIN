from flask import request
from flask_restplus import Resource

from ..dto.dto_fields import DTOFields
from ..service.fields_service import get_all_fields, save_field, delete_field, fields_from_file, get_simple
from ..util.decorator import token_required
from ..util.dto import FieldsDto

api = FieldsDto.api
dto = FieldsDto.field


@api.route('/<domain_id>/fields')
@api.param('domain_id', 'Domain ID')
class Fields(Resource):
    """
        Domain Resource
    """
    @token_required
    @api.doc('Get All Domains')
    @api.marshal_list_with(dto)
    def get(self, domain_id):
        return [DTOFields.from_dao_to_dto(f, domain_id) for f in get_all_fields(domain_id)]

    @api.doc('Create/Update Domain Fields')
    @api.response(201, 'Field successfully created/updated.')
    @api.expect(dto, validate=True)
    # @api.marshal_with(dto)
    @token_required
    def post(self, domain_id):
        # get the post data
        # post_data = request.json
        post_data = DTOFields.from_dto_dict_to_dao_dict(request.json)
        return save_field(data=post_data, domain_id = domain_id)

    @api.doc('delete field')
    @api.response(201, 'field successfully deleted.')
    @api.expect(dto, validate=True)
    # @api.marshal_with(dto)
    @token_required
    def delete(self, domain_id):
        # get the post data
        # post_data = request.json
        post_data = DTOFields.from_dto_dict_to_dao_dict(request.json)
        return delete_field(data=post_data, domain_id = domain_id)


@api.route('/<domain_id>/fields/file')
@api.param('domain_id', 'Domain ID')
class FieldsFile(Resource):

    @token_required
    @api.doc('Create/Update Domain Fields')
    def post(self, domain_id):
        # get the file data
        return fields_from_file(request.files['file'], domain_id)


@api.route('/<domain_id>/fields/simple')
@api.param('domain_id', 'Domain ID')
class FieldsFile(Resource):

    @token_required
    @api.doc('Get simple Domain Fields')
    def get(self, domain_id):
        # get the file data
        return get_simple(domain_id)