from flask import Blueprint

matches_bp = Blueprint('matches_bp', __name__)

from . import routes