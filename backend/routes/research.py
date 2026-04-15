from flask import Blueprint, request, jsonify, g
from middleware import token_required
from services.ai_orchestrator import analyze_query

research_bp = Blueprint('research', __name__)

@research_bp.route('/query', methods=['POST'])
@token_required
def research_query():
    data = request.get_json()
    query = data.get('query')
    
    if not query:
        return jsonify({'message': 'Query is required'}), 400
        
    try:
        # Call the orchestrator
        result = analyze_query(query)
        return jsonify(result), 200
    except Exception as e:
        import traceback
        traceback.print_exc()
        return jsonify({'message': 'Error processing query', 'error': str(e)}), 500
