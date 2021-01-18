import flask
from flask import request, jsonify
import sqlite3

app = flask.Flask(__name__)
app.config["DEBUG"] = True

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


@app.route('/', methods=['GET'])
def home():
    return '''<h1>Space flight API</h1>
<p>An API for Space flight.</p>'''


@app.route('/api/v1/launches/spacex/all', methods=['GET'])
def api_all():
    conn = sqlite3.connect('launches.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_books = cur.execute('SELECT * FROM SpaceX;').fetchall()

    return jsonify(all_books)



@app.errorhandler(404)
def page_not_found(e):
    return "<h1>404</h1><p>The resource could not be found.</p>", 404


@app.route('/api/v1/launches/spacex', methods=['GET'])
def api_filter():
    query_parameters = request.args

    id = query_parameters.get('id')
    unixtime = query_parameters.get('unix')
    localtime = query_parameters.get('local')

    query = "SELECT * FROM SpaceX WHERE"
    to_filter = []

    if id:
        query += ' id=? AND'
        to_filter.append(id)
    if unixtime:
        query += ' time-unix=? AND'
        to_filter.append(unixtime)
    if localtime:
        query += ' time-local=? AND'
        to_filter.append(localtime)
    if not (id or unixtime or localtime):
        return page_not_found(404)

    query = query[:-4] + ';'

    conn = sqlite3.connect('launches.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    results = cur.execute(query, to_filter).fetchall()

    return jsonify(results)

app.run()
