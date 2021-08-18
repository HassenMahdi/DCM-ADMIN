from flask import request
from flask_restplus import Resource

from ..service.rsu_service import import_rsu_data_from_file, get_all_rsu_data, update_rsu_data_from_file, compare_rsu_data
from ..util.decorator import token_required
from ..util.dto import RsuDto

api = RsuDto.api
rsu_data = RsuDto.rsu_data
rsu_with_header = RsuDto.rsu_with_header


@api.route('/')
class RsuDataList(Resource):
    @token_required
    @api.doc('Get All RSU Composition')
    @api.marshal_list_with(rsu_with_header)
    def get(self):
        return get_all_rsu_data()


@api.route('/import')
class RsuDataImport(Resource):
    @api.doc('import rsu composition data')
    @api.response(201, 'RSU composition successfully imported.')
    @token_required
    def post(self):
        # get the file data
        return import_rsu_data_from_file(request)


@api.route('/update')
class RsuDataUpdate(Resource):
    @api.doc('update rsu composition data')
    @api.response(201, 'Ref Data successfully updated.')
    @token_required
    def post(self):
        # get the file data
        return update_rsu_data_from_file(request)


@api.route('/compare')
class RefData(Resource):
    @api.doc('compare data')
    @api.response(201, 'RSU comparison successfully imported.')
    @token_required
    def post(self):
        # get the file data
        return compare_rsu_data(request.files['file'])
