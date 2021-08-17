sources = ["Nom", "Adresse", "Type logement", "Nombre de pieces", "Ordinateur",
          "Niveau scolaire du conjoint", "Sanitaire", "Antenne parabolique"]

targets = ["nom", "adresse", "type_logement", "nb_pieces", "oridnateur", "nv_scolaire_conjoint",
          "sanitaire", "antenne_parabolique"]


def rsu_map_column(column):
    # mapping = {"Nom": "nom",
    #            "Adresse": "adresse",
    #            "Type logement": "type_logement",
    #            "Nombre de pieces": "nb_pieces",
    #            "Ordinateur": "oridnateur",
    #            "Niveau scolaire du conjoint": "nv_scolaire_conjoint",
    #            "Sanitaire": "sanitaire",
    #            "Antenne parabolique": "antenne_parabolique",
    #            }

    mapping = dict(zip(sources, targets))

    return mapping.get(column)
