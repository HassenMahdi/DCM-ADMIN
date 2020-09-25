import datetime
from app.db.Models.reference_data import ReferenceData
from app.db.Models.reference_type import ReferenceType


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
    ReferenceData().db().remove(dict(ref_type_id=ref_type_id))
    return ReferenceType().load(dict(_id=ref_type_id)).delete()


def get_all_ref_types(domain_id = None):
    query = {}
    if domain_id:
        query = query.update({"domain_ids":{"$all": [domain_id]}})
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