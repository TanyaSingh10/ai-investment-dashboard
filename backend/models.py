import uuid
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.dialects.postgresql import JSONB
import sqlite3

db = SQLAlchemy()

def generate_uuid():
    return str(uuid.uuid4())

class Organization(db.Model):
    __tablename__ = 'organizations'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    users = db.relationship('User', backref='organization', lazy=True)
    reports = db.relationship('Report', backref='organization', lazy=True)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    reports = db.relationship('Report', backref='user', lazy=True)

class Report(db.Model):
    __tablename__ = 'reports'
    id = db.Column(db.String(36), primary_key=True, default=generate_uuid)
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    org_id = db.Column(db.String(36), db.ForeignKey('organizations.id'), nullable=False)
    title = db.Column(db.String(255), nullable=False)
    query = db.Column(db.Text, nullable=False)
    
    # We will use simple JSON column since SQLite doesn't support Postgres JSONB perfectly.
    # In production with Postgres we would use JSONB.
    report_data = db.Column(db.JSON, nullable=False) 
    
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
