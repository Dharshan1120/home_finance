from flask import Flask
from flask_jwt_extended import JWTManager
from models import db, bcrypt
from config import Config
from flask_cors import CORS

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    CORS(app, supports_credentials=True)

    # Initialize JWT Manager
    jwt = JWTManager(app)
    
    with app.app_context():
        # Register Blueprints
        from routes.auth import auth_bp
        from routes.expenses import expenses_bp
        from routes.dashboard import dashboard_bp
        from routes.views import views_bp
        from routes.budgets import budgets_bp

        app.register_blueprint(auth_bp, url_prefix='/api/auth')
        app.register_blueprint(expenses_bp, url_prefix='/api/expenses')
        app.register_blueprint(dashboard_bp, url_prefix='/api/dashboard')
        app.register_blueprint(budgets_bp, url_prefix='/api/budgets')
        app.register_blueprint(views_bp)

    return app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, port=5000)
