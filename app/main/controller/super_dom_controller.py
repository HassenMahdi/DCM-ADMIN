from flask import request
from flask_restplus import Resource

from ..service.auth_helper import Auth
from ..service.super_dom_service import get_all_super_domains, save_super_domain, delete_super_domain, \
    get_domains_hierarchy
from ..util.decorator import token_required
from ..util.dto import DomainDto, SuperDomainDto

api = SuperDomainDto.api
dto = SuperDomainDto.super_domain


@api.route('/')
class SuperDomains(Resource):
    """
        Domain Resource
    """
    @token_required
    @api.doc('Get All Super Domains')
    @api.marshal_list_with(dto)
    def get(self):
        user_rights, status = Auth.get_logged_in_user_rights(request)
        return get_all_super_domains(user_rights)

    @token_required
    @api.doc('Create/Update Super Domains')
    @api.response(201, 'Super Domain successfully created/updated.')
    # @api.marshal_with(dto, code=201)
    def post(self):
        # get the post data
        post_data = request.json
        return save_super_domain(data=post_data)

    @token_required
    @api.doc('delete super Domains')
    @api.response(201, 'Super Domain successfully deleted.')
    @api.marshal_with(dto)
    def delete(self):
        # get the post data
        post_data = request.json
        return delete_super_domain(data=post_data)


@api.route('/hierarchy')
class DomainsHierarchy(Resource):
    """
        Domain Resource
    """
    @token_required
    @api.doc('Get Domains Hierarchy')
    @api.marshal_list_with(dto)
    def get(self):
        user_rights, status = Auth.get_logged_in_user_rights(request)
        return get_domains_hierarchy(user_rights)

