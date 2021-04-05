from app.db.document import Document


class Word(Document):
    __TABLE__ = "words"

    code = None
    cat = None
    keywords = None
    dict_id = None
    created_on = None
    modified_on = None

