from flask import jsonify, request
from ...bootstrap import api
from ...validator import validate_schema, validate_404
from ...models import (Article, User, Comment)


@api.route('/articles', methods=['POST'])
@validate_schema('articles.create')
@validate_404()
def article_create():
    content = request.json
    attributes = content.get('data').get('attributes')
    user_relationship = content.get('data').get('relationships').get('users').get('data')

    user = User.nodes.get(mid=user_relationship.get('id'))

    article = Article(title=attributes['title'], text=attributes['text'])
    article.save()
    article.user.connect(user)
    return jsonify({"data":{ "type":article.getType(), "id":article.getId(), "attributes":article.getAttributes()}}), 201



@api.route('/articles/<id>/comment', methods=['POST'])
@validate_schema('articles.create_comment')
@validate_404()
def create_article_comment(id):
    content = request.json
    attributes = content.get('data').get('attributes')
    user_relationship = content.get('data').get('relationships').get('users').get('data')

    article = Article.nodes.get(mid=id)
    user = User.nodes.get(mid=user_relationship.get('id'))

    comment = Comment(text=attributes['text'])
    comment.save()
    comment.user.connect(user)
    article.comments.connect(comment)
    return jsonify({"data":{ "type": comment.getType(), "attributes": comment.getAttributes()}}), 201



@api.route('/articles/<id>', methods=['GET'])
@validate_404()
def get_article(id):
    article = Article.nodes.get(mid=id)
    commentList =[]
    for comment in article.comments.all():
        commentList.append({"type":comment.getType(), "attributes": comment.getAttributes()})

    us = article.user.get()
    userItem = {"id":us.getId(),"type":us.getType(), "attributes":us.getAttributes()}
    return jsonify({"data":{"id":article.getId(),"type":article.getType(),"attributes":article.getAttributes(), "relationships":{"comments":{"data":commentList}, "user":{"data":userItem}}}}), 200

