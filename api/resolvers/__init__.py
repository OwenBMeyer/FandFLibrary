from ariadne import QueryType, ObjectType

from api.resolvers.scalars import date_scalar
from api.resolvers.user import register_user_resolvers

query = QueryType()
user_type = ObjectType("User")

register_user_resolvers(query, user_type)

__all__ = ['query', 'user_type', 'date_scalar']
