from app.datacheck import CheckAbstract, CheckParam


class DoublePropertyOperation(CheckAbstract):

    id = "PROPERTY_BOUNDRY_CHECK"
    name = "Property Boundry Value Check"
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
        CheckParam('property', label='Target Field', type='property'),
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]