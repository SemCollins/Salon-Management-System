from flask import render_template, jsonify, request, Blueprint
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.models import Appointment, User, Service, Stylist, Product, Inventory
from app import db

bp = Blueprint('admin', __name__)

@bp.route('/')
@jwt_required()
def admin_dashboard():
    current_user = User.query.get(get_jwt_identity())
    if current_user.role != 'admin':
        return jsonify({'error': 'Unauthorized'}), 403
    
    # Dashboard statistics
    total_appointments = Appointment.query.count()
    pending_appointments = Appointment.query.filter_by(status='pending').count()
    total_revenue = db.session.query(db.func.sum(Invoice.total)).scalar() or 0
    
    return render_template('admin/dashboard.html',
                         total_appointments=total_appointments,
                         pending_appointments=pending_appointments,
                         total_revenue=total_revenue)

@bp.route('/api/appointments')
@jwt_required()
def api_appointments():
    appointments = Appointment.query.all()
    return jsonify([{
        'id': a.id,
        'client_name': f"{a.client.first_name} {a.client.last_name}",
        'service_name': a.service.name,
        'stylist_name': f"{a.stylist.user.first_name} {a.stylist.user.last_name}",
        'start_time': a.start_time.isoformat(),
        'status': a.status,
        'payment_status': a.payment_status
    } for a in appointments])