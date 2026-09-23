import requests
from config import Config

class WeatherService:
    def __init__(self):
        self.api_key = Config.WEATHER_API_KEY
        self.base_url = "http://api.openweathermap.org/data/2.5"
    
    def get_weather_impact(self, city, state):
        """
        Get weather data for a city and calculate impact on property value
        Good weather = positive impact, bad weather = negative impact
        """
        try:
            # Get current weather
            url = f"{self.base_url}/weather"
            params = {
                'q': f"{city},{state},US",
                'appid': self.api_key,
                'units': 'imperial'
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract weather info
                temp = data['main']['temp']
                description = data['weather'][0]['description']
                humidity = data['main']['humidity']
                
                # Calculate impact (-0.05 to +0.05 multiplier on property value)
                impact = self._calculate_impact(temp, description, humidity)
                
                return {
                    'temperature': temp,
                    'description': description,
                    'humidity': humidity,
                    'impact': impact,
                    'impact_percentage': round(impact * 100, 2)
                }
            else:
                return self._default_weather()
                
        except Exception as e:
            print(f"Weather Service Error: {str(e)}")
            return self._default_weather()
    
    def _calculate_impact(self, temp, description, humidity):
        """Calculate weather impact on property value"""
        impact = 0.0
        
        # Temperature impact (ideal: 65-75°F)
        if 65 <= temp <= 75:
            impact += 0.02
        elif temp < 32 or temp > 95:
            impact -= 0.03
        
        # Weather condition impact
        negative_weather = ['rain', 'storm', 'snow', 'drizzle']
        positive_weather = ['clear', 'sunny']
        
        for weather in negative_weather:
            if weather in description.lower():
                impact -= 0.02
                break
        
        for weather in positive_weather:
            if weather in description.lower():
                impact += 0.02
                break
        
        # Humidity impact
        if humidity > 80:
            impact -= 0.01
        elif 40 <= humidity <= 60:
            impact += 0.01
        
        # Cap the impact between -0.05 and +0.05
        return max(-0.05, min(0.05, impact))
    
    def _default_weather(self):
        """Default weather data if API fails"""
        return {
            'temperature': 72,
            'description': 'partly cloudy',
            'humidity': 50,
            'impact': 0.0,
            'impact_percentage': 0.0
        }
    
    def get_forecast(self, city, state):
        """Get 5-day weather forecast"""
        try:
            url = f"{self.base_url}/forecast"
            params = {
                'q': f"{city},{state},US",
                'appid': self.api_key,
                'units': 'imperial',
                'cnt': 5  # 5 data points
            }
            
            response = requests.get(url, params=params, timeout=10)
            
            if response.status_code == 200:
                data = response.json()
                forecast_list = []
                
                for item in data['list'][:5]:
                    forecast_list.append({
                        'date': item['dt_txt'],
                        'temp': item['main']['temp'],
                        'description': item['weather'][0]['description']
                    })
                
                return forecast_list
            else:
                return []
                
        except Exception as e:
            print(f"Forecast Error: {str(e)}")
            return []