import datetime
import xlrd
from io import BytesIO
import pandas as pd
from flask import send_file

from app.db.Models.domain import Domain
from app.db.Models.reference_data import ReferenceData
from app.db.Models.reference_type import ReferenceType
from app.main.util.strings import generate_id


def get_ref_type(ref_type_id):
    ref_type = ReferenceType(id=ref_type_id).load()

    if ref_type.parent_id:
        parent = ReferenceType(id=ref_type.parent_id).load()
        ref_type.shared = parent.shared
        ref_type.label = parent.label
        ref_type.properties = parent.properties
        ref_type.domain_ids = parent.domain_ids

    return ref_type



def save_ref_type(data):
    ref_type_id = data.get('id', None)
    ref_type = ReferenceType()
    if ref_type_id:
        ref_type.load(dict(_id=ref_type_id))

    if not ref_type.id:
        ref_type.created_on = datetime.datetime.now()

    # SAVE CHILD AS VERSION
    if data.get('parent_id', None):
        ref_type.parent_id = data.get('parent_id')
        ref_type.version_label = data.get('version_label')
        ref_type.description = data.get('description', None)
        ref_type.modified_on = datetime.datetime.now()

        if ReferenceType().db().find_one({'parent_id': ref_type.parent_id, '_id': {'$ne': ref_type.id}, 'version_label': ref_type.version_label}):
            return {"status": 'fail', "message": 'Reference Version Already Exists'}, 409
    # SAVE AS PARENT VERSION
    else:
        ref_type.label = data.get('label')
        ref_type.description = data.get('description', None)
        ref_type.properties = data.get('properties', [])
        ref_type.modified_on = datetime.datetime.now()
        ref_type.domain_ids = data.get('domain_ids', [])
        ref_type.shared = data.get('shared', False)
        ref_type.parent_id = data.get('parent_id', None)
        ref_type.version_label = data.get('version_label') or 'Version 1'

        if ReferenceType().db().find_one({'_id': {'$ne': ref_type.id}, 'label': ref_type.label}):
            return {"status": 'fail', "message": 'Reference Type Name Already Exists'}, 409

        if ReferenceType().db().find_one({'parent_id': ref_type.id, '_id': {'$ne': ref_type.id}, 'version_label': ref_type.version_label}):
            return {"status": 'fail', "message": 'Reference Version Already Exists In This Reference Type'}, 409

    ref_type.save()

    return {"status": 'success', "message": 'Reference Type Saved'}, 201


def delete_ref_type(ref_type_id):
    # CHECK IF REF TYPE IS USED
    ref_type = ReferenceType().load(dict(_id=ref_type_id))
    for domain_id in ref_type.domain_ids:
        if ref_type.is_used_in_domain(domain_id):
            return {'status': 'fail', 'message': 'Reference Type cannot be deleted because it is used.'}, 409

    ReferenceData().db().remove(dict(ref_type_id=ref_type_id))
    ref_type.delete()

    return {'status': 'success', 'message': 'Reference Type deleted'}, 200


def share_ref_type(ref_type_id, domain_ids):
    # CHECK IF REF TYPE IS USED
    ref_type = ReferenceType().load(dict(_id=ref_type_id))

    # CHEKC IF REF TYPE IS USED
    removed_domains_ids = set(domain_ids).union(set(ref_type.domain_ids)).difference(set(domain_ids))
    for domain_id in removed_domains_ids:
        if ref_type.is_used_in_domain(domain_id):
            domain = Domain().load(dict(_id=domain_id))
            if domain.id:
                return {'status': 'fail', 'message': f'Cannot remove {ref_type.label} from domain {domain.name}.'}, 409

    ref_type.domain_ids = domain_ids
    ref_type.save()

    return {'status': 'success', 'message': 'Reference Type Collection Updated'}, 200


def get_all_ref_types(domain_id=None, include_shared=True):
    query = {"parent_id": None}
    if domain_id:
        query.update({
            "$or": [
                    {
                        "domain_ids": {
                            "$all": [domain_id]
                        }
                    },
                {"shared": True}
            ]
        })

    lookup = {
            "from": ReferenceType.__TABLE__,
            "localField": "_id",
            "foreignField": "parent_id",
            "as": "versions",
        }

    cursor = ReferenceType().db().aggregate([{"$match": query}, {"$lookup": lookup}])

    result = []
    for r in cursor:
        reference_type = ReferenceType(**r)
        first_version = ReferenceType(**r)
        reference_type.versions = [first_version] + [ReferenceType(**v) for v in r["versions"]]
        result.append(reference_type)

    return result


def get_ref_data(ref_id):
    return ReferenceData(id=ref_id).load()


def save_ref_data(data):
    ref_id = data.get('id', None)
    ref_data = ReferenceData()
    if ref_id:
        ref_data.load({"id": ref_id})

    if not ref_data.id:
        ref_data.created_on = datetime.datetime.now()
        ref_data.ref_type_id = data.get('ref_type_id')

    ref_data.code = data.get('code')
    ref_data.alias = data.get('alias', [])
    ref_data.modified_on = datetime.datetime.now()
    ref_data.properties = data.get('properties', {})

    if not ref_data.has_unique_code():
        return {'status': 'fail', 'message': "this Code is already used"}, 409

    if not ref_data.has_unique_alias():
        return {'status': 'fail', 'message': "One Alias or more are already is use"}, 409

    ref_data.save()

    return {'status': 'success', 'message': "Reference Data Saved"}, 201


