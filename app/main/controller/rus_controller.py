from flask import request
from flask_restplus import Resource

from ..service.rsu_service import import_rsu_data_from_file
from ..util.decorator import token_required
from ..util.dto import RsuDto

api = RsuDto.api


@api.route('/import')
class RefData(Resource):
    @api.doc('import ref')
    @api.response(201, 'RSU composition successfully imported.')
    @token_required
    def post(self):
        # get the file data
        return import_rsu_data_from_file(request.files['file'])
