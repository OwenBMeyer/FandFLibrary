from ariadne import ObjectType

def register_genre_resolvers(genre_type):

    @genre_type.field("id")
    def resolve_id(genre, info):
        return genre.genre_id

    @genre_type.field("name")
    def resolve_name(genre, info):
        return genre.name

    @genre_type.field("book_titles")
    def resolve_book_titles(genre, info):
        return genre.book_titles

    @genre_type.field("num_books")
    def num_books(genre, info):
        return genre.num_books
