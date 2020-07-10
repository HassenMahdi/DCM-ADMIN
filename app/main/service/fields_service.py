import uuid
import datetime

from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.main import db
from app.main.model.user import User


def save_field(data, domain_id):
    dom = TargetField(**data).load(domain_id=domain_id)
    if not dom.id:
        identifier = uuid.uuid4().hex.upper()
        new_dom = TargetField(
            **{**data, **{
                'id': identifier,
                'created_on': datetime.datetime.utcnow()
            }})
        dom = new_dom

    dom.label = data['label']
    dom.name = data['name']
    dom.description = data.get('description', None)
    dom.category = data['category']
    dom.type = data['type']
    dom.modified_on = datetime.datetime.utcnow()

    dom.save(domain_id=domain_id)

    return dom


def get_all_fields(domain_id):
    return TargetField.get_all(domain_id = domain_id)
