from app.datacheck import CheckAbstract, CheckParam


class Check(CheckAbstract):

    id = "MAXIMUM_PROPERTY_CHECK"
    name = "Is Lower Than"
    category = None
    description = None

    parameters = [
        CheckParam('property', label='Target Field', type='property')
    ]

    def check_column(self, df, column, *args, **kwargs):
        return df[column]