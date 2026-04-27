from flask import Blueprint, request, jsonify, g
from models import db, Report
from middleware import token_required

reports_bp = Blueprint('reports', __name__)

@reports_bp.route('/', methods=['GET'])
@token_required
def get_reports():
    # Enforce multi-tenancy by filtering with org_id
    reports = db.session.query(Report).filter_by(org_id=g.org_id).order_by(Report.created_at.desc()).all()
    
    result = []
    for r in reports:
        result.append({
            'id': r.id,
            'title': r.title,
            'query': r.query,
            'created_at': r.created_at.isoformat(),
            # Exclude full report data for list view to save bandwidth
            'report_data': r.report_data 
        })
        
    return jsonify(result), 200

@reports_bp.route('/', methods=['POST'])
@token_required
def create_report():
    data = request.get_json()
    title = data.get('title')
    query = data.get('query')
    report_data = data.get('report_data')
    
    if not title or not query or not report_data:
        return jsonify({'message': 'Missing fields'}), 400
        
    new_report = Report(
        user_id=g.user_id,
        org_id=g.org_id,
        title=title,
        query=query,
        report_data=report_data
    )
    db.session.add(new_report)
    db.session.commit()
    
    return jsonify({'message': 'Report saved', 'id': new_report.id}), 201

@reports_bp.route('/<report_id>', methods=['DELETE'])
@token_required
def delete_report(report_id):
    report = db.session.query(Report).filter_by(id=report_id, org_id=g.org_id).first()
    
    if not report:
        return jsonify({'message': 'Report not found or access denied'}), 404
        
    db.session.delete(report)
    db.session.commit()
    
    return jsonify({'message': 'Report deleted successfully'}), 200
