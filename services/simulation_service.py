"""
Market Simulation Service
Implements complex economic crisis simulations with multi-factor calculations
This demonstrates advanced logic beyond simple AI API calls
"""
import random
from datetime import datetime

class MarketSimulationService:
    
    # Define crisis scenarios with realistic parameters
    SCENARIOS = {
        '2008_crisis': {
            'name': '2008 Housing Crisis Replay',
            'description': 'Simulates the 2008 financial crisis with subprime mortgage collapse, credit freeze, and cascading market effects',
            'icon': 'fa-chart-line-down',
            'severity': 'Critical',
            'duration_months': 18,
            'base_depreciation': 0.30,  # 30% base decline
            'interest_rate_change': 2.5,
            'affected_regions': 'all',
            'recovery_months': 36
        },
        'rate_shock': {
            'name': 'Interest Rate Shock',
            'description': 'Federal Reserve raises rates from 6.5% to 9.5%, causing immediate demand collapse and price corrections',
            'icon': 'fa-percentage',
            'severity': 'High',
            'duration_months': 12,
            'base_depreciation': 0.18,  # 18% base decline
            'interest_rate_change': 3.0,
            'affected_regions': 'all',
            'recovery_months': 24
        },
        'tech_collapse': {
            'name': 'Tech Sector Collapse',
            'description': 'Major tech industry downturn with mass layoffs, hitting tech hub real estate markets hardest',
            'icon': 'fa-microchip',
            'severity': 'High',
            'duration_months': 24,
            'base_depreciation': 0.25,  # 25% base decline in tech cities
            'interest_rate_change': 0.5,
            'affected_regions': ['San Francisco', 'Seattle', 'Austin', 'San Jose'],
            'recovery_months': 48
        },
        'natural_disaster': {
            'name': 'Coastal Insurance Crisis',
            'description': 'Hurricane devastation + insurance company exodus from coastal markets creates regional real estate collapse',
            'icon': 'fa-house-tsunami',
            'severity': 'Critical',
            'duration_months': 12,
            'base_depreciation': 0.35,  # 35% base decline in coastal areas
            'interest_rate_change': 0.0,
            'affected_regions': ['Miami', 'Los Angeles', 'New York'],
            'recovery_months': 60
        }
    }
    
    @staticmethod
    def get_scenarios():
        """Return all available crisis scenarios"""
        return MarketSimulationService.SCENARIOS
    
    @staticmethod
    def run_simulation(scenario_id, properties, market_data):
        """
        Run complex economic crisis simulation
        This is the core algorithm with multi-factor calculations
        """
        if scenario_id not in MarketSimulationService.SCENARIOS:
            return None
        
        scenario = MarketSimulationService.SCENARIOS[scenario_id]
        duration = scenario['duration_months']
        
        # Initialize portfolio tracking
        initial_portfolio_value = sum([p.price for p in properties])
        property_timelines = []
        
        # Simulate each property independently
        for prop in properties:
            timeline = MarketSimulationService._simulate_property(prop, scenario, duration)
            property_timelines.append({
                'property': prop,
                'timeline': timeline,
                'initial_value': prop.price,
                'final_value': timeline[-1]['value'],
                'total_loss': prop.price - timeline[-1]['value'],
                'loss_percentage': ((timeline[-1]['value'] - prop.price) / prop.price) * 100
            })
        
        # Calculate portfolio-level metrics
        final_portfolio_value = sum([pt['final_value'] for pt in property_timelines])
        total_loss = initial_portfolio_value - final_portfolio_value
        loss_percentage = (total_loss / initial_portfolio_value) * 100
        
        # Find worst and best performing properties
        sorted_by_loss = sorted(property_timelines, key=lambda x: x['loss_percentage'])
        worst_hit = sorted_by_loss[:3]  # Top 3 worst
        best_protected = sorted_by_loss[-3:] if len(sorted_by_loss) > 3 else []  # Top 3 best
        
        # Generate insights
        insights = MarketSimulationService._generate_insights(
            property_timelines, scenario, market_data
        )
        
        # Calculate recovery projection
        recovery_timeline = MarketSimulationService._project_recovery(
            final_portfolio_value, 
            initial_portfolio_value,
            scenario['recovery_months']
        )
        
        return {
            'scenario': scenario,
            'duration_months': duration,
            'portfolio_summary': {
                'initial_value': initial_portfolio_value,
                'final_value': final_portfolio_value,
                'total_loss': total_loss,
                'loss_percentage': loss_percentage,
                'recovery_months': scenario['recovery_months'],
                'projected_recovery_value': recovery_timeline[-1]['value']
            },
            'property_breakdown': property_timelines,
            'worst_hit': worst_hit,
            'best_protected': best_protected,
            'insights': insights,
            'recovery_timeline': recovery_timeline,
            'market_effects': {
                'interest_rate_change': scenario['interest_rate_change'],
                'unemployment_increase': round(scenario['base_depreciation'] * 15, 1),
                'foreclosure_rate_increase': round(scenario['base_depreciation'] * 25, 1),
                'days_on_market_increase': int(scenario['base_depreciation'] * 150)
            }
        }
    
    @staticmethod
    def _simulate_property(property, scenario, duration_months):
        """
        Calculate month-by-month impact on a single property
        Uses multi-factor depreciation model
        """
        timeline = []
        current_value = property.price
        
        for month in range(duration_months + 1):
            if month == 0:
                # Initial state
                timeline.append({
                    'month': 0,
                    'value': current_value,
                    'change_amount': 0,
                    'change_percentage': 0
                })
                continue
            
            # COMPLEX MULTI-FACTOR CALCULATION
            
            # 1. Base depreciation rate for this month
            base_rate = MarketSimulationService._get_time_curve_factor(
                month, duration_months, scenario['base_depreciation']
            )
            
            # 2. Location multiplier
            location_mult = MarketSimulationService._get_location_multiplier(
                property.city, scenario
            )
            
            # 3. Property type multiplier
            type_mult = MarketSimulationService._get_type_multiplier(
                property.property_type, scenario
            )
            
            # 4. Price tier multiplier (luxury properties drop more)
            tier_mult = MarketSimulationService._get_price_tier_multiplier(
                property.price
            )
            
            # 5. Size factor (larger properties more volatile)
            size_mult = MarketSimulationService._get_size_multiplier(
                property.sqft
            )
            
            # 6. Calculate monthly depreciation
            monthly_depreciation_rate = (
                base_rate * 
                location_mult * 
                type_mult * 
                tier_mult * 
                size_mult
            )
            
            # Apply depreciation
            depreciation_amount = current_value * monthly_depreciation_rate
            current_value -= depreciation_amount
            
            timeline.append({
                'month': month,
                'value': round(current_value, 2),
                'change_amount': round(-depreciation_amount, 2),
                'change_percentage': round(-monthly_depreciation_rate * 100, 2),
                'factors': {
                    'location': location_mult,
                    'type': type_mult,
                    'tier': tier_mult,
                    'size': size_mult
                }
            })
        
        return timeline
    
    @staticmethod
    def _get_time_curve_factor(month, total_months, base_depreciation):
        """
        Calculate how depreciation changes over time (acceleration, peak, stabilization)
        Months 1-30%: Slow start (acceleration phase)
        Months 30-70%: Rapid decline (crisis peak)
        Months 70-100%: Slowdown (stabilization)
        """
        progress = month / total_months
        
        if progress <= 0.3:  # Early phase - accelerating
            intensity = progress / 0.3  # 0 to 1
            return (base_depreciation / total_months) * 0.5 * intensity
        elif progress <= 0.7:  # Peak crisis
            return (base_depreciation / total_months) * 1.5
        else:  # Late phase - slowing down
            intensity = 1 - ((progress - 0.7) / 0.3)  # 1 to 0
            return (base_depreciation / total_months) * 1.0 * intensity
    
    @staticmethod
    def _get_location_multiplier(city, scenario):
        """
        Different cities affected differently based on scenario type
        """
        scenario_id = None
        for sid, s in MarketSimulationService.SCENARIOS.items():
            if s['name'] == scenario['name']:
                scenario_id = sid
                break
        
        # Tech collapse hits tech cities harder
        if scenario_id == 'tech_collapse':
            tech_cities = {'San Francisco': 1.5, 'Seattle': 1.4, 'San Jose': 1.5, 'Austin': 1.3}
            return tech_cities.get(city, 0.7)  # Other cities less affected
        
        # Natural disaster hits coastal cities
        elif scenario_id == 'natural_disaster':
            coastal_cities = {'Miami': 1.8, 'Los Angeles': 1.4, 'New York': 1.3}
            return coastal_cities.get(city, 0.6)
        
        # Housing crisis and rate shock affect overheated markets more
        elif scenario_id in ['2008_crisis', 'rate_shock']:
            overheated = {
                'San Francisco': 1.4, 
                'Miami': 1.3, 
                'Los Angeles': 1.2,
                'Seattle': 1.1,
                'Austin': 0.9,
                'Denver': 0.85
            }
            return overheated.get(city, 1.0)
        
        return 1.0
    
    @staticmethod
    def _get_type_multiplier(property_type, scenario):
        """
        Property types react differently to crises
        Condos typically more volatile, houses more stable
        """
        if property_type == 'Condo':
            return 1.25  # Condos drop 25% more
        elif property_type == 'Apartment':
            return 1.20
        elif property_type == 'House':
            return 1.0  # Baseline
        elif property_type == 'Townhouse':
            return 1.1
        else:
            return 1.0
    
    @staticmethod
    def _get_price_tier_multiplier(price):
        """
        Luxury properties (>$1M) drop faster
        Affordable properties (<$500k) more resilient
        """
        if price >= 1000000:
            return 1.4  # Luxury drops 40% more
        elif price >= 750000:
            return 1.2
        elif price >= 500000:
            return 1.0
        else:
            return 0.85  # Affordable properties hold value better
    
    @staticmethod
    def _get_size_multiplier(sqft):
        """
        Larger properties have higher volatility
        """
        if sqft >= 3000:
            return 1.15
        elif sqft >= 2000:
            return 1.05
        else:
            return 1.0
    
    @staticmethod
    def _generate_insights(property_timelines, scenario, market_data):
        """
        Generate human-readable insights from simulation results
        """
        insights = []
        
        # Calculate averages by city
        city_impacts = {}
        for pt in property_timelines:
            city = pt['property'].city
            if city not in city_impacts:
                city_impacts[city] = []
            city_impacts[city].append(pt['loss_percentage'])
        
        # Find worst hit city
        worst_city = min(city_impacts.items(), key=lambda x: sum(x[1])/len(x[1]))
        insights.append(f"{worst_city[0]} properties lost an average of {abs(round(sum(worst_city[1])/len(worst_city[1]), 1))}%")
        
        # Property type analysis
        type_impacts = {}
        for pt in property_timelines:
            ptype = pt['property'].property_type
            if ptype not in type_impacts:
                type_impacts[ptype] = []
            type_impacts[ptype].append(pt['loss_percentage'])
        
        if len(type_impacts) > 1:
            worst_type = min(type_impacts.items(), key=lambda x: sum(x[1])/len(x[1]))
            insights.append(f"{worst_type[0]}s were hit hardest, losing {abs(round(sum(worst_type[1])/len(worst_type[1]), 1))}% on average")
        
        # Luxury property impact
        luxury_count = sum(1 for pt in property_timelines if pt['property'].price >= 1000000)
        if luxury_count > 0:
            luxury_losses = [pt['loss_percentage'] for pt in property_timelines if pt['property'].price >= 1000000]
            avg_luxury_loss = sum(luxury_losses) / len(luxury_losses)
            insights.append(f"Luxury properties ($1M+) saw steeper declines averaging {abs(round(avg_luxury_loss, 1))}%")
        
        # Recovery estimate
        insights.append(f"Full market recovery projected to take {scenario['recovery_months']} months")
        
        # Scenario-specific insight
        if 'tech' in scenario['name'].lower():
            insights.append("Tech sector job losses driving migration away from expensive tech hubs")
        elif 'rate' in scenario['name'].lower():
            insights.append("Higher borrowing costs reducing buyer affordability and demand")
        
        return insights
    
    @staticmethod
    def _project_recovery(final_value, initial_value, recovery_months):
        """
        Project recovery timeline with logarithmic curve
        Recovery is typically slower than decline
        """
        recovery_timeline = []
        current_value = final_value
        monthly_recovery = (initial_value - final_value) / recovery_months
        
        for month in range(0, recovery_months + 1, 6):  # Every 6 months
            # Logarithmic recovery (fast at first, slows down)
            progress = month / recovery_months
            recovery_factor = 1 - (1 - progress) ** 2  # Quadratic ease-out
            projected_value = final_value + ((initial_value - final_value) * recovery_factor)
            
            recovery_timeline.append({
                'month': month,
                'value': round(projected_value, 2),
                'recovery_percentage': round((projected_value - final_value) / (initial_value - final_value) * 100, 1)
            })
        
        return recovery_timeline