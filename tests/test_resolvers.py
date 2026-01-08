"""
Tests for individual GraphQL resolvers.
"""
import pytest
from ariadne import graphql_sync


def test_user_id_resolver(schema, sample_data):
    """Test that user id resolver returns string"""
    query = """
    query {
        user(id: "1") {
            id
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['user']['id'] == "1"
    assert isinstance(result['data']['user']['id'], str)


def test_user_books_owned_resolver(schema, sample_data):
    """Test books_owned resolver returns list of books"""
    query = """
    query {
        user(id: "1") {
            books_owned {
                id
                title
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert len(result['data']['user']['books_owned']) == 1
    assert result['data']['user']['books_owned'][0]['id'] == "1"
    assert result['data']['user']['books_owned'][0]['title'] == "Test Book"


def test_book_id_resolver(schema, sample_data):
    """Test that book id resolver returns string"""
    query = """
    query {
        book(id: "1") {
            id
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['book']['id'] == "1"
    assert isinstance(result['data']['book']['id'], str)


def test_book_title_resolver(schema, sample_data):
    """Test book title resolver"""
    query = """
    query {
        book(id: "1") {
            title
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['book']['title'] == "Test Book"


def test_book_author_resolver(schema, sample_data):
    """Test book author resolver"""
    query = """
    query {
        book(id: "1") {
            author
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['book']['author'] == "John Doe"


def test_region_id_resolver(schema, sample_data):
    """Test region id resolver returns string"""
    query = """
    query {
        user(id: "1") {
            region {
                id
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['user']['region']['id'] == "1"
    assert isinstance(result['data']['user']['region']['id'], str)


def test_region_num_books_resolver(schema, sample_data):
    """Test region num_books resolver"""
    query = """
    query {
        user(id: "1") {
            region {
                num_books
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['user']['region']['num_books'] == 1


def test_author_id_resolver(schema, sample_data):
    """Test author id resolver returns string"""
    query = """
    query {
        book(id: "1") {
            author_id {
                id
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['book']['author_id']['id'] == "1"
    assert isinstance(result['data']['book']['author_id']['id'], str)


def test_author_name_resolver(schema, sample_data):
    """Test author name resolver"""
    query = """
    query {
        book(id: "1") {
            author_id {
                name
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert result['data']['book']['author_id']['name'] == "John Doe"