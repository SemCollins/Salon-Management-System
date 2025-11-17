from app import create_app, db
from app.models import User, Stylist, Service, Appointment, Review, Product, Invoice, Inventory, Notification

app = create_app()

# optionally expose shell context for flask shell
@app.shell_context_processor
def make_shell_context():
    return {'db': db, 'User': User, 'Stylist': Stylist, 'Service': Service, 'Appointment': Appointment, 'Review': Review}

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)