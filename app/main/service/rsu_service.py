import xlrd

from app.db.Models.rsu_composition import RsuComposition


def import_rsu_data_from_file(file):
    book = xlrd.open_workbook(file_contents = file.read())
    sheet = book.sheet_by_index(0)

    file_columns = []
    for col in range(sheet.ncols):
        # col_name = str(map_column(sheet.cell_value(0, col))).lower()
        col_name = str(sheet.cell_value(0, col)).lower()
        file_columns.append(col_name)

    # create a dataframe from this sheet + those new file columns

    data = sheet.to_dict(orient = "records")

    RsuComposition().db().insert_many(data)

    return {"status": "success", "message": f'RSU Composition Data Imported'}, 200


def map_column(column):
    mapping = {"Nombre de foyer": "nb_foyer"}

    return mapping.get(column)
