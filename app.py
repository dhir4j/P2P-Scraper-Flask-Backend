from flask import Flask
from flask_cors import CORS
from routes.dashboard_routes import dashboard_bp
from routes.liquidity_routes import liquidity_bp
from routes.logs_routes import logs_bp

def create_app():
    app = Flask(__name__)
    CORS(app)
    
    # Register blueprints
    app.register_blueprint(dashboard_bp)
    app.register_blueprint(liquidity_bp)
    app.register_blueprint(logs_bp)
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)