from flask import Blueprint, request, jsonify, current_app
from flask_jwt_extended import jwt_required, get_jwt_identity
from werkzeug.utils import secure_filename
from app import db
from app.models import Resume
from app.utils.file_handler import allowed_file, extract_text
import os
from datetime import datetime

bp = Blueprint('resumes', __name__, url_prefix='/api/resumes')

@bp.route('/upload', methods=['POST'])
@jwt_required()
def upload_resume():
    try:
        user_id = get_jwt_identity()
        
        if 'file' not in request.files:
            return jsonify({'error': 'Bad Request', 'message': 'No file provided'}), 400
        
        file = request.files['file']
        
        if file.filename == '':
            return jsonify({'error': 'Bad Request', 'message': 'No file selected'}), 400
        
        if not allowed_file(file.filename, current_app.config['ALLOWED_EXTENSIONS']):
            return jsonify({'error': 'Bad Request', 'message': 'Invalid file type. Only PDF and TXT files are allowed'}), 400
        
        filename = secure_filename(file.filename)
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        unique_filename = f"{timestamp}_{filename}"
        file_path = os.path.join(current_app.config['UPLOAD_FOLDER'], unique_filename)
        
        os.makedirs(current_app.config['UPLOAD_FOLDER'], exist_ok=True)
        file.save(file_path)
        
        file_extension = filename.rsplit('.', 1)[1].lower()
        extracted_text = extract_text(file_path, file_extension)
        
        if not extracted_text:
            os.remove(file_path)
            return jsonify({'error': 'Bad Request', 'message': 'Could not extract text from file'}), 400
        
        resume = Resume(
            user_id=user_id,
            filename=filename,
            file_path=file_path,
            extracted_text=extracted_text
        )
        db.session.add(resume)
        db.session.commit()
        
        return jsonify(resume.to_dict(include_text=True)), 201
    except Exception as e:
        db.session.rollback()
        if 'file_path' in locals() and os.path.exists(file_path):
            os.remove(file_path)
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('', methods=['GET'])
@jwt_required()
def get_resumes():
    try:
        user_id = get_jwt_identity()
        resumes = Resume.query.filter_by(user_id=user_id).order_by(Resume.uploaded_at.desc()).all()
        return jsonify([resume.to_dict() for resume in resumes]), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('/<int:resume_id>', methods=['DELETE'])
@jwt_required()
def delete_resume(resume_id):
    try:
        user_id = get_jwt_identity()
        resume = Resume.query.filter_by(id=resume_id, user_id=user_id).first()
        
        if not resume:
            return jsonify({'error': 'Not Found', 'message': 'Resume not found'}), 404
        
        if os.path.exists(resume.file_path):
            os.remove(resume.file_path)
        
        db.session.delete(resume)
        db.session.commit()
        
        return jsonify({'message': 'Resume deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
