from app.datacheck import CheckAbstract, CheckParam


class DateComparison(CheckAbstract):

    id = "DATE_BOUNDRY_CHECK"
    name = "Date Boundry Value Check"
    category = None
    description = None
    property_types = ['date']

    parameters = [
        CheckParam('operator', label='Operator', type='select', options=[
            {'key': '<', 'value': '<'},
            {'key': '>', 'value': '>'}
        ]),
        CheckParam('operand', label='Date', type='date')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]