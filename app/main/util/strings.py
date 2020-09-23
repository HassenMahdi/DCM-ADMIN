import math
import uuid


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


def generate_id():
    uuid.uuid4().hex.upper()


def get_max_id_iter(cursor):
    def get_num(identifier):
        split = identifier['identifier'].split('_')
        if len(split) == 2:
            return int(split[1])
        else:
            return 0

    all = list(cursor)
    return max(max(list(map(get_num, all))),len(all))