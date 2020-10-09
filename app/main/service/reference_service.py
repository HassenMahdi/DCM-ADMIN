import datetime

import xlrd
from pymongo import InsertOne

from app.db.Models.field import TargetField
from app.db.Models.reference_data import ReferenceData
from app.db.Models.reference_type import ReferenceType
from app.main.util.strings import generate_id


def get_ref_type(ref_type_id):
    return ReferenceType(id=ref_type_id).load()


def save_ref_type(data):
    ref_type_id = data.get('id', None)
    ref_type = ReferenceType()
    if ref_type_id:
        ref_type.load(dict(_id=ref_type_id))

    if not ref_type.id:
        ref_type.created_on = datetime.datetime.now()

    ref_type.label = data.get('label')
    ref_type.description = data.get('description', None)
    ref_type.properties = data.get('properties', [])
    ref_type.modified_on = datetime.datetime.now()
    ref_type.domain_ids = data.get('domain_ids', [])

    ref_type.save()

    return ref_type


def delete_ref_type(ref_type_id):
    # CHECK IF REF TYPE IS USED
    ref_type = ReferenceType().load(dict(_id=ref_type_id))
    for domain_id in ref_type.domain_ids:
        if TargetField().db(domain_id=domain_id).find_one({'rules.conditions.ref_type_id' : ref_type.id}):
            return {'status': 'fail', 'message': 'Reference Type cannot be deleted because it is used.'}, 409

    ReferenceData().db().remove(dict(ref_type_id=ref_type_id))
    ref_type.delete()

    return {'status':'success', 'message':'Reference Type deleted'}, 200


def get_all_ref_types(domain_id = None):
    query = {}
    if domain_id:
        query = {"domain_ids":{"$all": [domain_id]}}
    return ReferenceType().get_all(query)


def get_ref_data(ref_id):
    return ReferenceData(id=ref_id).load()


def save_ref_data(data):
    ref_id = data.get('id', None)
    ref_data = ReferenceData()
    if ref_id:
        ref_data.load(dict(_id=ref_id))

    if not ref_data.id:
        ref_data.created_on = datetime.datetime.now()
        ref_data.ref_type_id = data.get('ref_type_id')

    ref_data.code = data.get('code')
    ref_data.alias = data.get('alias', [])
    ref_data.modified_on = datetime.datetime.now()
    ref_data.properties = data.get('properties', {})

    ref_data.save()

    return ref_data


def delete_ref_data(ref_id):
    return ReferenceData().load(dict(_id=ref_id)).delete()


def get_all_ref_data(ref_type_id = None):
    query = {}
    if ref_type_id:
        query = {"ref_type_id":ref_type_id}
    return ReferenceData().get_all(query)


def import_ref_data_from_file(file, ref_type_id):

    properties = {'code':'code', 'alias': 'alias'}
    ref_type = get_ref_type(ref_type_id)
    for p in ref_type.properties:
        properties.setdefault(str(p['label']).lower(), p['code'])

    wb = xlrd.open_workbook(file_contents=file.read())
    sh = wb.sheet_by_index(0)

    file_columns = []  # The row where we stock the name of the column
    for col in range(sh.ncols):
        col_name = str(sh.cell_value(0, col)).lower()
        file_columns.append(properties.get(col_name, col_name))

    ops = []
    for row in range(1, sh.nrows):
        data = dict(zip(file_columns, sh.row_values(row)))
        ref_data = {'created_on': datetime.datetime.now(), 'modified_on': datetime.datetime.now(),
                    'ref_type_id': ref_type_id, 'code': data.get('code'),
                    'alias': data.get('alias', '').split(';'), 'properties': {},
                    'id': generate_id()
                    }
        for p in ref_type.properties:
            property_code = p['code']
            ref_data['properties'][property_code]= data.get(property_code, None)

        ops.append(ref_data)
    ReferenceData().db().delete_many({})
    ReferenceData().db().insert_many(ops)
    return
