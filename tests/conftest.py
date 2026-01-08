"""
Test configuration and fixtures for the FandFLibrary project.
"""
import pytest
from api import app, db
from api.models import (
    User, Book, BookTitle, Author, Region, UserInfo, 
    Genre, ReadingList, LendingRecord
)

@pytest.fixture(scope='function')
def test_app():
    """Create a test Flask application"""
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(test_app):
    """Create a test client"""
    return test_app.test_client()

@pytest.fixture
def sample_data(test_app):
    """Create sample test data for testing"""
    with test_app.app_context():
        # Create test region
        region = Region(
            region_id=1,
            region_name='Test City',
            zipcode=12345,
            population=100
        )
        db.session.add(region)
        
        # Create test user info
        user_info = UserInfo(
            user_info_id=1,
            first_name='Test',
            last_name='User',
            email='test@example.com',
            password='password',
            is_active=True
        )
        db.session.add(user_info)
        
        # Create test user
        user = User(
            user_id=1,
            username='testuser',
            user_info_id=1,
            region_id=1,
            date_joined=1234567890,
            books_borrowed_current=0,
            books_borrowed_lifetime=0,
            books_owned=1
        )
        db.session.add(user)
        
        # Create test author
        author = Author(
            author_id=1,
            first_name='John',
            last_name='Doe',
            birthyear=1980
        )
        db.session.add(author)
        
        # Create test genre
        genre = Genre(
            genre_id=1,
            genre_name='Fiction',
            count_books=1
        )
        db.session.add(genre)
        
        # Create test book title
        book_title = BookTitle(
            book_title_id=1,
            book_title_name='Test Book',
            date_of_publication=2020
        )
        book_title.authors.append(author)
        book_title.genres.append(genre)
        db.session.add(book_title)
        
        # Create test book
        book = Book(
            book_id=1,
            owner_id=1,
            title_id=1,
            date_added=1234567890,
            times_borrowed=0,
            is_lendable=True,
            is_being_lent=False,
            quality='Good'
        )
        db.session.add(book)
        
        db.session.commit()
        
        return {
            'user': user,
            'book': book,
            'book_title': book_title,
            'author': author,
            'region': region,
            'genre': genre,
            'user_info': user_info
        }

@pytest.fixture
def schema(test_app):
    """Get the GraphQL schema"""
    with test_app.app_context():
        from ariadne import load_schema_from_path, make_executable_schema
        from api.resolvers import (
            query, user_type, book_type, genre_type, lending_record_type,
            region_type, book_title_type, author_type, reading_list_type,
            date_scalar
        )
        
        type_defs = load_schema_from_path("gqlschema/schema.graphql")
        graphql_schema = make_executable_schema(
            type_defs, query, user_type, book_type, genre_type,
            lending_record_type, region_type, book_title_type,
            author_type, reading_list_type, date_scalar
        )
        return graphql_schema
