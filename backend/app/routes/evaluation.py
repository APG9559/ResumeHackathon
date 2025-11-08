from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import Job, Resume, Evaluation
from app.utils.nlp_engine import calculate_fit_score, extract_matching_keywords

bp = Blueprint('evaluation', __name__, url_prefix='/api/evaluate')

@bp.route('', methods=['POST'])
@jwt_required()
def evaluate_resumes():
    try:
        user_id = get_jwt_identity()
        data = request.get_json()
        
        job_id = data.get('job_id')
        if not job_id:
            return jsonify({'error': 'Bad Request', 'message': 'job_id is required'}), 400
        
        job = Job.query.filter_by(id=job_id, user_id=user_id).first()
        if not job:
            return jsonify({'error': 'Not Found', 'message': 'Job not found'}), 404
        
        resumes = Resume.query.filter_by(user_id=user_id).all()
        
        if not resumes:
            return jsonify({'error': 'Bad Request', 'message': 'No resumes found to evaluate'}), 400
        
        Evaluation.query.filter_by(job_id=job_id).delete()
        
        results = []
        for resume in resumes:
            fit_score = calculate_fit_score(resume.extracted_text, job.description)
            matching_keywords = extract_matching_keywords(resume.extracted_text, job.description)
            
            evaluation = Evaluation(
                job_id=job_id,
                resume_id=resume.id,
                fit_score=fit_score
            )
            evaluation.set_keywords(matching_keywords)
            db.session.add(evaluation)
        
        db.session.commit()
        
        # Build results after commit so evaluated_at is populated
        evaluations = Evaluation.query.filter_by(job_id=job_id).all()
        for evaluation in evaluations:
            resume = Resume.query.get(evaluation.resume_id)
            results.append({
                'resume_id': resume.id,
                'filename': resume.filename,
                'fit_score': evaluation.fit_score,
                'matching_keywords': evaluation.get_keywords(),
                'evaluated_at': evaluation.evaluated_at.isoformat()
            })
        
        results.sort(key=lambda x: x['fit_score'], reverse=True)
        
        return jsonify({
            'job_id': job_id,
            'job_title': job.title,
            'results': results
        }), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500

@bp.route('/<int:job_id>', methods=['GET'])
@jwt_required()
def get_evaluation_results(job_id):
    try:
        user_id = get_jwt_identity()
        
        job = Job.query.filter_by(id=job_id, user_id=user_id).first()
        if not job:
            return jsonify({'error': 'Not Found', 'message': 'Job not found'}), 404
        
        evaluations = Evaluation.query.filter_by(job_id=job_id).join(Resume).filter(Resume.user_id == user_id).all()
        
        if not evaluations:
            return jsonify({'error': 'Not Found', 'message': 'No evaluation results found for this job'}), 404
        
        results = []
        for evaluation in evaluations:
            resume = Resume.query.get(evaluation.resume_id)
            results.append({
                'resume_id': evaluation.resume_id,
                'filename': resume.filename,
                'fit_score': evaluation.fit_score,
                'matching_keywords': evaluation.get_keywords(),
                'evaluated_at': evaluation.evaluated_at.isoformat()
            })
        
        results.sort(key=lambda x: x['fit_score'], reverse=True)
        
        return jsonify({
            'job_id': job_id,
            'job_title': job.title,
            'results': results
        }), 200
    except Exception as e:
        return jsonify({'error': 'Internal Server Error', 'message': str(e)}), 500
