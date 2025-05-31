from flask import Blueprint

from .add_book_page import add_book_bp
from .home_page import home_bp
from .search_by_book_page import search_by_book_bp
from .add_rishon_page import add_bp
from .search_by_rishon_page import search_by_rishon_bp

app_routes = Blueprint('app_routes', __name__)
app_routes.register_blueprint(home_bp)
app_routes.register_blueprint(search_by_book_bp)
app_routes.register_blueprint(add_bp)
app_routes.register_blueprint(search_by_rishon_bp)
app_routes.register_blueprint(add_book_bp)


