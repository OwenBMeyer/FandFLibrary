from flask import Flask
from flask_cors import CORS
from ariadne import load_schema_from_path, make_executable_schema, graphql_sync
from flask import request, jsonify
from datetime import datetime
from ariadne.explorer import ExplorerGraphiQL

from api.database import db
from api.resolvers import query, user_type, book_type, date_scalar, genre_type
from api import models

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///../FaFLib.db"

db.init_app(app)

CORS(app)

type_defs = load_schema_from_path("gqlschema/schema.graphql")

schema = make_executable_schema(type_defs, query, user_type, book_type, genre_type, date_scalar)


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

