import uuid
import datetime

from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.super_domain import SuperDomain
from app.main.util.strings import get_next_iteration, camelCase


def save_super_domain(data):
    dom = SuperDomain(**data).load()
    if not dom.id:
        identifier = camelCase(data['name'])
        next_iter = get_next_iteration(
            SuperDomain().db().find({'identifier': {'$regex': f"{identifier}(_[1-9]+)?"}}, {'identifier': 1})
        )
        if next_iter > 0:
            identifier = f"{identifier}_{str(next_iter)}"

        new_dom = SuperDomain(
            **{**data, **{
                'id': identifier,
                'identifier': identifier,
                'created_on': datetime.datetime.utcnow()

            }})
        #     CREATE NEW TABLES HERE
        dom = new_dom

    dom.name = data['name']
    dom.description = data.get('description')
    dom.modified_on = datetime.datetime.utcnow()

    dom.save()

    return dom


def delete_super_domain(data):
    super_dom = SuperDomain(**data).load()
    if super_dom.id:
        dms = Domain.get_all(query={'super_domain_id':super_dom.id})
        dm: Domain
        for dm in dms:
            TargetField.drop(domain_id=dm.id)
            dm.delete()

        super_dom.delete()

    return super_dom

def get_user_query(user_rights):
    query = {}
    if user_rights:
        if not user_rights['admin']:
            query = {'_id': {'$in': user_rights['domain_ids']}}
    return query


def get_all_super_domains(user_rights=None):
    return SuperDomain.get_all(query=get_user_query(user_rights))


def get_domains_hierarchy(user_rights={}):
    query_result = SuperDomain().db().aggregate([
        {"$match":get_user_query(user_rights)},
        {
       "$lookup": {
           'from': Domain().db().name,
           'localField': 'identifier',
           'foreignField': 'super_domain_id',
           'as': 'domains'
           }
        }])

    hierarchy = []
    for sd in query_result:
        hierarchy.append(
            SuperDomain(
                **{**sd, 'domains':[Domain(**d) for d in sd['domains']]})
        )

    return hierarchy
