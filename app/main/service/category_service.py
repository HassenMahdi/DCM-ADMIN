from app.db.Models.word import Word
import datetime
import uuid


def save_word(data):
    dict_id = data['dict_id']
    #Check if there is a dictionary with the dict_id as an id before inserting a word to it
    if dict_id:
        word = Word(**data).load()
        if not word.id:
            new_word = Word(
                    **{**data, **{
                        'id': uuid.uuid4().hex.upper(),
                        'created_on': datetime.datetime.utcnow()
                    }})
            word = new_word

        word.code = data.get('code', None)
        word.cat = data.get('cat', None)
        word.keywords = data.get('keywords', None)
        word.dict_id = data.get('dict_id', None)
        word.modified_on = datetime.datetime.utcnow()

        if Word().db().find_one({'_id': {'$ne': word.id}, 'name': word.code}):
            return {"status": 'fail', "message": 'Word code already used'}, 409
        word.save()
    else:
        return {"status": "fail", "message": "No Dictionary with provided ID found"}, 409

    return {"status": "success", "message": "Word saved"}, 201


def get_all_words_by_dict_id(dict_id):
    return Word.get_all(query={'dict_id': dict_id})


def delete_word(word_id):
    word = Word(**{'id': word_id}).load()
    if word.id:
        word.delete()
        return {"status": "success", "message": "Word deleted."}, 200
    else:
        return {"status": "success", "message": "No Word found."}, 404


def get_word(word_id):
    return Word(**{'id': word_id}).load()


def get_words_by_cat(cat):
    return Word.get_all(query={'cat': cat})


