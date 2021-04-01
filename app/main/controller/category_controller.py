from flask import request, jsonify
from flask_restplus import Resource

from ..service.category_service import *
from ..util.decorator import token_required
from ..util.dto import CategoryDto

api = CategoryDto.api
dto = CategoryDto.category

@api.route('/<dict_id>')
class CategoryList(Resource):

    @api.doc('Get All Categories')
    @api.marshal_list_with(dto)
    @token_required
    def get(self,dict_id):
        return get_all_categories_by_dict_id(dict_id)

    @api.doc('Create/Update Categories')
    @api.response(201, 'Category successfully created/updated.')
    @token_required
    @api.marshal_with(dto)
    def post(self,dict_id):
        post_data = request.json
        return save_category(data=post_data)

@api.route('/<cat_id>')
class Dictionaries(Resource):

    @api.doc('delete Dictionary')
    @api.response(201, 'Dictionary successfully deleted.')
    @api.marshal_with(dto)
    def delete(self, cat_id):
        return delete_category(cat_id)

    @api.doc('Get Dictionary by Id')
    @api.marshal_with(dto)
    def get(self, cat_id):
        return get_category(cat_id)