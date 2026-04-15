from flask import Flask, jsonify
from flask_cors import CORS
from config import Config
from models import db

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app) # Allow cross-origin requests from React
    
    db.init_app(app)
    
    # Import routes inside the function to avoid circular imports if needed
    from routes.auth import auth_bp
    from routes.research import research_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(research_bp, url_prefix='/api/research')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Basic healthcheck
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    with app.app_context():
        # Create all tables (Fallback for local dev. Supabase would use migrations)
        db.create_all()

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=True)
