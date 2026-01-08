from ariadne import QueryType, ObjectType
from api.models import User, LendingRecord
from api.database import db

def register_user_resolvers(query, user_type):

    @query.field("user")
    def resolve_user(_, info, id):
        # TODO: Once login sessions implemented:
        # user_id = info.context.get('user_id')
        # user = User.query.get(user_id)

        user = db.session.get(User, int(id))
        if not user:
            raise Exception(f"User with id {id} not found")

        return user

    @user_type.field("id")
    def resolve_user_id(user, info):
        return user.user_id

    @user_type.field("books_owned")
    def resolve_books_owned(user, info):
        # TODO: Once login session implemented delete id
        return user.books

    # TODO: Think more about region logic. 
    @user_type.field("region")
    def resolve_region(user, info):
        return user.region
    
    @user_type.field("books_borrowed_current")
    def resolve_books_borrowed_current(user, info):
        active_loans = LendingRecord.query.filter_by(
            borrower_id=user.user_id,
            actively_borrowed=True
        ).all()

        return [loan.book for loan in active_loans]

    @user_type.field("books_lent_out")
    def resolve_books_lent_out(user, info):
        return [book for book in user.books if book.is_being_lent]

    @user_type.field("reading_lists")
    def resolve_reading_lists(user, info):
        return user.reading_lists

    @user_type.field("book_titles_owned")
    def resolve_book_titles_owned(user, info):
        titles = {}
        for book in user.books:
            if book.title:
                titles[book.title.book_title_id] = book.title
        return list(titles.values())
