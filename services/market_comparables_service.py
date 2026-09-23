import random

class MarketComparablesService:
    """
    Provides market comparable and trend data for the platform.
    
    Note: This service generates simulated market data for demonstration
    purposes rather than pulling from a live third-party source.
    """

    def get_market_comparables(self, city, state):
        """Get comparable properties in the market"""
        try:
            comparables = self._generate_comparables(city, state)
            return comparables
        except Exception as e:
            print(f"Comparables Error: {str(e)}")
            return []

    def _generate_comparables(self, city, state):
        """Generate comparable properties for market analysis"""
        comparables = []

        for i in range(5):
            comparable = {
                'address': f"{random.randint(100, 9999)} {random.choice(['Main', 'Oak', 'Pine', 'Maple', 'Cedar'])} St",
                'city': city,
                'state': state,
                'price': random.randint(400000, 1200000),
                'bedrooms': random.randint(2, 4),
                'bathrooms': random.choice([2, 2.5, 3]),
                'sqft': random.randint(1500, 2800),
                'price_per_sqft': 0,
                'days_on_market': random.randint(5, 60)
            }
            comparable['price_per_sqft'] = round(comparable['price'] / comparable['sqft'], 2)
            comparables.append(comparable)

        return comparables

    def get_market_trends(self, city, state):
        """Get simulated market trends for a location"""
        return {
            'median_price': random.randint(500000, 900000),
            'price_change_month': round(random.uniform(-2.5, 5.0), 2),
            'price_change_year': round(random.uniform(-5.0, 15.0), 2),
            'days_on_market': random.randint(20, 45),
            'inventory': random.randint(100, 500)
        }