from models import db, User, Property, MarketData
from datetime import datetime
import random

def init_database(app):
    """Initialize database with sample data"""
    with app.app_context():
        # DROP ALL TABLES AND RECREATE
        db.drop_all()
        db.create_all()
        
        print("Initializing database...")
        
        # Create users
        admin = User(username='admin', email='admin@realestate.com', role='admin', balance=5000000.0)
        admin.set_password('admin123')
        db.session.add(admin)
        
        investor1 = User(username='investor1', email='investor1@email.com', role='investor', balance=2000000.0)
        investor1.set_password('investor123')
        db.session.add(investor1)
        
        investor2 = User(username='investor2', email='investor2@email.com', role='investor', balance=750000.0)
        investor2.set_password('investor123')
        db.session.add(investor2)
        
        # Sample properties
        props = [
            Property(address='123 Oak Street', city='San Francisco', state='CA', zipcode='94102', price=850000, bedrooms=3, bathrooms=2.5, sqft=2100, property_type='House', description='Beautiful Victorian home in the heart of SF', image_url='https://images.unsplash.com/photo-1568605114967-8130f3a36994?w=400&h=300&fit=crop'),
            Property(address='456 Pine Avenue', city='Los Angeles', state='CA', zipcode='90001', price=620000, bedrooms=2, bathrooms=2, sqft=1500, property_type='Condo', description='Modern condo with city views', image_url='https://images.unsplash.com/photo-1545324418-cc1a3fa10c00?w=400&h=300&fit=crop'),
            Property(address='789 Maple Drive', city='Seattle', state='WA', zipcode='98101', price=725000, bedrooms=4, bathrooms=3, sqft=2400, property_type='House', description='Spacious family home near schools', image_url='https://images.unsplash.com/photo-1580587771525-78b9dba3b914?w=400&h=300&fit=crop'),
            Property(address='321 Beach Road', city='Miami', state='FL', zipcode='33101', price=1200000, bedrooms=3, bathrooms=3, sqft=2800, property_type='House', description='Luxury beachfront property', image_url='https://images.unsplash.com/photo-1613490493576-7fde63acd811?w=400&h=300&fit=crop'),
            Property(address='555 Downtown Plaza', city='New York', state='NY', zipcode='10001', price=950000, bedrooms=2, bathrooms=2, sqft=1200, property_type='Apartment', description='High-rise luxury apartment in Manhattan', image_url='https://images.unsplash.com/photo-1512917774080-9991f1c4c750?w=400&h=300&fit=crop'),
            Property(address='888 Sunset Boulevard', city='Austin', state='TX', zipcode='78701', price=485000, bedrooms=3, bathrooms=2, sqft=1900, property_type='House', description='Contemporary home in tech hub', image_url='https://images.unsplash.com/photo-1600596542815-ffad4c1539a9?w=400&h=300&fit=crop'),
            Property(address='999 Mountain View', city='Denver', state='CO', zipcode='80201', price=675000, bedrooms=4, bathrooms=2.5, sqft=2200, property_type='House', description='Mountain view property with modern amenities', image_url='https://images.unsplash.com/photo-1600585154340-be6161a56a0c?w=400&h=300&fit=crop'),
            Property(address='111 Tech Park Lane', city='San Jose', state='CA', zipcode='95101', price=920000, bedrooms=3, bathrooms=2.5, sqft=2000, property_type='House', description='Modern home in Silicon Valley', image_url='https://images.unsplash.com/photo-1600047509807-ba8f99d2cdde?w=400&h=300&fit=crop')
        ]
        
        for p in props:
            db.session.add(p)
        
        # Add market data
        market = MarketData(interest_rate=6.5, avg_price=750000, market_trend='stable', weather_impact=0.0, economic_indicator=1.0)
        db.session.add(market)
        
        db.session.commit()
        print("Database initialized successfully!")
        print(f"Created {User.query.count()} users")
        print(f"Created {Property.query.count()} properties")
        print("Login credentials:")
        print("  Admin - username: admin, password: admin123")
        print("  Investor - username: investor1, password: investor123")