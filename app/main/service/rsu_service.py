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
        print('row',sheet.row_values(row))
        data = dict(zip(new_columns, sheet.row_values(row)))
        compare_data(data)
        #createRow(data, rows)

    #RsuComposition().db().insert_many(rows)

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

def compare_rsu_data(file):
    book = xlrd.open_workbook(file_contents=file.read())
    sheet = book.sheet_by_index(0)

    new_columns = []
    for col in range(sheet.ncols):
        col_name = str(rsu_map_column(sheet.cell_value(0, col))).lower()
        new_columns.append(col_name)

    rows = []
    for row in range(1, sheet.nrows):
        data = dict(zip(new_columns, sheet.row_values(row)))
        compare_data(data)
        #createRow(data, rows)


def compare_data(col):
    query = {'composition.adresse': col['adresse'], "composition.type_logement": col['type_logement']}
    res = RsuComposition.get_all(query=query)
    to_filter_wtih = ["nb_pieces"]

    for row in res:
        for filter in to_filter_wtih:
            is_fraud = filterBy(filter,col[filter],row.composition)
            print("Rah si ",col["nom"], is_fraud)

def filterBy(col_name,value,row):
    col = row.get(col_name)
    if ';' in col:
        compare = col.split(";")
        if(value<float(compare[1]) and value>float(compare[0])):
            return True
        return False
    else:
        if value == col:
            return True
        return False

