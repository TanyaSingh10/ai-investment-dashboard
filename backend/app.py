# from prometheus_client import Counter, Histogram, generate_latest
# from flask import Flask, jsonify
# from flask_cors import CORS
# from config import Config
# from models import db
# from dotenv import load_dotenv
# load_dotenv()

# import os
# print("API KEY LOADED:", os.getenv("OPENAI_API_KEY"))
# REQUEST_COUNT = Counter('request_count', 'Total API Requests')
# REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')

# def create_app():
#     app = Flask(__name__)
#     app.config.from_object(Config)
#     @app.before_request
#     def before_request():
#         REQUEST_COUNT.inc()
    
#     CORS(app) # Allow cross-origin requests from React
    
#     db.init_app(app)
    
#     # Import routes inside the function to avoid circular imports if needed
#     from routes.auth import auth_bp
#     from routes.research import research_bp
#     from routes.reports import reports_bp
    
#     app.register_blueprint(auth_bp, url_prefix='/api/auth')
#     app.register_blueprint(research_bp, url_prefix='/api/research')
#     app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
#     # Basic healthcheck
#     @app.route('/health', methods=['GET'])
#     def health():
#         return jsonify({'status': 'ok'})

#     with app.app_context():
#         # Create all tables (Fallback for local dev. Supabase would use migrations)
#         db.create_all()

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(host='0.0.0.0', port=5001, debug=True)

from prometheus_client import Counter, Histogram, generate_latest
from flask import Flask, jsonify, request
from flask_cors import CORS
from config import Config
from models import db
from dotenv import load_dotenv
from time import time

load_dotenv()

import os
print("API KEY LOADED:", os.getenv("OPENAI_API_KEY"))

# =======================
# Prometheus Metrics
# =======================
REQUEST_COUNT = Counter('request_count', 'Total API Requests')
REQUEST_LATENCY = Histogram('request_latency_seconds', 'Request latency')


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)  # Allow cross-origin requests from React
    
    db.init_app(app)
    
    # =======================
    # Middleware for Metrics
    # =======================
    @app.before_request
    def before_request():
        request.start_time = time()
        REQUEST_COUNT.inc()

    @app.after_request
    def after_request(response):
        latency = time() - request.start_time
        REQUEST_LATENCY.observe(latency)
        return response

    # =======================
    # Routes
    # =======================
    from routes.auth import auth_bp
    from routes.research import research_bp
    from routes.reports import reports_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(research_bp, url_prefix='/api/research')
    app.register_blueprint(reports_bp, url_prefix='/api/reports')
    
    # Healthcheck
    @app.route('/health', methods=['GET'])
    def health():
        return jsonify({'status': 'ok'})

    # =======================
    # Prometheus Metrics Endpoint
    # =======================
    @app.route('/metrics')
    def metrics():
        return generate_latest(), 200, {'Content-Type': 'text/plain'}

    with app.app_context():
        db.create_all()

    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5001, debug=True)