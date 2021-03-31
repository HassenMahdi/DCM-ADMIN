from flask import request, jsonify
from flask_restplus import Resource

from ..service.dictionary_service import *
from ..util.decorator import token_required
from ..util.dto import DictionaryDto

api = DictionaryDto.api
dto = DictionaryDto.dictionary


@api.route('/')
class DictionariesList(Resource):
    """
        Dictionary Resource
    """
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

    @api.doc('delete Dictionary')
    @api.response(201, 'Dictionary successfully deleted.')
    @api.marshal_with(dto)
    def delete(self):
        post_data = request.json
        return delete_dcitionary(data=post_data)
