from ariadne import QueryType, ObjectType
from api.models import User

def register_user_resolvers(query, user_type):

    @query.field("user")
    def resolve_user(_, info, id):
        # TODO: Once login sessions implemented:
        # user_id = info.context.get('user_id')
        # user = User.query.get(user_id)

        user = User.query.get(int(id))
        if not user:
            raise Exception(f"User with with id {id} not found")

        return user

    @user_type.field("id")
    def resolve_user_id(user, info):
        return user.user_id

    @user_type.field("books_owned")
    def resolve_books_owned(user, info):
        # TODO: Once login session implemented delete id
        return user.books
