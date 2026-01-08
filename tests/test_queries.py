"""
Tests for GraphQL queries.
"""
import pytest
from ariadne import graphql_sync


def test_user_query(schema, sample_data):
    """Test querying a user by ID"""
    query = """
    query {
        user(id: "1") {
            id
            username
            date_joined
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert result['data']['user']['id'] == "1"
    assert result['data']['user']['username'] == "testuser"
    assert result['data']['user']['date_joined'] == 1234567890


def test_user_with_books_owned(schema, sample_data):
    """Test querying a user with their books"""
    query = """
    query {
        user(id: "1") {
            id
            username
            books_owned {
                id
                title
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert len(result['data']['user']['books_owned']) == 1
    assert result['data']['user']['books_owned'][0]['id'] == "1"
    assert result['data']['user']['books_owned'][0]['title'] == "Test Book"


def test_user_not_found(schema):
    """Test querying a non-existent user"""
    query = """
    query {
        user(id: "999") {
            id
            username
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' in result
    assert 'not found' in result['errors'][0]['message'].lower()


def test_book_query(schema, sample_data):
    """Test querying a book by ID"""
    query = """
    query {
        book(id: "1") {
            id
            title
            is_lendable
            owner {
                username
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert result['data']['book']['id'] == "1"
    assert result['data']['book']['title'] == "Test Book"
    assert result['data']['book']['is_lendable'] is True
    assert result['data']['book']['owner']['username'] == "testuser"


def test_book_with_author(schema, sample_data):
    """Test querying a book with author information"""
    query = """
    query {
        book(id: "1") {
            id
            title
            author
            author_id {
                id
                name
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert result['data']['book']['author'] == "John Doe"
    assert result['data']['book']['author_id']['name'] == "John Doe"


def test_book_not_found(schema):
    """Test querying a non-existent book"""
    query = """
    query {
        book(id: "999") {
            id
            title
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' in result
    assert 'not found' in result['errors'][0]['message'].lower()


def test_user_region_relationship(schema, sample_data):
    """Test user-region relationship"""
    query = """
    query {
        user(id: "1") {
            id
            region {
                id
                population
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert result['data']['user']['region']['id'] == "1"
    assert result['data']['user']['region']['population'] == 100


def test_user_books_borrowed_current_empty(schema, sample_data):
    """Test books_borrowed_current when user has no active loans"""
    query = """
    query {
        user(id: "1") {
            id
            books_borrowed_current {
                id
            }
        }
    }
    """
    
    success, result = graphql_sync(schema, {"query": query}, context_value={})
    
    assert success is True
    assert 'errors' not in result
    assert result['data']['user']['books_borrowed_current'] == []
