from ariadne import ObjectType
from api.models import Author

def register_author_resolvers(author_type):
    @author_type.field("id")
    def resolve_author_id(author, info):
        return author.author_id
    
    @author_type.field("name")
    def resolve_author_name(author, info):
        return f"{author.first_name} {author.last_name}"