from ariadne import ObjectType
from api.models import ReadingList

def register_reading_list_resolvers(reading_list_type):
    @reading_list_type.field("id")
    def resolve_reading_list_id(reading_list, info):
        return reading_list.reading_list_id
    
    @reading_list_type.field("books")
    def resolve_reading_list_books(reading_list, info):
        return reading_list.book_titles