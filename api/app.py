from flask import Flask, jsonify, request
from flask_swagger_ui import get_swaggerui_blueprint
from flask_cors import CORS
import create_db

import sqlite3

app = Flask(__name__)
CORS(app)

SWAGGER_URL = '/api/docs'
API_URL = '/static/swagger.json'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': "Python Tech Test API"
    }
)
app.register_blueprint(swaggerui_blueprint)

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

# TODO - you will need to implement the other endpoints
# GET /api/person/{id} - get person with given id
# POST /api/people - create 1 person
# PUT /api/person/{id} - Update a person with the given id
# DELETE /api/person/{id} - Delete a person with a given id

@app.route("/api/people")
def getall_people():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    all_people = cur.execute('SELECT * FROM Person;').fetchall()

    return jsonify(all_people)

@app.route('/api/person/<id>', methods=['GET'])
def get_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query1 = f"SELECT * FROM Person WHERE id={id};"
    person = cur.execute(query1).fetchone()

    cur.close()
    conn.close()

    return jsonify(person)

@app.route('/api/people', methods=['POST'])
def post_person():
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()
    
    person = (request.json['id'], request.json['firstName'], request.json['lastName'], request.json['authorised'], request.json['enabled'])

    print('Inserting data into tables')
    cur.execute('INSERT INTO Person(id, firstName, lastName, authorised, enabled) VALUES(?, ?, ?, ?, ?)', person)
    print('Finished inserting data into tables')
    conn.commit()
    cur.close()
    conn.close()
    print('Connection closed')

    return "added"

@app.route('/api/person/<id>', methods=['PUT'])
def update_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    pid = request.json['id']
    firstName = request.json['firstName']
    lastName = request.json['lastName']
    authorised = request.json['authorised']
    enabled = request.json['enabled']

    query1 = f"UPDATE Person SET id = {pid}, firstName = '{firstName}', lastName = '{lastName}', authorised = {authorised}, enabled = {enabled} WHERE id={id};"

    print('updating data into tables')
    cur.execute(query1)
    print('Finished updating data into tables')
    conn.commit()
    cur.close()
    conn.close()
    print('Connection closed')

    return "updated"

@app.route('/api/person/<id>', methods=['DELETE'])
def delete_person(id):
    conn = sqlite3.connect('test.db')
    conn.row_factory = dict_factory
    cur = conn.cursor()

    query1 = f"DELETE FROM Person WHERE id={id};"

    print('deleting data from tables')
    cur.execute(query1)
    print('Finished deleting data from tables')
    conn.commit()
    cur.close()
    conn.close()
    print('Connection closed')

    return "deleted"

if __name__ == '__main__':
    app.run()
