from app.db.document import Document


class Category(Document):
    __TABLE__ = "categories"

    code = None
    cat = None
    keywords = None
    dict_id = None
    created_on = None
    modified_on = None

