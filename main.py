import os

from flask import Flask
from routes import app_routes

app = Flask(__name__)
app.secret_key = 'your-secret-key'

app.register_blueprint(app_routes, url_prefix='/app')

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
