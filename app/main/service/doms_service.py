import uuid
import datetime

from app.db.Models.domain import Domain
from app.main import db
from app.main.model.user import User


def save_domain(data):
    dom = Domain(**data).load()
    if not dom.id:
        identifier = uuid.uuid4().hex.upper()
        new_dom = Domain(
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


def get_all_domains():
    return Domain.get_all()
