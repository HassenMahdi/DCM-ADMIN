from .default.double_property_compare import DoublePropertyOperation
from .default.empty import EmptyCheck
from .default.format import FormatCheck
from .default.ref import ReferenceCheck
from .default.date_compare import DateComparison
from .default.double_compare import DoubleOperation

default_checks = [
    DateComparison(),
    DoubleOperation(),
    DoublePropertyOperation(),
    EmptyCheck(),
    FormatCheck(),
    ReferenceCheck()
]
