from app.db.document import Document


class Dictionary(Document):
    __TABLE__ = "dictionaries"

    name = None
    description = None
    created_on = None
    modified_on = None


