from flask import Blueprint
from .home_page import home_bp
from .add_rishon_page import add_bp

app_routes = Blueprint('app_routes', __name__)
app_routes.register_blueprint(home_bp)
app_routes.register_blueprint(add_bp)
