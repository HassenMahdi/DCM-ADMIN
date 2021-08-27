import datetime
import traceback

import xlrd

from app.db.Models.rsu_composition import RsuComposition
from app.main.util.rsu_utils import rsu_map_column, SOURCES, TARGETS, allowed_file, RES_SOURCES, RES_TARGETS
from app.main.util.strings import generate_id

from geopy.geocoders import Nominatim
from geopy.extra.rate_limiter import RateLimiter

geocoder = Nominatim(user_agent = 'deepkube')
geocode = RateLimiter(geocoder.geocode, min_delay_seconds = 1,return_value_on_exception = None)


def get_rows_col_from_file(request):
    try:
        if 'file' not in request.files:
            return {"status": "failed", "message": 'No file part'}

        file = request.files['file']
        filename = file.filename

        if filename == '':
            return {"status": "failed", "message": "Empty Payload"}

        file_extension = allowed_file(filename)

        if file and file_extension:
            book = xlrd.open_workbook(file_contents=file.read())
            sheet = book.sheet_by_index(0)

            new_columns = []
            for col in range(sheet.ncols):
                col_name = str(rsu_map_column(sheet.cell_value(0, col)))
                new_columns.append(col_name)

            rows = []
            for row in range(1, sheet.nrows):
                data = dict(zip(new_columns, sheet.row_values(row)))
                createRsuRow(data, rows)

            return rows, new_columns

    except Exception:
        traceback.print_exc()
        return {"status": "failed", "message": "Exception Occured"}


def import_rsu_data_from_file(request):
    rows, columns = get_rows_col_from_file(request)

    # SAVE new compositions
    if len(rows) > 0:
        RsuComposition().db().insert_many(rows)
        RsuComposition().createIndex()

        return {"status": "success", "message": f'RSU Composition Data Imported'}, 200
    else:
        return {"status": "success", "message": f'Imported file is empty'}, 200


def update_rsu_data_from_file(request):
    rows, columns = get_rows_col_from_file(request)
    rowToAdd = []

    # UPDATE / Get new compositions from the file then save it
    for row in rows:
        if not RsuComposition().db().find_one({"composition": row['composition']}):
            rowToAdd.append(row)

    if len(rowToAdd) > 0:
        RsuComposition().db().insert_many(rowToAdd)
        return {"status": "success", "message": f'RSU Composition Data Updated'}, 200
    else:
        return {"status": "success", "message": f'Nothing to update'}, 200


def get_all_rsu_data():
    data = RsuComposition().get_all({})

    response = {
        "data": data,
        "sources": SOURCES,
        "targets": TARGETS
    }

    return response


def createRsuRow(data, rows=[]):
    aji = {
        'type':'Point',
        'coordinates' : [geocode(data['adresse']).longitude,geocode(data['adresse']).latitude]
    }

    new_composition = {
        'id': generate_id(),
        'created_on': datetime.datetime.now(),
        'modified_on': datetime.datetime.now(),
        'composition': data,
        'location': aji
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
        # createRow(data, rows)


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
        if float(compare[1]) > value > float(compare[0]):
            return True
        return False
    else:
        if value == col:
            return True
        return False

