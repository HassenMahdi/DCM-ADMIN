SOURCES = ["Nom", "Adresse", "Type logement", "Nombre de pieces", "Ordinateur",
          "Niveau scolaire du conjoint", "Sanitaire", "Antenne parabolique","Travail"]

TARGETS = ["nom", "adresse", "type_logement", "nb_pieces", "oridnateur", "nv_scolaire_conjoint",
          "sanitaire", "antenne_parabolique","travail"]

RES_SOURCES = ["Nom", "latitude","longitude", "Type logement", "Nombre de pieces", "Ordinateur",
          "Niveau scolaire du conjoint", "Sanitaire", "Antenne parabolique"]

RES_TARGETS = ["nom", "latitude","longitude", "type_logement", "nb_pieces", "oridnateur", "nv_scolaire_conjoint",
          "sanitaire", "antenne_parabolique"]

ALLOWED_EXTENSIONS = {"xlsx", "xlx"}
# "xlmx", "csv"


def rsu_map_column(column):
    mapping = dict(zip(SOURCES, TARGETS))
    return mapping.get(column)


def allowed_file(filename):
    file_extension = filename.rsplit('.', 1)[-1].lower()

    if '.' in filename and file_extension in ALLOWED_EXTENSIONS:
        return file_extension
