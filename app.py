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

    query_for_min_num = "SELECT min(phonenumber) FROM people WHERE "
    query_for_search_results = "SELECT * FROM people WHERE "

    query_arguments = []

    if search_first_name:
        query_arguments.append(f"first_name='{search_first_name}'")

    if search_last_name:
        query_arguments.append(f"last_name='{search_last_name}'")

    if search_state:
        query_arguments.append(f"state='{search_state}'")

    query_arguments_string = " AND ".join(query_arguments)

    query_for_min_num += query_arguments_string

    print(query_for_min_num)

    db.row_factory = sqlite3.Row
    cur= db.cursor()

    min_phonenum = cur.execute(query_for_min_num)
    
    print(type(min_phonenum))
    print(min_phonenum.arraysize)
    print(type(cur.fetchone()[0]))

    query_for_search_results = query_for_search_results + query_arguments_string #+ " AND phonenumber >= :min_phonenum ORDER BY phonenumber LIMIT 5;"

    search_results = db.execute(query_for_search_results, {"min_phonenum": min_phonenum})
    search_results_list_of_dictionaries = [{k: item[k] for k in item.keys()} for item in search_results]

    return search_results_of_dictionaries

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
