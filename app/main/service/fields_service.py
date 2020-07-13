import uuid
import datetime

from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.main import db
from app.main.model.user import User


def save_field(data, domain_id):
    target_field = TargetField(**data).load(domain_id=domain_id)
    if not target_field.id:
        identifier = uuid.uuid4().hex.upper()
        new_dom = TargetField(
           **{
                'id': identifier,
                'created_on': datetime.datetime.utcnow()
            })
        target_field = new_dom

    target_field.label = data['label']
    target_field.name = data['name']
    target_field.description = data.get('description', None)
    target_field.category = data['category']
    target_field.type = data['type']
    target_field.rules = data['rules']
    target_field.modified_on = datetime.datetime.utcnow()

    target_field.save(domain_id=domain_id)

    return target_field


def get_all_fields(domain_id):
    return TargetField.get_all(domain_id = domain_id)
