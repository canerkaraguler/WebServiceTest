from flask import Flask, jsonify, abort, make_response, request
from flask_httpauth import HTTPBasicAuth
from Table2 import Table2
from DTO.userDTO import userDTO
import json


auth = HTTPBasicAuth()
authAdmin = HTTPBasicAuth()


@auth.get_password
def get_password(username):
    if databaseObj.CheckUserExistance(username) is not None:
        passw = databaseObj.GetPassword(username)[0]

        return passw
    return None


@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized access'}), 401)


@authAdmin.get_password
def get_password(username):
    if databaseObj.CheckAdminExistance(username) is not None:
        passw = databaseObj.GetPassword(username)[0]

        return passw
    return None


@authAdmin.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Admin access'}), 401)


app = Flask(__name__)

databaseObj = Table2()


@app.route('/api/users/register', methods=['POST'])
def new_user():
    user = userDTO(request.json.get('username'), request.json.get('password'), request.json.get('userId'),
                   request.json.get('admin'))

    if user.username is None or user.password is None:
        abort(400)  # missing arguments

    if databaseObj.CheckUserExistance(user.username) is not None:
        return jsonify({'Message': 'existing user'}), 400  # existing user

    else:
        databaseObj.CreateNewUser(user)

    return jsonify({'tasks': 'done'}), 201


@app.route('/api/get/<database_name>/<table_name>', methods=['GET'])
@authAdmin.login_required
def get_all_info(database_name, table_name):
    response = databaseObj.GetAllInfo(database_name, table_name)

    return jsonify({'Data': response}), 201


@app.route('/api/create/<database_name>/<table_name>', methods=['POST'])
@authAdmin.login_required
def create_database(database_name, table_name):
    if not request.json:
        abort(400)

    clones = json.loads(json.dumps(request.json))

    databaseObj.CreateDatabaseRelatedToJson(database_name, table_name, clones)
    return jsonify({'Message': 'Database and table created.'}), 201


@app.route('/api/fill/<database_name>/<table_name>', methods=['POST'])
@auth.login_required
def create_table(database_name, table_name):  #isim düzeltilcek
    if not request.json:
        abort(400)

    clones = json.loads(json.dumps(request.json))

    databaseObj.AddItemToDatabase(database_name, table_name, clones)
    return jsonify({'Message': 'Table filled.'}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host='127.0.0.1', port=8080)
