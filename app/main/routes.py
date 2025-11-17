from flask import render_template, jsonify, request, Blueprint
from app.models import Service, Stylist, Review, User
from app import db

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('index.html')

@bp.route('/services')
def services():
    return render_template('services.html')

@bp.route('/booking')
def booking():
    return render_template('booking.html')

@bp.route('/dashboard')
def dashboard():
    return render_template('dashboard.html')

# API Routes
@bp.route('/api/services')
def api_services():
    services = Service.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'name': s.name,
        'category': s.category,
        'price': s.price,
        'duration': s.duration,
        'description': s.description,
        'image': s.image
    } for s in services])

@bp.route('/api/stylists')
def api_stylists():
    stylists = Stylist.query.filter_by(is_active=True).all()
    return jsonify([{
        'id': s.id,
        'first_name': s.user.first_name,
        'last_name': s.user.last_name,
        'specialties': s.specialties,
        'experience': s.experience,
        'bio': s.bio,
        'portfolio_images': s.portfolio_images
    } for s in stylists])

@bp.route('/api/available-slots')
def available_slots():
    stylist_id = request.args.get('stylist_id')
    date = request.args.get('date')
    # Implement slot availability logic
    return jsonify({'slots': []})