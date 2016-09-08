from flask import jsonify, request
from ...bootstrap import api
from ...validator import validate_schema, validate_404
from ...models import (User, Comment)



@api.route('/users', methods=['POST'])
@validate_schema('users.create')
def create():
    content = request.json
    attributes = content.get('data').get('attributes')
    user = User(name=attributes['name'], age=attributes['age'])
    user.save()
    return jsonify({"data":{ "type": user.getType(), "id":user.getId(), "attributes": user.getAttributes()}}), 201



@api.route('/users/<id>', methods=['PATCH'])
@validate_schema('users.update')
@validate_404()
def update(id):
    content = request.json
    attributes = content.get('data').get('attributes')
    user = User.nodes.get(mid=id)
    user.name = attributes["name"]
    user.age = attributes["age"]
    user.save()
    return jsonify({"data": {"type":user.getType(), "id":user.getId(), "attributes": user.getAttributes()}}), 202



@api.route('/users/<id>', methods=['DELETE'])
@validate_404()
def delete(id):
    user = User.nodes.get(mid=id)
    print user.delete()
    return "", 204



@api.route('/users', methods=['GET'])
def get_all():
    collection = []
    users = User.all()
    for user in users:
        collection.append({"type":user.getType(), "id":user.getId(), "attributes":user.getAttributes()})
    return jsonify({"data":collection}), 200



@api.route('/users/<id>', methods=['GET'])
@validate_404()
def get(id):
     user = User.nodes.get(mid=id)
     commentList =[]
     for comment in user.comments.all():
         commentList.append({"type":comment.getType(), "attributes": comment.getAttributes()})
     return jsonify({"data":{"type":user.getType(), "id": user.getId(), "attributes": user.getAttributes()}, "relationships": {"comments":{"data": commentList}}}), 200