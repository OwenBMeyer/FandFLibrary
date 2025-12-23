from flask import Flask
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from ariadne import QueryType, ScalarType
from flask import request, jsonify
from datetime import datetime
from ariadne.explorer import ExplorerGraphiQL

app = Flask(__name__)
CORS(app)

type_defs = load_schema_from_path("gqlschema/schema.graphql")

date_scalar = ScalarType("Date")

@date_scalar.serializer
def serialize_date(value):
    if value:
        return datetime.fromtimestamp(value).isoformat()
    return None

@date_scalar.value_parser
def parse_date_value(value):
    if isinstance(value, int):
        return value
    if isinstance(value, str):
        return int(datetime.fromisoformat(value).timestamp())
    return None

query = QueryType()

@query.field("user")
def resolve_user(*_):
    # Fetch from db
    return {
        "id": "1",
        "username": "test_user",
        "region": {
            "id": "1",
            "population": 5,
            "num_books": 10,
            "users_in_region": [],
            "books_in_region": []
        },
        "date_joined": int(datetime.now().timestamp()),
        "books_owned": [],
        "books_borrowed_current": [],
        "books_lent_out": [],
        "reading_lists": [],
        "book_titles_owned": []
    }

schema = make_executable_schema(type_defs, query, date_scalar)

@app.route('/')
def hello():
    return 'API Call Baby!'

explorer_html = ExplorerGraphiQL().html("/graphql")

@app.route("/graphql", methods=["GET"])
def graphql_explorer():
    return explorer_html, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(schema, data, context_value=request)
    status_code = 200 if success else 400
    return jsonify(result), status_code

