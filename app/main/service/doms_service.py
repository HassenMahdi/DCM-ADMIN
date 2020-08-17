import uuid
import datetime

from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.super_domain import SuperDomain


def get_domain(dom_id):
    return Domain(id=dom_id).load()


def save_domain(data):
    super_domain_id = data['super_domain_id']
    super_dom = SuperDomain(**{'id':super_domain_id}).load()

    if super_dom.id:
        dom = Domain(**data).load()
        if not dom.id:
            identifier = uuid.uuid4().hex.upper()

            new_dom = Domain(
                **{**data, **{
                    'id': identifier,
                    'identifier': identifier,
                    'created_on': datetime.datetime.utcnow(),
                    'super_domain_id': super_domain_id

                }})
            #     CREATE NEW TABLES HERE
            dom = new_dom

        dom.name = data['name']
        dom.description = data['description']
        dom.modified_on = datetime.datetime.utcnow()

        dom.save()
    else:
        raise Exception(f'NO SUPER DOMAIN WITH ID {super_domain_id} FOUND')

    return dom


def delete_domain(data):
    super_domain_id = data['super_domain_id']
    super_dom = SuperDomain(**{'id':super_domain_id}).load()

    if super_dom.id:
        dom = Domain(**data).delete()
        TargetField.drop(domain_id=dom.id)
    else:
        raise Exception(f'NO SUPER DOMAIN WITH ID {super_domain_id} FOUND')

    return dom


def get_all_domains():
    return Domain.get_all()


def get_domains_by_super_id(super_id):
    return Domain.get_all(query={'super_domain_id':super_id})


def duplicate_domain(data):
    data['id'] = None;
    data['identifier'] = None;
    data['name'] = data['name'] + '- copy';
    return save_domain(data)

def get_domains_grouped_by_super_domains():
    super_domains = SuperDomain.get_all()
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

