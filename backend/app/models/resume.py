from datetime import datetime
from app import db

class Resume(db.Model):
    __tablename__ = 'resumes'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    filename = db.Column(db.String(255), nullable=False)
    file_path = db.Column(db.String(500), nullable=False)
    extracted_text = db.Column(db.Text, nullable=False)
    uploaded_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    evaluations = db.relationship('Evaluation', backref='resume', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self, include_text=False):
        data = {
            'id': self.id,
            'filename': self.filename,
            'uploaded_at': self.uploaded_at.isoformat()
        }
        if include_text:
            data['extracted_text'] = self.extracted_text
            data['text_preview'] = self.extracted_text[:200] + '...' if len(self.extracted_text) > 200 else self.extracted_text
        return data
