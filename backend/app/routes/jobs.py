from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Job

bp = Blueprint('jobs', __name__, url_prefix='/api/jobs')

@bp.route('', methods=['POST'])
@jwt_required()
def create_job():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        if not title or not description:
            return jsonify({'error': 'Bad Request', 'message': 'Title and description are required'}), 400
        
        job = Job(
            user_id=user_id,
            title=title,
            description=description
        )
        db.session.add(job)
        db.session.commit()
        
        return jsonify(job.to_dict()), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('', methods=['GET'])
@jwt_required()
def get_jobs():
    try:
        user_id = get_jwt_identity()
        jobs = Job.query.filter_by(user_id=user_id).order_by(Job.created_at.desc()).all()
        return jsonify([job.to_dict() for job in jobs]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('/<int:job_id>', methods=['PUT'])
@jwt_required()
def update_job(job_id):
    try:
        user_id = get_jwt_identity()
        job = Job.query.filter_by(id=job_id, user_id=user_id).first()
        
        if not job:
            return jsonify({'error': 'Not Found', 'message': 'Job not found'}), 404
        
        data = request.get_json()
        title = data.get('title', '').strip()
        description = data.get('description', '').strip()
        
        if not title or not description:
            return jsonify({'error': 'Bad Request', 'message': 'Title and description are required'}), 400
        
        job.title = title
        job.description = description
        db.session.commit()
        
        return jsonify(job.to_dict()), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('/<int:job_id>', methods=['DELETE'])
@jwt_required()
def delete_job(job_id):
    try:
        user_id = get_jwt_identity()
        job = Job.query.filter_by(id=job_id, user_id=user_id).first()
        
        if not job:
            return jsonify({'error': 'Not Found', 'message': 'Job not found'}), 404
        
        db.session.delete(job)
        db.session.commit()
        
        return jsonify({'message': 'Job deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
