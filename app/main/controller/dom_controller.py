from flask import request, jsonify
from flask_restplus import Resource

from ..service.auth_helper import Auth
from ..service.doms_service import get_all_domains, save_domain, get_domains_by_super_id, delete_domain, \
    duplicate_domain, get_domains_grouped_by_super_domains, get_domain
from ..service.fields_service import duplicate_fields
from ..service.super_dom_service import get_super_dom
from ..util.decorator import token_required
from ..util.dto import DomainDto

api = DomainDto.api
dto = DomainDto.domain


@api.route('/')
class DomainsList(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    @api.marshal_list_with(dto)
    @token_required
    def get(self):
        return get_all_domains()

    @api.doc('Create/Update Domains')
    @api.response(201, 'Domain successfully created/updated.')
    @token_required
    # @api.marshal_with(dto)
    def post(self):
        # get the post data
        post_data = request.json
        return save_domain(data=post_data)

    @api.doc('Duplicate Domains')
    @api.response(201, 'Domain successfully duplicated.')
    @api.expect(dto, validate=True)
    @api.marshal_with(dto)
    @token_required
    def put(self):
        # get the post data
        post_data = request.json
        old_id = post_data['id']
        new_domain = duplicate_domain(data=post_data)
        new_id = new_domain.id
        duplicate_fields(old_id, new_id)
        return new_domain

    @api.doc('delete Domains')
    @api.response(201, 'Domain successfully deleted.')
    @token_required
    @api.marshal_with(dto)
    def delete(self):
        # get the post data
        post_data = request.json
        return delete_domain(data=post_data)


@api.route('/super/<super_id>')
class SuperDomains(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    @api.marshal_list_with(dto)
    @token_required
    def get(self, super_id):
        return get_domains_by_super_id(super_id)


@api.route('/<dom_id>/info')
class Domain(Resource):
    """
        Domain Resource
    """
    @api.doc('Get Domain Information')
    @token_required
    def get(self, dom_id):
        dom = get_domain(dom_id)
        super_dom = get_super_dom(dom.super_domain_id)
        return {
            "collection":{
                "name":dom.name,
                "id":dom.id
            },
            "domain":{
                "name":super_dom.name,
                "id":super_dom.id
            }
        }


@api.route('/<dom_id>')
class DomainDetails(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains')
    @api.marshal_with(dto)
    @token_required
    def get(self, dom_id):
        return get_domain(dom_id)

    @api.doc('delete Domains')
    @api.response(201, 'Domain successfully deleted.')
    @api.marshal_with(dto)
    @token_required
    def delete(self, dom_id):
        return delete_domain(data={id: dom_id})


@api.route('/all/super')
class SubDomainsGrouped(Resource):
    """
        Domain Resource
    """
    @api.doc('Get All Domains Grouped By Super Domains')
    @token_required
    def get(self):
        user_rights, status = Auth.get_logged_in_user_rights(request)
        res = {"resultat": get_domains_grouped_by_super_domains(user_rights)}
        return jsonify(res)