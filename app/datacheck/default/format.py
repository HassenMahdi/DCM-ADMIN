from app.datacheck import CheckAbstract, CheckParam


class FormatCheck(CheckAbstract):

    id = "FORMAT_CHECK"
    name = "Format Check"
    category = None
    description = 'Check cell respects selected format'

    parameters = [
        CheckParam('regex', label='Format', type='select', options=[
            {'key': 'exp1', 'value':'n,nnn.nn'},
            {'key': 'exp2', 'value':'mm-dd-yyyy'},
            {'key': 'exp3', 'value':'(String)-(String)'},
        ]),
        CheckParam('custom', label='Custom Regex', type='checkbox')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]