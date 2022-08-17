from flask import Flask

# app test client
def create_app(config):
    app = Flask(__name__)
    app.config.from_object(config)

    @app.route('/index')
    def index():
        return 'Hello, World!'

    return app