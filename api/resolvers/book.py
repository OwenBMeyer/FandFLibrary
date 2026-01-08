from ariadne import ObjectType
from api.models import Book
from api.database import db

def register_book_resolvers(query, book_type):

    @query.field("book")
    def resolve_book(_, info, id):
        book = db.session.get(Book, int(id))
        if not book:
            raise Exception(f"Book with id {id} not found")
        return book

    @book_type.field("id")
    def resolve_book_id(book, info):
        return book.book_id

    @book_type.field("title")
    def resolve_book_title(book, info):
        return book.title.book_title_name if book.title else None

    @book_type.field("author")
    def resolve_book_author(book, info):
        # TODO: Make this returnable as a list of authors. Kind of silly not to have thought of this
        if book.title and book.title.authors:
            author = book.title.authors[0]
            return f"{author.first_name} {author.last_name}"
        return None

    @book_type.field("author_id")
    def resolve_book_author_id(book, info):
        # TODO: Make this returnable as a list of author IDs. Like todo in resolve_book_author()
        if book.title and book.title.authors:
            return book.title.authors[0]
        return None

    @book_type.field("date_of_publication")
    def resolve_date_of_publication(book, info):
        return book.title.date_of_publication if book.title else None

    @book_type.field("title_id")
    def resolve_book_title_id(book, info):
        return book.title

    @book_type.field("scheduled_return_time")
    def resolve_scheduled_return_time(book, info):
        # Seems like a bad way to do this. Look into books having a field that
        # links to their most recent lending record and updating it every so often
        #   (bad practice or clever?)
        for record in book.lending_records:
            if record.actively_borrowed:
                return record.borrowed_end
        return None

    @book_type.field("genres")
    def resolve_genres(book, info):
        return book.title.genres if book.title else []
