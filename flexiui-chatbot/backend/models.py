"""
Database Models for FlexiUI AI Generator
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# ============================================
# Project Model - Stores Generated UIs
# ============================================

class Project(db.Model):
    """
    Stores each generated UI project
    """
    __tablename__ = 'projects'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    prompt = db.Column(db.Text, nullable=False)
    
    # Generated code
    html_code = db.Column(db.Text, nullable=True)
    css_code = db.Column(db.Text, nullable=True)
    js_code = db.Column(db.Text, nullable=True)
    
    # Metadata
    component_type = db.Column(db.String(50), default='general')
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Statistics
    views = db.Column(db.Integer, default=0)
    
    def to_dict(self):
        """Convert project to dictionary"""
        return {
            'id': self.id,
            'name': self.name,
            'prompt': self.prompt,
            'html_code': self.html_code,
            'css_code': self.css_code,
            'js_code': self.js_code,
            'component_type': self.component_type,
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat(),
            'views': self.views
        }
    
    def __repr__(self):
        return f'<Project {self.id}: {self.name}>'

# ============================================
# Generation Log Model - Track API Usage
# ============================================

class GenerationLog(db.Model):
    """
    Tracks all generation attempts for analytics
    """
    __tablename__ = 'generation_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    prompt = db.Column(db.Text, nullable=False)
    component_type = db.Column(db.String(50))
    
    # Result
    success = db.Column(db.Boolean, default=True)
    error_message = db.Column(db.Text, nullable=True)
    
    # Timing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    generation_time = db.Column(db.Float)  # seconds
    
    def to_dict(self):
        return {
            'id': self.id,
            'prompt': self.prompt,
            'component_type': self.component_type,
            'success': self.success,
            'error_message': self.error_message,
            'created_at': self.created_at.isoformat(),
            'generation_time': self.generation_time
        }
    
    def __repr__(self):
        return f'<GenerationLog {self.id}: {"Success" if self.success else "Failed"}>'