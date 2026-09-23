from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from werkzeug.utils import secure_filename
from services.simulation_service import MarketSimulationService
from config import Config
from models import db, User, Property, Transaction, MarketData, AIPrediction
from database import init_database
from services.ai_service import AIService
from services.weather_service import WeatherService
from services.market_comparables_service import MarketComparablesService
from datetime import datetime
from functools import wraps
import json
import os

app = Flask(__name__)
app.config.from_object(Config)
app.jinja_env.filters['from_json'] = json.loads

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

ai_service = AIService()
weather_service = WeatherService()
market_service = MarketComparablesService()

init_database(app)

# Ensure upload directories exist
os.makedirs(os.path.join('static', 'user_videos'), exist_ok=True)
os.makedirs(os.path.join('static', 'images'), exist_ok=True)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

def role_required(role):
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated or current_user.role != role:
                flash('Access denied. Insufficient permissions.', 'danger')
                return redirect(url_for('login'))
            return f(*args, **kwargs)
        return decorated_function
    return decorator

@app.route('/')
def index():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('admin_dashboard'))
        else:
            return redirect(url_for('investor_dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            login_user(user)
            flash(f'Welcome back, {user.username}!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid username or password', 'danger')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        confirm_password = request.form.get('confirm_password')
        if password != confirm_password:
            flash('Passwords do not match', 'danger')
            return render_template('register.html')
        if User.query.filter_by(username=username).first():
            flash('Username already exists', 'danger')
            return render_template('register.html')
        if User.query.filter_by(email=email).first():
            flash('Email already registered', 'danger')
            return render_template('register.html')
        new_user = User(username=username, email=email, role='investor')
        new_user.set_password(password)
        db.session.add(new_user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/investor/dashboard')
@login_required
@role_required('investor')
def investor_dashboard():
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    recent_transactions = Transaction.query.filter_by(user_id=current_user.id).order_by(Transaction.transaction_date.desc()).limit(5).all()
    portfolio_value = sum([prop.price for prop in my_properties])
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    if market:
        market_analysis = ai_service.get_market_analysis({'interest_rate': market.interest_rate, 'market_trend': market.market_trend, 'avg_price': market.avg_price})
    else:
        market_analysis = "Market data unavailable"
    return render_template('investor_dashboard.html', my_properties=my_properties, recent_transactions=recent_transactions, portfolio_value=portfolio_value, market=market, market_analysis=market_analysis)

@app.route('/marketplace')
@login_required
@role_required('investor')
def marketplace():
    properties = Property.query.filter_by(status='available').all()
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    return render_template('marketplace.html', properties=properties, market=market)

@app.route('/property/<int:property_id>')
@login_required
@role_required('investor')
def property_detail(property_id):
    property = Property.query.get_or_404(property_id)
    weather_data = weather_service.get_weather_impact(property.city, property.state)
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    
    # Check for existing prediction (IMPROVED CACHING - 7 days)
    prediction = AIPrediction.query.filter_by(property_id=property_id).order_by(AIPrediction.prediction_date.desc()).first()
    
    # Only generate NEW prediction if:
    # 1. No prediction exists, OR
    # 2. Prediction is older than 7 days (instead of 1 day)
    if not prediction or (datetime.utcnow() - prediction.prediction_date).days > 7:
        property_data = {
            'address': property.address, 
            'city': property.city, 
            'state': property.state, 
            'price': property.price, 
            'sqft': property.sqft, 
            'bedrooms': property.bedrooms, 
            'bathrooms': property.bathrooms, 
            'property_type': property.property_type
        }
        market_data = {
            'interest_rate': market.interest_rate if market else 6.5, 
            'market_trend': market.market_trend if market else 'stable', 
            'avg_price': market.avg_price if market else 750000
        }
        
        # This is the slow part - only runs once per 7 days now
        ai_prediction = ai_service.get_property_prediction(property_data, market_data)
        
        new_prediction = AIPrediction(
            property_id=property_id, 
            predicted_value=ai_prediction['predicted_value'], 
            confidence_score=ai_prediction['confidence_score'], 
            factors=json.dumps(ai_prediction['factors']), 
            recommendation=ai_prediction['recommendation']
        )
        db.session.add(new_prediction)
        db.session.commit()
        prediction = new_prediction
    
    comparables = market_service.get_market_comparables(property.city, property.state)
    
    return render_template('property_detail.html', 
                         property=property, 
                         weather=weather_data, 
                         prediction=prediction, 
                         comparables=comparables)

@app.route('/buy_property/<int:property_id>', methods=['POST'])
@login_required
@role_required('investor')
def buy_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.status != 'available':
        flash('Property is not available for purchase', 'danger')
        return redirect(url_for('marketplace'))
    if current_user.balance < property.price:
        flash('Insufficient funds', 'danger')
        return redirect(url_for('property_detail', property_id=property_id))
    current_user.balance -= property.price
    property.status = 'sold'
    property.owner_id = current_user.id
    transaction = Transaction(property_id=property_id, user_id=current_user.id, transaction_type='buy', amount=property.price)
    db.session.add(transaction)
    db.session.commit()
    flash(f'Successfully purchased {property.address}!', 'success')
    return redirect(url_for('portfolio'))

@app.route('/portfolio')
@login_required
@role_required('investor')
def portfolio():
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    total_purchase_price = 0
    total_current_value = 0
    for prop in my_properties:
        purchase = Transaction.query.filter_by(property_id=prop.id, user_id=current_user.id, transaction_type='buy').first()
        if purchase:
            total_purchase_price += purchase.amount
        prediction = AIPrediction.query.filter_by(property_id=prop.id).order_by(AIPrediction.prediction_date.desc()).first()
        if prediction:
            total_current_value += prediction.predicted_value
        else:
            total_current_value += prop.price
    roi = ((total_current_value - total_purchase_price) / total_purchase_price * 100) if total_purchase_price > 0 else 0
    return render_template('portfolio.html', properties=my_properties, total_purchase=total_purchase_price, total_current=total_current_value, roi=roi)

@app.route('/sell_property/<int:property_id>', methods=['POST'])
@login_required
@role_required('investor')
def sell_property(property_id):
    property = Property.query.get_or_404(property_id)
    if property.owner_id != current_user.id:
        flash('You do not own this property', 'danger')
        return redirect(url_for('portfolio'))
    prediction = AIPrediction.query.filter_by(property_id=property_id).order_by(AIPrediction.prediction_date.desc()).first()
    sale_price = prediction.predicted_value if prediction else property.price
    current_user.balance += sale_price
    property.status = 'available'
    property.owner_id = None
    property.price = sale_price
    transaction = Transaction(property_id=property_id, user_id=current_user.id, transaction_type='sell', amount=sale_price)
    db.session.add(transaction)
    db.session.commit()
    flash(f'Successfully sold {property.address} for ${sale_price:,.0f}!', 'success')
    return redirect(url_for('portfolio'))

@app.route('/ai_advisor')
@login_required
@role_required('investor')
def ai_advisor():
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    recommendations = []
    for prop in my_properties:
        prediction = AIPrediction.query.filter_by(property_id=prop.id).order_by(AIPrediction.prediction_date.desc()).first()
        if prediction:
            recommendations.append({'property': prop, 'prediction': prediction})
    return render_template('ai_advisor.html', recommendations=recommendations, market=market)

@app.route('/portfolio_optimizer')
@login_required
@role_required('investor')
def portfolio_optimizer():
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    
    if my_properties:
        market_data = {
            'interest_rate': market.interest_rate if market else 6.5,
            'market_trend': market.market_trend if market else 'stable'
        }
        optimization = ai_service.optimize_portfolio(my_properties, market_data, current_user.balance)
    else:
        optimization = None
    
    return render_template('portfolio_optimizer.html', optimization=optimization, properties=my_properties)

@app.route('/market_analytics')
@login_required
@role_required('investor')
def market_analytics():
    """Enhanced market analytics with charts and insights"""
    # Get market history (last 30 days)
    market_history = MarketData.query.order_by(MarketData.date.desc()).limit(30).all()
    market_history.reverse()  # Oldest to newest for charts
    
    # Prepare market trend chart data
    market_trend_data = {
        'dates': [m.date.strftime('%m/%d') for m in market_history] if market_history else [],
        'interest_rates': [m.interest_rate for m in market_history] if market_history else []
    }
    
    # Get all properties for analysis
    all_properties = Property.query.all()
    avg_price = sum([p.price for p in all_properties]) / len(all_properties) if all_properties else 0
    total_properties = len(all_properties)
    available_properties = len([p for p in all_properties if p.status == 'available'])
    
    # Calculate city performance
    city_stats = {}
    for prop in all_properties:
        if prop.city not in city_stats:
            city_stats[prop.city] = {'count': 0, 'total_value': 0, 'avg_price': 0}
        city_stats[prop.city]['count'] += 1
        city_stats[prop.city]['total_value'] += prop.price
    
    # Calculate average prices and sort by value
    top_cities = []
    for city, stats in city_stats.items():
        avg_city_price = stats['total_value'] / stats['count']
        top_cities.append({
            'city': city,
            'properties': stats['count'],
            'avg_price': avg_city_price,
            'total_value': stats['total_value']
        })
    
    # Sort by total value (descending)
    top_cities.sort(key=lambda x: x['total_value'], reverse=True)
    
    # Get market trends
    market_trends = market_service.get_market_trends('San Francisco', 'CA')
    
    # Market health indicators
    current_market = MarketData.query.order_by(MarketData.date.desc()).first()
    
    # Calculate supply & demand health
    availability_ratio = (available_properties / total_properties * 100) if total_properties > 0 else 0
    if availability_ratio > 60:
        supply_demand_health = "Oversupply"
    elif availability_ratio > 40:
        supply_demand_health = "Healthy"
    else:
        supply_demand_health = "High Demand"
    
    # Interest rate trend
    if len(market_history) > 1:
        rate_change = market_history[-1].interest_rate - market_history[0].interest_rate
        if rate_change > 0.5:
            rate_trend = "Rising"
        elif rate_change < -0.5:
            rate_trend = "Falling"
        else:
            rate_trend = "Stable"
    else:
        rate_trend = "Stable"
    
    # Market sentiment
    if current_market:
        if current_market.market_trend == 'bullish':
            market_sentiment = "Positive"
        elif current_market.market_trend == 'bearish':
            market_sentiment = "Negative"
        else:
            market_sentiment = "Neutral"
    else:
        market_sentiment = "Neutral"
    
    return render_template('market_analytics.html', 
                         market_history=market_history,
                         market_trend_data=market_trend_data,
                         avg_price=avg_price, 
                         total_properties=total_properties, 
                         available_properties=available_properties,
                         market_trends=market_trends,
                         top_cities=top_cities[:5],  # Top 5 cities
                         supply_demand_health=supply_demand_health,
                         rate_trend=rate_trend,
                         market_sentiment=market_sentiment,
                         current_market=current_market)

@app.route('/video_tutorials')
@login_required
def video_tutorials():
    user_videos = session.get('uploaded_videos', [])
    return render_template('video_tutorials.html', user_videos=user_videos)

@app.route('/upload_video', methods=['GET', 'POST'])
@login_required
def upload_video():
    if request.method == 'POST':
        if 'video' not in request.files:
            flash('No video file selected', 'danger')
            return redirect(request.url)
        
        video = request.files['video']
        if video.filename == '':
            flash('No file selected', 'danger')
            return redirect(request.url)
        
        if video and video.filename.lower().endswith(('.mp4', '.mov', '.avi', '.mkv')):
            filename = secure_filename(f"user_{current_user.id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}_{video.filename}")
            filepath = os.path.join('static', 'user_videos', filename)
            video.save(filepath)
            
            # Store in session
            if 'uploaded_videos' not in session:
                session['uploaded_videos'] = []
            session['uploaded_videos'].append(filename)
            session.modified = True
            
            flash('Video uploaded successfully! You can now play it from your device.', 'success')
            return redirect(url_for('video_tutorials'))
        else:
            flash('Invalid file type. Please upload MP4, MOV, AVI, or MKV files only.', 'danger')
    
    return render_template('upload_video.html')

@app.route('/delete_video/<filename>', methods=['POST'])
@login_required
def delete_video(filename):
    if 'uploaded_videos' in session and filename in session['uploaded_videos']:
        # Remove from session
        session['uploaded_videos'].remove(filename)
        session.modified = True
        
        # Delete file
        filepath = os.path.join('static', 'user_videos', filename)
        if os.path.exists(filepath):
            os.remove(filepath)
        
        flash('Video deleted successfully!', 'success')
    return redirect(url_for('video_tutorials'))

@app.route('/admin/dashboard')
@login_required
@role_required('admin')
def admin_dashboard():
    total_users = User.query.count()
    total_properties = Property.query.count()
    total_transactions = Transaction.query.count()
    recent_transactions = Transaction.query.order_by(Transaction.transaction_date.desc()).limit(10).all()
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    return render_template('admin_dashboard.html', total_users=total_users, total_properties=total_properties, total_transactions=total_transactions, recent_transactions=recent_transactions, recent_users=recent_users, market=market)

@app.route('/admin/properties')
@login_required
@role_required('admin')
def admin_properties():
    properties = Property.query.all()
    return render_template('admin_properties.html', properties=properties)

@app.route('/admin/add_property', methods=['POST'])
@login_required
@role_required('admin')
def add_property():
    new_property = Property(address=request.form.get('address'), city=request.form.get('city'), state=request.form.get('state'), zipcode=request.form.get('zipcode'), price=float(request.form.get('price')), bedrooms=int(request.form.get('bedrooms')), bathrooms=float(request.form.get('bathrooms')), sqft=int(request.form.get('sqft')), property_type=request.form.get('property_type'), description=request.form.get('description'), image_url=request.form.get('image_url', 'https://via.placeholder.com/400x300'), status='available')
    db.session.add(new_property)
    db.session.commit()
    flash('Property added successfully!', 'success')
    return redirect(url_for('admin_properties'))

@app.route('/admin/delete_property/<int:property_id>', methods=['POST'])
@login_required
@role_required('admin')
def delete_property(property_id):
    property = Property.query.get_or_404(property_id)
    Transaction.query.filter_by(property_id=property_id).delete()
    AIPrediction.query.filter_by(property_id=property_id).delete()
    db.session.delete(property)
    db.session.commit()
    flash('Property deleted successfully!', 'success')
    return redirect(url_for('admin_properties'))

@app.route('/admin/users')
@login_required
@role_required('admin')
def admin_users():
    users = User.query.all()
    return render_template('admin_users.html', users=users)

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/update_profile', methods=['POST'])
@login_required
def update_profile():
    current_user.email = request.form.get('email')
    new_password = request.form.get('new_password')
    if new_password:
        current_user.set_password(new_password)
    db.session.commit()
    flash('Profile updated successfully!', 'success')
    return redirect(url_for('profile'))

@app.route('/market_simulator')
@login_required
@role_required('investor')
def market_simulator():
    """Market Crisis Simulator - shows complex economic simulations"""
    scenarios = MarketSimulationService.get_scenarios()
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    
    return render_template('market_simulator.html', 
                         scenarios=scenarios, 
                         properties=my_properties,
                         has_properties=len(my_properties) > 0)

@app.route('/run_simulation/<scenario_id>', methods=['POST'])
@login_required
@role_required('investor')
def run_simulation(scenario_id):
    """Run the crisis simulation"""
    my_properties = Property.query.filter_by(owner_id=current_user.id).all()
    
    if not my_properties:
        flash('You need to own properties to run a simulation', 'warning')
        return redirect(url_for('marketplace'))
    
    market = MarketData.query.order_by(MarketData.date.desc()).first()
    market_data = {
        'interest_rate': market.interest_rate if market else 6.5,
        'market_trend': market.market_trend if market else 'stable'
    }
    
    # Run the simulation
    simulation_service = MarketSimulationService()
    results = simulation_service.run_simulation(scenario_id, my_properties, market_data)
    
    if not results:
        flash('Invalid simulation scenario', 'danger')
        return redirect(url_for('market_simulator'))
    
    # Convert Property objects to dictionaries for JSON serialization
    serializable_results = {
        'scenario': results['scenario'],
        'duration_months': results['duration_months'],
        'portfolio_summary': results['portfolio_summary'],
        'property_breakdown': [
            {
                'property': {
                    'id': pt['property'].id,
                    'address': pt['property'].address,
                    'city': pt['property'].city,
                    'state': pt['property'].state,
                    'property_type': pt['property'].property_type,
                    'price': pt['property'].price
                },
                'timeline': pt['timeline'],
                'initial_value': pt['initial_value'],
                'final_value': pt['final_value'],
                'total_loss': pt['total_loss'],
                'loss_percentage': pt['loss_percentage']
            }
            for pt in results['property_breakdown']
        ],
        'worst_hit': [
            {
                'property': {
                    'id': wh['property'].id,
                    'address': wh['property'].address,
                    'city': wh['property'].city,
                    'state': wh['property'].state,
                    'property_type': wh['property'].property_type,
                    'price': wh['property'].price
                },
                'initial_value': wh['initial_value'],
                'final_value': wh['final_value'],
                'total_loss': wh['total_loss'],
                'loss_percentage': wh['loss_percentage']
            }
            for wh in results['worst_hit']
        ],
        'best_protected': [
            {
                'property': {
                    'id': bp['property'].id,
                    'address': bp['property'].address,
                    'city': bp['property'].city,
                    'state': bp['property'].state,
                    'property_type': bp['property'].property_type,
                    'price': bp['property'].price
                },
                'initial_value': bp['initial_value'],
                'final_value': bp['final_value'],
                'total_loss': bp['total_loss'],
                'loss_percentage': bp['loss_percentage']
            }
            for bp in results['best_protected']
        ],
        'insights': results['insights'],
        'recovery_timeline': results['recovery_timeline'],
        'market_effects': results['market_effects']
    }
    
    # Store serializable results in session
    session['simulation_results'] = serializable_results
    session['simulation_scenario_id'] = scenario_id
    
    return redirect(url_for('simulation_results'))

@app.route('/simulation_results')
@login_required
@role_required('investor')
def simulation_results():
    """Display simulation results"""
    results = session.get('simulation_results')
    
    if not results:
        flash('No simulation results available', 'info')
        return redirect(url_for('market_simulator'))
    
    return render_template('simulation_results.html', results=results)

@app.route('/admin/update_market', methods=['POST'])
@login_required
@role_required('admin')
def update_market():
    """Update market configuration"""
    try:
        interest_rate = float(request.form.get('interest_rate'))
        market_trend = request.form.get('market_trend')
        economic_indicator = float(request.form.get('economic_indicator'))
        
        # Get current market data or create new
        market = MarketData.query.order_by(MarketData.date.desc()).first()
        
        if market:
            # Update existing
            market.interest_rate = interest_rate
            market.market_trend = market_trend
            market.economic_indicator = economic_indicator
            market.date = datetime.utcnow()
        else:
            # Create new
            market = MarketData(
                interest_rate=interest_rate,
                market_trend=market_trend,
                economic_indicator=economic_indicator,
                avg_price=750000  # Default
            )
            db.session.add(market)
        
        db.session.commit()
        flash('Market configuration updated successfully!', 'success')
    except Exception as e:
        flash(f'Error updating market: {str(e)}', 'danger')
    
    return redirect(url_for('admin_dashboard'))

if __name__ == '__main__':
    app.run(debug=True, port=5000)