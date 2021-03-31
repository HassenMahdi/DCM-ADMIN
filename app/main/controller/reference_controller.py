from flask import request
from flask_restplus import Resource, reqparse

from ..dto.dto_fields import DTOFields
from ..service.fields_service import get_all_fields, save_field, delete_field, fields_from_file, get_simple
from ..service.reference_service import save_ref_type, get_all_ref_types, delete_ref_type, get_all_ref_data, \
    save_ref_data, delete_ref_data, get_ref_type, import_ref_data_from_file, share_ref_type, update_ref_data_from_file, \
    download_ref_data_from_file
from ..util.decorator import token_required
from ..util.dto import FieldsDto, ReferenceTypeDto

api = ReferenceTypeDto.api
ref_type = ReferenceTypeDto.ref_type
ref_data = ReferenceTypeDto.ref_data


# REF TYPES
@api.route('/type')
class RefTypeList(Resource):
    """
        Domain Resource
    """
    # @token_required
    @api.doc('Get All Domain Reference DataTypes')
    @api.marshal_list_with(ref_type)
    def get(self):
        parser = reqparse.RequestParser()
        parser.add_argument('domain_id', location='args')
        args = parser.parse_args()
        domain_id = args.get("domain_id", None)
        return get_all_ref_types(domain_id)

    @api.doc('Create/Update Reference Data')
    @api.response(201, 'Field successfully created/updated.')
    @api.expect(ref_type, validate=True)
    # @token_required
    def post(self):
        data = request.json
        return save_ref_type(data)


@api.route('/type/<ref_type_id>')
@api.param('ref_type_id', 'Domain ID')
class RefType(Resource):
    @api.doc('delete field')
    @api.response(201, 'field successfully deleted.')
    # @api.expect(ref_type, validate=True)
    # @api.marshal_with(ref_type)
    @token_required
    def delete(self, ref_type_id):
        return delete_ref_type(ref_type_id)

    # @token_required
    @api.doc('Get Ref Type')
    @api.marshal_with(ref_type)
    def get(self, ref_type_id):
        return get_ref_type(ref_type_id)


@api.route('/type/<ref_type_id>/share')
@api.param('ref_type_id', 'Domain ID')
class RefTypeShare(Resource):
    @api.doc('delete field')
    @api.response(201, 'Ref Type Shared.')
    @token_required
    def post(self, ref_type_id):
        domain_ids = request.json.get('domain_ids')
        return share_ref_type(ref_type_id, domain_ids)


# REF DATA
@api.route('/type/<ref_type_id>/data')
@api.param('ref_type_id', 'Ref Type Id')
class RefDataList(Resource):
    @token_required
    @api.doc('Get All Domain Reference DataTypes')
    @api.marshal_list_with(ref_data)
    def get(self, ref_type_id):
        return get_all_ref_data(ref_type_id)

    @api.doc('Create/Update Domain Fields')
    @api.response(201, 'Field successfully created/updated.')
    @api.expect(ref_data, validate=True)
    # @api.marshal_with(ref_data)
    @token_required
    def post(self, ref_type_id):
        data = request.json
        return save_ref_data(data)


@api.route('/data/<ref_id>')
@api.param('ref_id', 'Domain ID')
class RefData(Resource):
    @api.doc('delete field')
    @api.response(201, 'field successfully deleted.')
    # @api.expect(ref_data, validate=True)
    @api.marshal_with(ref_data)
    @token_required
    def delete(self, ref_id):
        return delete_ref_data(ref_id)


@api.route('/type/<ref_type_id>/import')
@api.param('ref_type_id', 'Domain ID')
class RefData(Resource):
    @api.doc('import ref')
    @api.response(201, 'Ref Data successfully imported.')
    @token_required
    def post(self, ref_type_id):
        # get the file data
        return import_ref_data_from_file(request.files['file'], ref_type_id)

@api.route('/type/<ref_type_id>/update')
@api.param('ref_type_id', 'Domain ID')
class RefDataUpdate(Resource):
    @api.doc('update ref')
    @api.response(201, 'Ref Data successfully updated.')
    @token_required
    def post(self, ref_type_id):
        # get the file data
        return update_ref_data_from_file(request.files['file'], ref_type_id)


@api.route('/type/<ref_type_id>/download')
@api.param('ref_type_id', 'Domain ID')
class RefDataDownload(Resource):
    @api.doc('download ref')
    @api.response(201, 'Ref Data successfully downloaded.')
    @token_required
    def post(self, ref_type_id):
        # get the file data
        return download_ref_data_from_file(ref_type_id)