def delete_ref_data(ref_id):
    return ReferenceData().load(dict(_id=ref_id)).delete()


def get_all_ref_data(ref_type_id=None):
    query = {}
    if ref_type_id:
        query = {"ref_type_id": ref_type_id}
    return ReferenceData().get_all(query)


def import_ref_data_from_file(file, ref_type_id):
    properties = {'code': 'code', 'alias': 'alias'}
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
        create_codes(ref_type_id, data, ref_type, ops)

    # Validate Excel File
    codes_set = set()
    alias_set = set()

    duplicated_alias_set = set()
    duplicated_codes_set = set()

    for ref_data in ops:
        code = ref_data['code']
        alias = ref_data['alias']
        if code in codes_set:
            duplicated_codes_set.add(code)
        else:
            codes_set.add(code)
        for a in alias:
            if a in alias_set:
                duplicated_alias_set.add(a)
            else:
                alias_set.add(a)

    if len(duplicated_alias_set) > 0 or len(duplicated_codes_set) > 0:
        return {
                   "status": "fail",
                    "message": f'<h6>Duplicated Codes</h6>'
                               f'<ul>'
                               + ''.join([f'<li>{c}</li>' for c in duplicated_codes_set])
                               + f'</ul>'
                                 f'<h6>Duplicated Aliases</h6>'
                                 f'<ul>'
                               + ''.join([f'<li>{c}</li>' for c in duplicated_alias_set])
                               + f'</ul>'
               }, 409

    ReferenceData().db().delete_many({"ref_type_id": ref_type_id})
    ReferenceData().db().insert_many(ops)

    return {"status": "success", "message": f'Reference Data Imported'}, 200


def update_ref_data_from_file(file, ref_type_id):
    properties = {'code': 'code', 'alias': 'alias'}
    ref_type = get_ref_type(ref_type_id)
    for p in ref_type.properties:
        properties.setdefault(str(p['label']).lower(), p['code'])

    wb = xlrd.open_workbook(file_contents=file.read())
    sh = wb.sheet_by_index(0)

    file_columns = []  # The row where we stock the name of the column
    for col in range(sh.ncols):
        col_name = str(sh.cell_value(0, col)).lower()
        file_columns.append(properties.get(col_name, col_name))

    codes = []
    for row in range(1, sh.nrows):
        data = dict(zip(file_columns, sh.row_values(row)))
        create_codes(ref_type_id, data, ref_type, codes)
    # Separate the codes into two lists: The ones to update and the ones to add
    references = ReferenceData().db().find({"ref_type_id": ref_type_id, "code": {"$in": [c["code"] for c in codes]}})
    # todo We can enhance this by removing the references that have the same alias as the file
    codes_to_update = [c for c in references]
    codes_to_add = [code for code in codes if code['code'] not in [m['code'] for m in codes_to_update]]
    # Add the new codes
    if len(codes_to_add) > 0:
        ReferenceData().db().insert_many(codes_to_add)
    # Update the codes
    final_updated_codes = []
    for code in codes_to_update:
        ref_code_index = [c["code"] for c in codes].index(code['code'])
        if code['alias'] != codes[ref_code_index]['alias']:
            code['alias'] = codes[ref_code_index]['alias']
            code['modified_on'] = codes[ref_code_index]['modified_on']
            final_updated_codes.append(code)
    if len(final_updated_codes) > 0:
        for c in final_updated_codes:
            ReferenceData().db().update_one(
                {'_id': c['_id']},
                {'$set': {
                    'alias': c["alias"],
                    "modified_on": c['modified_on']
                }
                }, upsert=False
            )

    return {"status": "success", "message": f'Reference Data Updated'}, 200


def create_codes(ref_type_id, data, ref_type, codes=[]):
    ref_data = {'created_on': datetime.datetime.now(), 'modified_on': datetime.datetime.now(),
                'ref_type_id': ref_type_id, 'code': data.get('code'),
                'alias': data.get('alias', '').split(';'), 'properties': {},
                'id': generate_id()
                }
    for p in ref_type.properties:
        property_code = p['code']
        ref_data['properties'][property_code] = data.get(property_code, None)
    codes.append(ref_data)

    return ref_data


def download_ref_data_from_file(ref_type_id):
    ref = ReferenceData().db().find({"ref_type_id": ref_type_id})
    references = [{'code': m['code'], 'alias': ';'.join(m['alias'])} for m in ref]
    df = pd.DataFrame(references)
    output = BytesIO()
    writer = pd.ExcelWriter(output, engine='xlsxwriter')
    df.to_excel(writer, sheet_name='Reference Data')
    writer.save()
    output.seek(0)
    return send_file(output, attachment_filename='reference.xlsx', as_attachment=True)


