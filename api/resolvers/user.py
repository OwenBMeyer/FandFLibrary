from api.models import User

def register_user_resolvers(query):

    @query.field("user")
    def resolve_user(_, info, id):
        # TODO: Once login sessions implemented:
        # user_id = info.context.get('user_id')
        # user = User.query.get(user_id)
        
        user = User.query.get(id)
        if not user:
            raise Exception(f"User with with id {id} not found")

        return user

    @query.field("books_owned")
    def resolve_books_owned(_, info, id):
        # TODO: Once login session implemented delete id

        user = User.query.get(id)
        if not user:
            raise Exception(f"User with with id {id} not found")

        return user.books
