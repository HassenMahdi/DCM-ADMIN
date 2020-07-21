import uuid
import datetime

from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.super_domain import SuperDomain


def save_super_domain(data):
    dom = SuperDomain(**data).load()
    if not dom.id:
        identifier = uuid.uuid4().hex.upper()
        new_dom = SuperDomain(
            **{**data, **{
                'id': identifier,
                'identifier': identifier,
                'created_on': datetime.datetime.utcnow()

            }})
        #     CREATE NEW TABLES HERE
        dom = new_dom
    else:
        dom.name = data['name']
        dom.description = data['description']

    dom.save()

    return dom


def delete_domain(data):
    super_dom = SuperDomain(**data).load()
    if super_dom.id:
        Domain.delete(query={"super_domain_id": super_dom.id})
        TargetField.drop(domain_id=super_dom.id)
    return super_dom


def get_all_super_domains():
    return SuperDomain.get_all()
