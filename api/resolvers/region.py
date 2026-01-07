from ariadne import ObjectType
from api.models import Region, Book

def register_region_resolvers(region_type):

    @region_type.field("id")
    def resolve_region_id(region, info):
        return str(region.region_id)
    
    # Number of books in the region
    @region_type.field("num_books")
    def resolve_num_books(region, info):
        total_books = 0
        for user in region.users:
            total_books += len(user.books)
        return total_books
    
    # All books in the region
    @region_type.field("books_in_region")
    def resolve_books_in_region(region, info):
        # Collect all books from all users in this region
        books = []
        for user in region.users:
            books.extend(user.books)
        return books
