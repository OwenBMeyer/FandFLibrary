from ariadne import ScalarType
from datetime import datetime

date_scala = ScalarType("Date")

@date_scalar.serializer
def serialize_date(value):
    if value:
        return datetime.fromtimestamp(value).isoformat()
    return None

@date_scalar.value_parser
def parse_date_value(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(datetime.fromisoformat(value).timestamp())
    return None


