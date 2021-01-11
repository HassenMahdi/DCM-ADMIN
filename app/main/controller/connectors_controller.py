from flask import request
from flask_restplus import Resource

from ..service.connectors_service import get_all_connectors, save_connector, delete_connector
from ..util.decorator import token_required
from ..util.dto import ConnectorsDto

api = ConnectorsDto.api
dto = ConnectorsDto.dto

@api.route('/')
class ConnectorsList(Resource):
    # @token_required
    @api.doc('Get All Connectors')
    @api.marshal_list_with(dto)
    def get(self):
        return get_all_connectors()

    # @token_required
    @api.doc('Save Connector')
    def post(self):
        post_data = request.json
        return save_connector(post_data)


@api.route('/<cn_id>')
class Connectors(Resource):
    # @token_required
    @api.doc('delete')
    def delete(self,cn_id):
        return delete_connector(cn_id)

