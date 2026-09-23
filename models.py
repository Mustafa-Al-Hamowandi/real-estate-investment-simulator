from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False, default='investor')  # 'investor' or 'admin'
    balance = db.Column(db.Float, default=1000000.0)  # Starting balance
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    owned_properties = db.relationship('Property', backref='owner', lazy=True, foreign_keys='Property.owner_id')
    transactions = db.relationship('Transaction', backref='user', lazy=True, foreign_keys='Transaction.user_id')
    
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Property(db.Model):
    __tablename__ = 'properties'
    
    id = db.Column(db.Integer, primary_key=True)
    address = db.Column(db.String(200), nullable=False)
    city = db.Column(db.String(100), nullable=False)
    state = db.Column(db.String(50), nullable=False)
    zipcode = db.Column(db.String(20), nullable=False)
    price = db.Column(db.Float, nullable=False)
    bedrooms = db.Column(db.Integer, nullable=False)
    bathrooms = db.Column(db.Float, nullable=False)
    sqft = db.Column(db.Integer, nullable=False)
    property_type = db.Column(db.String(50), nullable=False)  # House, Condo, Apartment
    description = db.Column(db.Text)
    image_url = db.Column(db.String(300))
    status = db.Column(db.String(20), default='available')  # available, sold, pending
    owner_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)
    listed_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    transactions = db.relationship('Transaction', backref='property', lazy=True)
    predictions = db.relationship('AIPrediction', backref='property', lazy=True)
    
    def __repr__(self):
        return f'<Property {self.address}>'


class Transaction(db.Model):
    __tablename__ = 'transactions'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    transaction_type = db.Column(db.String(20), nullable=False)  # 'buy' or 'sell'
    amount = db.Column(db.Float, nullable=False)
    transaction_date = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Transaction {self.transaction_type} - ${self.amount}>'


class MarketData(db.Model):
    __tablename__ = 'market_data'
    
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    interest_rate = db.Column(db.Float, default=6.5)
    avg_price = db.Column(db.Float)
    market_trend = db.Column(db.String(20))  # 'bullish', 'bearish', 'stable'
    weather_impact = db.Column(db.Float, default=0.0)
    economic_indicator = db.Column(db.Float, default=1.0)
    
    def __repr__(self):
        return f'<MarketData {self.date}>'


class AIPrediction(db.Model):
    __tablename__ = 'ai_predictions'
    
    id = db.Column(db.Integer, primary_key=True)
    property_id = db.Column(db.Integer, db.ForeignKey('properties.id'), nullable=False)
    predicted_value = db.Column(db.Float, nullable=False)
    confidence_score = db.Column(db.Float, nullable=False)
    prediction_date = db.Column(db.DateTime, default=datetime.utcnow)
    factors = db.Column(db.Text)  # JSON string of factors
    recommendation = db.Column(db.String(20))  # 'buy', 'sell', 'hold'
    
    def __repr__(self):
        return f'<AIPrediction Property:{self.property_id} - ${self.predicted_value}>'