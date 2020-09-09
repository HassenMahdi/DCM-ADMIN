from app.datacheck import CheckAbstract, CheckParam


class Check(CheckAbstract):

    id = "MINIMUM_PROPERTY_CHECK"
    name = "Is Greater Than"
    category = None
    description = None

    parameters = [
        CheckParam('property', label='Target Field', type='property')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]