import uuid
import datetime

from app.db.Models.domain import Domain


def save_domain(data):
    dom = Domain(**data).load()
    if not dom.id:
        identifier = uuid.uuid4().hex.upper()
        super_domain_id = data['super_domain_id']
        new_dom = Domain(
            **{**data, **{
                'id': identifier,
                'identifier': identifier,
                'created_on': datetime.datetime.utcnow(),
                'super_domain_id': super_domain_id

            }})
        #     CREATE NEW TABLES HERE
        dom = new_dom
    else:
        dom.name = data['name']
        dom.description = data['description']

    dom.save()

    return dom


def get_all_domains():
    return Domain.get_all()


def get_domains_by_super_id(super_id):
    return Domain.get_all(query={'super_domain_id':super_id})
