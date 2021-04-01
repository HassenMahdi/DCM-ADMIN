from flask import request, jsonify
from flask_restplus import Resource

from ..service.dictionary_service import *
from ..util.decorator import token_required
from ..util.dto import DictionaryDto

api = DictionaryDto.api
dto = DictionaryDto.dictionary


@api.route('/')
class DictionariesList(Resource):

    @api.doc('Get All Dictionaries')
    @api.marshal_list_with(dto)
    @token_required
    def get(self):
        return get_all_dictionaries()

    @api.doc('Create/Update Dictionaries')
    @api.response(201, 'Dictionary successfully created/updated.')
    @token_required
    @api.marshal_with(dto)
    def post(self):
        post_data = request.json
        return save_dictionary(data=post_data)


@api.route('/<dict_id>')
class Dictionaries(Resource):

    @api.doc('delete Dictionary')
    @api.response(201, 'Dictionary successfully deleted.')
    @api.marshal_with(dto)
    def delete(self, dict_id):
        return delete_dcitionary(dict_id)

    @api.doc('Get Dictionary by Id')
    @api.marshal_with(dto)
    def get(self, dict_id):
        return get_dictionary(dict_id)
