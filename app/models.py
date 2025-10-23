# app/models.py
from app import db
from flask_login import UserMixin
from datetime import datetime
import json

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    phone = db.Column(db.String(20))
    role = db.Column(db.String(20), nullable=False, default='client')  # admin, staff, client
    password_hash = db.Column(db.String(128))
    membership_points = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    email_verified = db.Column(db.Boolean, default=False)
    
    # Relationships
    appointments = db.relationship('Appointment', backref='client', lazy='dynamic')
    reviews = db.relationship('Review', backref='client', lazy='dynamic')
    notifications = db.relationship('Notification', backref='user', lazy='dynamic')

class Stylist(db.Model):
    __tablename__ = 'stylists'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    specialties = db.Column(db.String(200))
    experience = db.Column(db.Integer)  # in years
    bio = db.Column(db.Text)
    portfolio_images = db.Column(db.Text)  # JSON string of image URLs
    is_active = db.Column(db.Boolean, default=True)
    rating = db.Column(db.Float, default=0.0)
    
    user = db.relationship('User', backref=db.backref('stylist', uselist=False))
    appointments = db.relationship('Appointment', backref='stylist', lazy='dynamic')

class Service(db.Model):
    __tablename__ = 'services'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    category = db.Column(db.String(50))  # hair, nails, spa, etc.
    price = db.Column(db.Float, nullable=False)
    duration = db.Column(db.Integer)  # in minutes
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    is_active = db.Column(db.Boolean, default=True)
    
    appointments = db.relationship('Appointment', backref='service', lazy='dynamic')
    reviews = db.relationship('Review', backref='service', lazy='dynamic')

class Appointment(db.Model):
    __tablename__ = 'appointments'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylists.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    status = db.Column(db.String(20), default='booked')  # booked, confirmed, cancelled, completed
    payment_status = db.Column(db.String(20), default='pending')  # pending, paid, refunded
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    invoice = db.relationship('Invoice', backref='appointment', uselist=False)

class Review(db.Model):
    __tablename__ = 'reviews'
    
    id = db.Column(db.Integer, primary_key=True)
    client_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    service_id = db.Column(db.Integer, db.ForeignKey('services.id'), nullable=False)
    stylist_id = db.Column(db.Integer, db.ForeignKey('stylists.id'), nullable=False)
    rating = db.Column(db.Integer, nullable=False)  # 1-5
    comment = db.Column(db.Text)
    date_posted = db.Column(db.DateTime, default=datetime.utcnow)
    is_approved = db.Column(db.Boolean, default=False)

class Product(db.Model):
    __tablename__ = 'products'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)
    stock = db.Column(db.Integer, default=0)
    description = db.Column(db.Text)
    image = db.Column(db.String(200))
    category = db.Column(db.String(50))
    is_active = db.Column(db.Boolean, default=True)

class Invoice(db.Model):
    __tablename__ = 'invoices'
    
    id = db.Column(db.Integer, primary_key=True)
    appointment_id = db.Column(db.Integer, db.ForeignKey('appointments.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    tax = db.Column(db.Float, default=0.0)
    discount = db.Column(db.Float, default=0.0)
    total = db.Column(db.Float, nullable=False)
    date_issued = db.Column(db.DateTime, default=datetime.utcnow)
    payment_method = db.Column(db.String(50))
    stripe_payment_intent_id = db.Column(db.String(100))

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False)
    quantity = db.Column(db.Integer, default=0)
    reorder_level = db.Column(db.Integer, default=5)
    last_restocked = db.Column(db.DateTime, default=datetime.utcnow)
    
    product = db.relationship('Product', backref='inventory')

class Notification(db.Model):
    __tablename__ = 'notifications'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    message = db.Column(db.Text, nullable=False)
    type = db.Column(db.String(50))  # email, sms, app
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default='sent')  # sent, delivered, read
    related_entity_type = db.Column(db.String(50))  # appointment, product, etc.
    related_entity_id = db.Column(db.Integer)