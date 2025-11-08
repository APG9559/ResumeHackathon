from datetime import datetime
from app import db
import json

class Evaluation(db.Model):
    __tablename__ = 'evaluations'
    
    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    resume_id = db.Column(db.Integer, db.ForeignKey('resumes.id'), nullable=False)
    fit_score = db.Column(db.Float, nullable=False)
    matching_keywords = db.Column(db.Text, nullable=False)  # JSON string
    evaluated_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def set_keywords(self, keywords_list):
        self.matching_keywords = json.dumps(keywords_list)
    
    def get_keywords(self):
        return json.loads(self.matching_keywords)
    
    def to_dict(self):
        return {
            'id': self.id,
            'job_id': self.job_id,
            'resume_id': self.resume_id,
            'fit_score': round(self.fit_score, 2),
            'matching_keywords': self.get_keywords(),
            'evaluated_at': self.evaluated_at.isoformat()
        }
