from ariadne import QueryType, ObjectType

from api.resolvers.scalars import date_scalar
from api.resolvers.user import register_user_resolvers
from api.resolvers.book import register_book_resolvers
from api.resolvers.genre import register_genre_resolvers

query = QueryType()
user_type = ObjectType("User")
book_type = ObjectType("Book")
genre_type = ObjectType("Genre")

register_user_resolvers(query, user_type)
register_book_resolvers(query, book_type)
register_genre_resolvers(genre_type)

__all__ = ['query', 'user_type', 'book_type', 'genre_type', 'date_scalar']
