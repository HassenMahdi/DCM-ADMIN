import math
import uuid


def camelCase(st):
    output = ''.join(x for x in st.title() if x.isalnum())
    return output[0].lower() + output[1:]


def generate_id():
    return uuid.uuid4().hex.upper()


def get_next_iteration(cursor, key='identifier'):
    all_records = list(cursor)
    if len(all_records) == 0:
        return 0
    else:
        def get_num(identifier):
            split = identifier[key].split('_')
            if len(split) == 2:
                return int(split[1])
            else:
                return 0

    return max(len(all_records), max(list(map(get_num, all_records)))+1)

