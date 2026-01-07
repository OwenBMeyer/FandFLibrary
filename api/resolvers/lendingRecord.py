from ariadne import ObjectType
from api.models import LendingRecord

def register_lending_record_resolvers(lending_record_type):
    @lending_record_type.field("id")
    def resolve_lending_record_id(lending_record, info):
        return str(lending_record.lending_record_id)
   