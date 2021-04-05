from app.db.Models.dictionary import Dictionary
from app.db.Models.word import Word
import datetime
import uuid


def save_dictionary(data):
    dict = Dictionary(**data).load()

    if not dict.id:
        new_dict = Dictionary(**{**data,**{
                    'id': uuid.uuid4().hex.upper(),
                    'created_on': datetime.datetime.utcnow()
                }})
        dict = new_dict

    dict.name = data.get('name', None)
    dict.description = data.get('description', None)
    dict.modified_on = datetime.datetime.utcnow()

    if Dictionary().db().find_one({'_id': {'$ne': dict.id}, 'name': dict.name}):
        return {"status": 'fail', "message": 'Dictionary name already used'}, 409

    dict.save()

    return {"status": "success", "message": "Dictionary saved"}, 201


def get_all_dictionaries():
    return Dictionary.get_all()


def delete_dcitionary(dict_id):
    dict = Dictionary(**{'id': dict_id}).load()

    if dict.id:
        cats = Word.get_all(query={'dict_id':dict.id})

        for cat in cats:
            cat.delete()

        dict.delete()

        return {"status":"success", "message": "Dictionary deleted."}, 200
    else:
        return {"status": "success", "message": "No Dictionary found."}, 404


def get_dictionary(dict_id):
    dict = Dictionary(**{'id': dict_id}).load()

    if dict.id:
        return dict
    else:
        return {"status": "success", "message": "No Dictionary found."}, 404