import uuid
import datetime
from copy import copy

import xlrd

from app.datacheck.default.empty import EmptyCheck
from app.datacheck.default.ref import ReferenceCheck
from app.db.Models.domain import Domain
from app.db.Models.field import TargetField
from app.db.Models.flow_context import FlowContext
from app.db.Models.mapping import Mapping
from app.main.util.strings import camelCase


def save_field(data, domain_id):
    dom = Domain(**{'id': domain_id}).load()

    if dom.id:
        target_field = TargetField(**data).load(domain_id=domain_id)
        original_field = copy(target_field)

        if not target_field.id:
            identifier = uuid.uuid4().hex.upper()
            new_dom = TargetField(
               **{
                    'id': identifier,
                    'created_on': datetime.datetime.utcnow(),
                    'name': camelCase(data['label'])
                })
            target_field = new_dom

        target_field.label = data['label']
        target_field.description = data.get('description', None)
        target_field.type = data['type']
        target_field.mandatory = data.get('mandatory', False)
        target_field.editable = data.get('editable', False)
        target_field.rules = data.get('rules', [])
        target_field.modified_on = datetime.datetime.utcnow()
        target_field.ref_type_id = data.get('ref_type_id', None)

        if original_field.id:
            if original_field.type != target_field.type:
                if FlowContext().db().find_one({"domain_id": domain_id, "columns":{"$in":[target_field.name]}}):
                    return {'status':'fail', 'message': 'Unable to change Field Type After Upload'}, 409

        target_field.save(domain_id=domain_id)

    else:
        return {"status":"fail", "message":"Domain does exist"}, 409

    return {"status":"success", "message":"Field Created"}, 200


def delete_field(data, domain_id):
    tf = TargetField(**data).load(domain_id=domain_id)

    if tf.is_used(domain_id):
        return {"status": "fail", "message": "Target Field cannot be deleted."}, 409
    elif Mapping.is_using_field(tf.name, domain_id):
        return {"status": "fail", "message": "Target Field is used in mapping."}, 409

    tf.delete(domain_id=domain_id)
    return {"status":"success", "message": "Target Field deleted."}, 200


def get_all_fields(domain_id):
    return TargetField.get_all(domain_id = domain_id)


def get_simple(domain_id):
    return list(TargetField().db(domain_id = domain_id).aggregate([
        {"$project": {'label': 1, 'value': '$name', "type":1}}
        ]))


def fields_from_file(file, domain_id):

    col_field = {
        'MANDATORY': 'mandatory',
        'DESCRIPTION': 'description',
        'FIELD': 'label',
        'EDITABLE': 'editable',
        'TYPE': 'type'
    }

    wb = xlrd.open_workbook(file_contents=file.read())
    sh = wb.sheet_by_index(0)

    first_row = []  # The row where we stock the name of the column
    for col in range(sh.ncols):
        first_row.append(sh.cell_value(0, col))

    fields_data = []
    for row in range(1, sh.nrows):
        elm = {}
        for col in range(sh.ncols):
            data_field_name = col_field[first_row[col]]
            elm[data_field_name] = sh.cell_value(row, col)

        if elm.get('mandatory', None):
            elm.setdefault('rules', []).append({'type': EmptyCheck.id})

        fields_data.append(elm)

    TargetField.drop(domain_id=domain_id)
    for data in fields_data:
        save_field(data, domain_id)

    return


def duplicate_fields(old_id, new_id):
    fields = get_all_fields(old_id)
    for f in fields:
        f.save(domain_id=new_id)

    return fields


