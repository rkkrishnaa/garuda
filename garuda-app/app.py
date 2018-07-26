#/usr/bin/python

from uuid import uuid1
from datetime import datetime
import json
from flask import Flask
from flask_pymongo import PyMongo
from flask import request
from pymongo import MongoClient
from flask import render_template
from flask import Response
from flask import jsonify

mongo_host = 'host'
mongo_port = 'port'
mongo_db_name = 'garuda'
#client = MongoClient(mongo_host+':'+mongo_port)
#db = client.garuda

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://' + mongo_host + ':' + mongo_port + '/' + mongo_db_name
mongo = PyMongo(app)

#user management
@app.route('/user/', methods=['POST'])
def create():
    username = request.data
    user = json.loads(username, encoding='utf-8')
    uuid = uuid1().hex
    try:
        user['userid'] = uuid
        created_at = datetime.utcnow()
        user['created_at'] = created_at
        user['updated_at'] = created_at
        user['status'] = 'active'
        #users = db.user.insert_one(user)
        users = mongo.db.user.insert_one(user)
        response_body = {'userid': str(uuid), 'created at': str(created_at)}
        response = app.response_class(
            response=json.dumps(response_body, indent=2),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        print(e)

@app.route('/user/', methods=['GET'])
def list():
    users = mongo.db.user.find()
    user_list = []
    for user in users:
        user_dict = {}
        user_dict['username'] = user['username']
        user_dict['userid'] = user['userid']
        user_dict['email'] = user['email']
        user_dict['status'] = user['status']
        user_dict['description'] = user['description']
        user_dict['created_at'] = str(user['created_at'])
        user_dict['updated_at'] =  str(user['updated_at'])
        user_dict['projects'] = None
        user_dict['last_login'] = None
        user_dict['last_activity'] = None
        user_list.append(user_dict)

    response = app.response_class(
        response=json.dumps(user_list, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/user/<uuid>/', methods=['GET'])
def show(uuid):
    users = mongo.db.user.find({"userid": uuid})
    for user in users:
        user_dict = {}
        user_dict['username'] = user['username']
        user_dict['userid'] = user['userid']
        user_dict['email'] = user['email']
        user_dict['status'] = user['status']
        user_dict['description'] = user['description']
        user_dict['created_at'] = str(user['created_at'])
        user_dict['updated_at'] = str(user['updated_at'])
        user_dict['projects'] = None
        user_dict['last_login'] = None
        user_dict['last_activity'] = None
    response = app.response_class(
        response=json.dumps(user_dict, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )

    return response

@app.route('/user/<uuid>/', methods=['PUT'])
def update(uuid):
    return ''

@app.route('/user/<uuid>/', methods=['DELETE'])
def delete(uuid):
    try:
        #validate the existence of uuid
        user = {}
        user['updated_at'] = datetime.utcnow()

        #users = db.user.update_one(user)
        response = 'test delete'
        return response
    except:
        pass


#project management
@app.route('/project/', methods=['POST'])
def create_project():
    request_data = request.get_json()
    project = {}
    uuid = uuid1().hex
    try:
        project['projectid'] = uuid
        project['owner'] = request_data['userid']
        project['description'] = request_data['description']
        project['project_name'] = request_data['projectname']
        created_at = datetime.utcnow()
        project['created_at'] = created_at
        project['updated_at'] = created_at
        project['status'] = 'active'
        projects = mongo.db.project.insert_one(project)
        response_body = {'projectid': str(uuid), 'created at': str(created_at)}
        response = app.response_class(
            response=json.dumps(response_body, indent=2),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        print(e)

@app.route('/project/', methods=['GET'])
def list_project():
    projects = mongo.db.project.find()
    project_list = []
    for project in projects:
        project_dict = {}
        project_dict['project_name'] = project['project_name']
        project_dict['projectid'] = project['projectid']
        project_dict['owner'] = project['owner']
        project_dict['status'] = project['status']
        project_dict['description'] = project['description']
        project_dict['created_at'] = str(project['created_at'])
        project_dict['updated_at'] = str(project['updated_at'])
        project_dict['hosts'] = None
        project_list.append(project_dict)

    response = app.response_class(
        response=json.dumps(project_list, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/project/<projectid>/', methods=['GET'])
def show_project(projectid):
    projects = mongo.db.project.find({"projectid": projectid})
    for project in projects:
        project_dict = {}
        project_dict['project_name'] = project['project_name']
        project_dict['projectid'] = project['projectid']
        project_dict['owner'] = project['owner']
        project_dict['status'] = project['status']
        project_dict['description'] = project['description']
        project_dict['created_at'] = str(project['created_at'])
        project_dict['updated_at'] = str(project['updated_at'])
        project_dict['hosts'] = None

    response = app.response_class(
        response=json.dumps(project_dict, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/project/<projectid>/', methods=['PUT'])
def update_project(projectid):
    return ''

@app.route('/project/<projectid>/', methods=['DELETE'])
def delete_project(projectid):
    try:
        #validate the existence of uuid
        project = {}
        project['updated_at'] = datetime.utcnow()

        #users = db.user.update_one(user)
        response = 'test delete'
        return response
    except:
        pass

###
#host management
@app.route('/host/', methods=['POST'])
def create_host():
    request_data = request.get_json()
    host = {}
    uuid = uuid1().hex
    try:
        host['hostid'] = uuid
        host['owner'] = request_data['userid']
        host['hostname'] = request_data['hostname']
        host['description'] = request_data['description']
        host['project_id'] = request_data['projectid']
        created_at = datetime.utcnow()
        host['created_at'] = created_at
        host['updated_at'] = created_at
        host['status'] = 'active'
        host = mongo.db.host.insert_one(host)
        response_body = {'hostid': str(uuid), 'created at': str(created_at)}
        response = app.response_class(
            response=json.dumps(response_body, indent=2),
            status=200,
            mimetype='application/json'
        )
        return response
    except Exception as e:
        print(e)

@app.route('/host/', methods=['GET'])
def list_host():
    hosts = mongo.db.host.find()
    host_list = []
    for host in hosts:
        host_dict = {}
        host_dict['hostname'] = host['hostname']
        host_dict['hostid'] = host['hostid']
        host_dict['owner'] = host['owner']
        host_dict['status'] = host['status']
        host_dict['description'] = host['description']
        host_dict['created_at'] = str(host['created_at'])
        host_dict['updated_at'] = str(host['updated_at'])
        host_list.append(host_dict)

    response = app.response_class(
        response=json.dumps(host_list, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/host/<hostid>/', methods=['GET'])
def show_host(hostid):
    hosts = mongo.db.host.find({"hostid": hostid})
    for host in hosts:
        host_dict = {}
        host_dict['hostname'] = host['hostname']
        host_dict['hostid'] = host['hostid']
        host_dict['owner'] = host['owner']
        host_dict['status'] = host['status']
        host_dict['description'] = host['description']
        host_dict['created_at'] = str(host['created_at'])
        host_dict['updated_at'] = str(host['updated_at'])

    response = app.response_class(
        response=json.dumps(host_dict, encoding='utf-8'),
        status=200,
        mimetype='application/json'
    )
    return response

@app.route('/host/<hostid>/', methods=['PUT'])
def update_host(hostid):
    return ''

@app.route('/host/<hostid>/', methods=['DELETE'])
def delete_host(hostid):
    try:
        #validate the existence of uuid
        host = {}
        host['updated_at'] = datetime.utcnow()

        response = 'test delete'
        return response
    except:
        pass


if __name__ == '__main__':
    app.run()
