from app.db.Models.category import Category
from app.db.Models.dictionary import Dictionary
import datetime
import uuid

from flask import jsonify

def save_category(data):
    dict_id = data['dict_id']
    #Check if there is a dictionary with the dict_id as an id before inserting a category to it
    if dict_id:
        cat = Category(**data).load()
        if not cat.id:
            new_cat = Category(
                    **{**data, **{
                        'id': uuid.uuid4().hex.upper(),
                        'created_on': datetime.datetime.utcnow()
                    }})
            cat = new_cat

        cat.code = data.get('code', None)
        cat.cat = data.get('cat', None)
        cat.keywords = data.get('keywords', None)
        cat.cat_id = data.get('dict_id', None)
        cat.modified_on = datetime.datetime.utcnow()

        if Category().db().find_one({'_id': {'$ne': cat.id}, 'name': cat.code}):
            return {"status": 'fail', "message": 'category code already used'}, 409
        cat.save()
    else:
        return {"status": "fail", "message": "No Dictionary with provided ID found"}, 409

    return {"status": "success", "message": "category saved"}, 201

def get_all_categories_by_dict_id(dict_id):
    return Category.get_all(query={'dict_id': dict_id})

def delete_category(cat_id):
    cat = Category(**{'id': cat_id}).load()
    if cat.id:
        cat.delete()
        return {"status": "success", "message": "Dictionary deleted."}, 200
    else:
        return {"status": "success", "message": "No Dictionary found."}, 404


def get_category(cat_id):
    return Category(**{'id': cat_id}).load()


