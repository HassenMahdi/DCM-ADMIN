from app.datacheck import CheckAbstract, CheckParam


class DoubleOperation(CheckAbstract):

    id = "NUMERIC_BOUNDRY"
    name = "Numeric Boundry Value Check"
    category = None
    description = None
    property_types = ['double', 'int']

    parameters = [
        CheckParam('operator', label='Operator', type='select', options=[
            {'key': '<', 'value': 'Lesser'},
            {'key': '<=', 'value': 'Lesser or equal'},
            {'key': '>', 'value': 'Greater'},
            {'key': '>=', 'value': 'Greater or equal'},
        ]),
        CheckParam('operand', label='Value', type='number')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]