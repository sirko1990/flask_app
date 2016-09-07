from neomodel import (StructuredNode, StringProperty, IntegerProperty,
    RelationshipTo, RelationshipFrom, db)
from uuid import uuid4
from .attributeInterface import ModelDetailsinterface

class User(StructuredNode, ModelDetailsinterface):
    name = StringProperty()
    age = IntegerProperty(default=0)
    mid = StringProperty(unique=True, default=uuid4)
    comments = RelationshipFrom('Comment', 'COMMENTED_BY')
    articles = RelationshipFrom('Article', 'CREATED_BY')

    @classmethod
    def all(cls):
         results, columns = db.cypher_query("MATCH (n:User) RETURN n")
         return [cls.inflate(row[0]) for row in results]

    def getAttributes(self):
        return {"name": self.name, "age": self.age}

    def getId(self):
        return self.mid

    def getType(self):
        return "users"

class Comment(StructuredNode, ModelDetailsinterface):
    text = StringProperty()
    user = RelationshipTo(User, 'COMMENTED_BY')

    def getAttributes(self):
        return {"text": self.text}

    def getType(self):
        return "comments"


class Article(StructuredNode, ModelDetailsinterface):
    title = StringProperty()
    text = StringProperty()
    mid = StringProperty(unique=True, default=uuid4)
    user = RelationshipTo(User, 'CREATED_BY')
    comments = RelationshipFrom('Comment', 'COMMENTED')

    @classmethod
    def all(cls):
         results, columns = db.cypher_query("MATCH (n:Article) RETURN n")
         return [cls.inflate(row[0]) for row in results]

    def getAttributes(self):
        return {"title": self.title, "text": self.text}

    def getId(self):
        return self.mid

    def getType(self):
        return "articles"