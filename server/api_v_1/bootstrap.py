from flask import Blueprint

api = Blueprint("api", __name__)

from resourses.users import users
from resourses.articles import articles