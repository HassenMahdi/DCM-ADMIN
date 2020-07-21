import uuid
import datetime

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


def get_all_super_domains():
    return SuperDomain.get_all()
