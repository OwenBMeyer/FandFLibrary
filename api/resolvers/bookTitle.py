from ariadne import ObjectType
from api.models import BookTitle

def register_book_title_resolvers(book_title_type):
    @book_title_type.field("id")
    def resolve_book_title_id(book_title, info):
        return book_title.book_title_id
    
    @book_title_type.field("author")
    def resolve_book_title_author(book_title, info):
        authors = []
        for author in book_title.authors:
            authors.append(f"{author.first_name} {author.last_name}")
        return ", ".join(authors) if authors else "No authors found"
    
    @book_title_type.field("author_id")
    def resolve_book_title_author_id(book_title, info):
        return book_title.authors
    