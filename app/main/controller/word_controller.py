from flask import request, jsonify
from flask_restplus import Resource

from ..service.category_service import *
from ..util.decorator import token_required
from ..util.dto import WordDto

api = WordDto.api
dto = WordDto.category


@api.route('/')
class Word(Resource):
    @api.doc('Create/Update words')
    @api.response(201, 'Word successfully created/updated.')
    @token_required
    @api.marshal_with(dto)
    def post(self):
        post_data = request.json
        return save_word(data=post_data)


@api.route('/<dict_id>')
class WordList(Resource):

    @api.doc('Get All words of dict')
    @api.marshal_list_with(dto)
    @token_required
    def get(self,dict_id):
        return get_all_words_by_dict_id(dict_id)


@api.route('/<word_id>')
class Words(Resource):

    @api.doc('Delete Word by id')
    @api.response(201, 'Word successfully deleted.')
    @api.marshal_with(dto)
    def delete(self, word_id):
        return delete_word(word_id)

    @api.doc('Get Word by Id')
    @api.marshal_with(dto)
    def get(self, word_id):
        return get_word(word_id)
