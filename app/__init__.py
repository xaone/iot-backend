from flask import Flask

def create_app():
    """
    Factory function to create and configure the Flask app.
    """
    app = Flask(__name__)

    # Register blueprints
    from .controllers import api_blueprint
    app.register_blueprint(api_blueprint)

    return app