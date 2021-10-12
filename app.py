from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

def dictionary_factory(db, row):
    return {
        "first_name": row[0],
        "last_name": row[1],
        "state": row[2],
        "phonenumber": row[3],
        "email": row[4]
    }

def search_phone_book(**kwargs):
    db = sqlite3.connect("phonebook.db")
    
    search_first_name = kwargs.get("first_name")
    search_last_name = kwargs.get("last_name")
    search_state = kwargs.get("state")

    if not any([search_first_name, search_last_name, search_state]):
        return []

    query = "SELECT * FROM people WHERE "

    query_arguments = []
    query_parameters = dict()

    if search_first_name:
        query_arguments.append("first_name=:search_first_name")
        query_parameters['search_first_name'] = search_first_name


    if search_last_name:
        query_arguments.append("last_name=:search_last_name")
        query_parameters['search_last_name'] = search_last_name

    if search_state:
        query_arguments.append("state=:search_state")
        query_parameters['search_state'] = search_state

    query += " AND ".join(query_arguments)

    db.row_factory = dictionary_factory

    return list(db.execute(query, query_parameters))

@app.route("/search/", methods=['GET'])
def search_phonebook():
    first_name = request.args.get("firstName")
    last_name = request.args.get("lastName")
    state = request.args.get("state")

    if not any([first_name, last_name, state]):
        return jsonify({"error": "At least one of the three fields must be filled."}), 400

    search_results = search_phone_book(
        first_name=first_name, 
        last_name=last_name, 
        state=state
    )

    return jsonify(search_results)

if __name__ == "__main__":
    app.run(debug=True, port=8080, threaded=True)
