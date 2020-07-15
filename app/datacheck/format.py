from app.datacheck import CheckAbstract, CheckParam


class Check(CheckAbstract):

    id = "FORMAT_CHECK"
    name = "Format Check"
    category = None
    description = None

    parameters = [
        CheckParam('regex', label='REGEX')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]