import uuid
import datetime

from app.db.Models.collection_data import CollectionData
from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.super_domain import SuperDomain
from app.main.service.super_dom_service import get_user_query
from app.main.util.strings import camelCase, get_next_iteration


def get_domain(dom_id):
    return Domain(id=dom_id).load()


def save_domain(data):
    super_domain_id = data['super_domain_id']
    super_dom = SuperDomain(**{'id': super_domain_id}).load()

    if super_dom.id:
        dom = Domain(**data).load()
        if not dom.id:
            identifier = super_dom.id + '_' + camelCase(data['name'])
            max = get_next_iteration(
                Domain().db().find({'identifier': {'$regex': f"{identifier}(_[1-9]+)?"}}, {'identifier': 1})
            )

            if max > 0:
                identifier = f"{identifier}_{str(max)}"

            new_dom = Domain(
                **{**data, **{
                    'id': identifier,
                    'identifier': identifier,
                    'created_on': datetime.datetime.utcnow(),
                    'super_domain_id': super_domain_id

                }})
            #     CREATE NEW TABLES HERE
            dom = new_dom

        dom.name = data.get('name', None)
        dom.description = data.get('description', None)
        dom.classification = data.get('classification', None)
        dom.enableDF = data.get('enableDF', None)
        dom.modified_on = datetime.datetime.utcnow()

        if Domain().db().find_one({'_id': {'$ne': dom.id}, 'name': dom.name, 'super_domain_id': super_dom.id}):
            return {"status": 'fail', "message": 'Collection name already used in this Domain'}, 409

        dom.save()
    else:
        return {"status": "fail", "message": "No collection with provided ID found"}, 409

    return {"status": "success", "message": "Collection saved"}, 201


def delete_domain(data):
    super_domain_id = data['super_domain_id']
    super_dom = SuperDomain(**{'id':super_domain_id}).load()

    if super_dom.id:
        dom = Domain(**data).delete()
        TargetField.drop(domain_id=dom.id)
        CollectionData.drop(domain_id=dom.id)
    else:
        raise Exception(f'NO SUPER DOMAIN WITH ID {super_domain_id} FOUND')

    return dom


def get_all_domains():
    return Domain.get_all()


def get_domains_by_super_id(super_id):
    return Domain.get_all(query={'super_domain_id': super_id})


def duplicate_domain(data):
    data['id'] = None
    data['identifier'] = None
    return save_domain(data)


def get_domains_grouped_by_super_domains(user_rights=None):
    query = get_user_query(user_rights)
    super_domains = SuperDomain.get_all(query=query)
    domains = Domain.get_all()
    res = {}
    for super_dom in super_domains:
        res[super_dom.name] = []
        for dom in domains:
            if super_dom.id == dom.super_domain_id:
                dom_copy = dom.to_dict().copy()
                del dom_copy["created_on"]
                try:
                    del dom_copy["modified_on"]
                except:
                    print("key not found modified_on")
                res[super_dom.name].append(dom_copy)
    return res

