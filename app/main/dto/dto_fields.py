from app.datacheck.default.ref import ReferenceCheck
from app.db.Models.field import TargetField
from app.db.Models.reference_type import ReferenceType


class DTOFields():

    @staticmethod
    def from_dto_dict_to_dao_dict(d):
        new_d = {**d, 'rules':[]}

        for rule in d.get('rules', []):
            if "property" in rule and rule["property"]:
                rule["property"] = rule["property"]['value']

            if rule['type'] == ReferenceCheck.id:
                ref_type = rule.get('conditions', {}).get('ref_type', None)
                if ref_type:
                    rule['conditions']['ref_type_id'] = ref_type['value']
                    del rule['conditions']['ref_type']

            new_d['rules'].append(rule)

        return d

    @staticmethod
    def from_dao_to_dto(dao: TargetField, domain_id):
        dto = DTOFields()
        dto.__dict__ = {**dao.__dict__, "rules":[]}
        dto.id = dao.id

        dto.rules = []
        for rule in dao.rules:
            if "property" in rule and rule["property"]:
                tf = TargetField().load({'name': rule["property"]}, domain_id=domain_id)
                rule["property"] = {'value': tf.name, 'label':tf.label}

            if rule['type'] == ReferenceCheck.id:
                ref_type_id = rule.get('conditions', {}).get('ref_type_id', None)
                if ref_type_id:
                    ref_type = ReferenceType().load({'_id': ref_type_id})
                    rule['conditions']['ref_type'] = dict(value=ref_type.id, label=ref_type.label)
                    del rule['conditions']['ref_type_id']

            dto.rules.append(rule)

        return dto
