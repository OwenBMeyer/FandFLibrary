from ariadne import QueryType

from api.resolvers.scalars import date_scalar
from api.resolvers.user import register_user_resolvers

query = QueryType()

register_user_resolvers(query)

__all__ = ['query', 'date_scalar']
