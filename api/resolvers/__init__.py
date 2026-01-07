from ariadne import QueryType, ObjectType

from api.resolvers.scalars import date_scalar
from api.resolvers.user import register_user_resolvers
from api.resolvers.book import register_book_resolvers
from api.resolvers.genre import register_genre_resolvers
from api.resolvers.lendingRecord import register_lending_record_resolvers
from api.resolvers.region import register_region_resolvers
from api.resolvers.bookTitle import register_book_title_resolvers
from api.resolvers.author import register_author_resolvers
from api.resolvers.readingList import register_reading_list_resolvers

query = QueryType()
user_type = ObjectType("User")
book_type = ObjectType("Book")
genre_type = ObjectType("Genre")
lending_record_type = ObjectType("Lending_Record")
region_type = ObjectType("Region")
book_title_type = ObjectType("Book_Title")
author_type = ObjectType("Author")
reading_list_type = ObjectType("Reading_List")

register_user_resolvers(query, user_type)
register_book_resolvers(query, book_type)
register_genre_resolvers(genre_type)
register_lending_record_resolvers(lending_record_type)
register_region_resolvers(region_type)
register_book_title_resolvers(book_title_type)
register_author_resolvers(author_type)
register_reading_list_resolvers(reading_list_type)

__all__ = [
    'query', 'user_type', 'book_type', 
    'genre_type', 'lending_record_type', 
    'region_type', 'book_title_type', 
    'author_type', 'reading_list_type', 
    'date_scalar']
