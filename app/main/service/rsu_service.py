import datetime
import xlrd

from app.db.Models.rsu_composition import RsuComposition
from app.main.util.rsu_utils import rsu_map_column, sources, targets
from app.main.util.strings import generate_id


def import_rsu_data_from_file(file, update=False):
    book = xlrd.open_workbook(file_contents=file.read())
    sheet = book.sheet_by_index(0)

    new_columns = []
    for col in range(sheet.ncols):
        col_name = str(rsu_map_column(sheet.cell_value(0, col)))
        new_columns.append(col_name)

    rows = []
    for row in range(1, sheet.nrows):
        data = dict(zip(new_columns, sheet.row_values(row)))
        createRow(data, rows)

    # UPDATE / Get new compositions from the file then save it
    if update and len(rows) > 0:
        rowToAdd = []
        for row in rows:
            if not RsuComposition().db().find_one({"composition": row['composition']}):
                rowToAdd.append(row)

        if len(rowToAdd) > 0:
            RsuComposition().db().insert_many(rowToAdd)
            return {"status": "success", "message": f'RSU Composition Data Updated'}, 200
        else:
            return {"status": "success", "message": f'Nothing to update'}, 200

    # SAVE new compositions
    else:
        RsuComposition().db().insert_many(rows)
        return {"status": "success", "message": f'RSU Composition Data Imported'}, 200

def update_rsu_data_from_file(file):
    import_rsu_data_from_file(file, True)

def get_all_rsu_data():
    data = RsuComposition().get_all({})

    response = {
        "data": data,
        "sources": sources,
        "targets": targets
    }

    return response


def createRow(data, rows = []):
    new_composition = {
        'id': generate_id(),
        'created_on': datetime.datetime.now(),
        'modified_on': datetime.datetime.now(),
        'composition': data
    }

    rows.append(new_composition)
