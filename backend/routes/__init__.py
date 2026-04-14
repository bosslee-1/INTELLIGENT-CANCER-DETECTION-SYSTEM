from .health import health_bp
from .auth_routes import auth_bp
from .ml import ml_bp


# Blueprint = Router in Express

def register_routes(app):
    app.register_blueprint(health_bp, url_prefix="/api")
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(ml_bp, url_prefix="/api/ml")
