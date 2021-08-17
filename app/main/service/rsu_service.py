import datetime
import xlrd

from app.db.Models.rsu_composition import RsuComposition
from app.main.util.rsu_utils import rsu_map_column, sources, targets
from app.main.util.strings import generate_id


def import_rsu_data_from_file(file):
    book = xlrd.open_workbook(file_contents = file.read())
    sheet = book.sheet_by_index(0)

    new_columns = []
    for col in range(sheet.ncols):
        col_name = str(rsu_map_column(sheet.cell_value(0, col))).lower()
        new_columns.append(col_name)

    rows = []
    for row in range(1, sheet.nrows):
        data = dict(zip(new_columns, sheet.row_values(row)))
        createRow(data, rows)

    RsuComposition().db().insert_many(rows)

    return {"status": "success", "message": f'RSU Composition Data Imported'}, 200


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
