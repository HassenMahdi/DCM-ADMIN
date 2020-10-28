from app.datacheck.default.ref import ReferenceCheck
from app.db.Models.field import TargetField
from app.db.Models.reference_type import ReferenceType


class DTOFields():

    @staticmethod
    def from_dto_dict_to_dao_dict(d):
        new_d = {**d, 'rules':[]}

        if new_d.get('ref_type'):
            new_d['ref_type_id'] = new_d.get('ref_type').get('value')

        for rule in d.get('rules', []):
            if "property" in rule and rule["property"]:
                rule["property"] = rule["property"]['value']
            new_d['rules'].append(rule)

        return new_d

    @staticmethod
    def from_dao_to_dto(dao: TargetField, domain_id):
        dto = DTOFields()
        dto.__dict__ = {**dao.__dict__, "rules":[]}
        dto.id = dao.id

        if dao.ref_type_id:
            ref_type_obj = ReferenceType().load({'_id': dao.ref_type_id})
            ref_type = dict(value=ref_type_obj.id, label=ref_type_obj.label)
            dto.ref_type = ref_type
        else:
            dto.ref_type = None

        dto.rules = []
        for rule in dao.rules:
            if "property" in rule and rule["property"]:
                tf = TargetField().load({'name': rule["property"]}, domain_id=domain_id)
                rule["property"] = {'value': tf.name, 'label':tf.label}

            dto.rules.append(rule)

        return dto
