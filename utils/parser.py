"""
Weather data parser module.
Handles parsing and validation of weather API responses.
"""

from typing import Dict, Any


class WeatherParser:
    """Parser for weather API responses."""
    
    def parse_weather_data(self, raw_data: Dict[str, Any]) -> Dict[str, Any]:
        """Parse raw weather API response into structured format."""
        # TODO: Extract the city name from the 'name' field in raw_data
        # TODO: Extract the country code from the 'country' field inside raw_data['sys']
        # TODO: Extract the temperature from the 'temp' field inside raw_data['main']
        # TODO: Extract the feels-like temperature from the 'feels_like' field inside raw_data['main']
        # TODO: Extract the humidity from the 'humidity' field inside raw_data['main']
        # TODO: Extract the weather description from the first item in raw_data['weather']
        # TODO: Extract the wind speed from the 'speed' field inside raw_data['wind']
        # TODO: Return a dictionary containing city, country, temperature, feels_like, description, humidity, and wind_speed   
        city = raw_data.get('name', 'Unknown')
        country = raw_data.get('sys', {}).get('country', 'Unknown')
        temperature = raw_data.get('main', {}).get('temp', 'N/A')
        feels_like = raw_data.get('main', {}).get('feels_like', 'N/A')
        humidity = raw_data.get('main', {}).get('humidity', 'N/A')
        description = raw_data.get('weather', [{}])[0].get('description', 'N/A')
        wind_speed = raw_data.get('wind', {}).get('speed', 'N/A')
        #debugging print statements
        #print(f"Parsed Weather Data: City={city}, Country={country}, Temperature={temperature}, Feels Like={feels_like}, Description={description}, Humidity={humidity}, Wind Speed={wind_speed}")
        return {
            "city": city,
            "country": country,
            "temperature": temperature,
            "feels_like": feels_like,
            "description": description,
            "humidity": humidity,
            "wind_speed": wind_speed
        }    
    
    def validate_weather_data(self, weather_data: Dict[str, Any]) -> bool:
        """Validate that weather data has required fields."""

        required_fields = ['city', 'temperature', 'description', 'humidity', 'wind_speed', 'feels_like', 'country']
        # TODO: Check if required fields exist and are not None. Return True if all fields are present, False otherwise
        for field in required_fields:
            if field not in weather_data or weather_data[field] is None:
                return False
        return True
    
    def format_weather_for_llm(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data for LLM prompt."""
        # TODO: Return a formatted string containing City, Country, Temperature,
        #       Feels Like, Description, Humidity, and Wind Speed.
        #       Use 'Unknown' for missing city or country and 'N/A' for other
        #       missing values. Include appropriate units (°C, %, m/s).
        #       Make sure to follow the required naming conventions.
        weather_city = weather_data.get('city', 'Unknown')
        weather_country = weather_data.get('country', 'Unknown')        
        weather_temperature = weather_data.get('temperature', 'N/A')
        weather_feels_like = weather_data.get('feels_like', 'N/A')
        weather_description = weather_data.get('description', 'N/A')
        weather_humidity = weather_data.get('humidity', 'N/A')
        weather_wind_speed = weather_data.get('wind_speed', 'N/A')
        weather_info = (
            f"City: {weather_city}\n"
            f"Country: {weather_country}\n"
            f"Temperature: {weather_temperature}°C\n"
            f"Feels Like: {weather_feels_like}°C\n"
            f"Description: {weather_description}\n"
            f"Humidity: {weather_humidity}%\n"
            f"Wind Speed: {weather_wind_speed} m/s"
        )
        return weather_info
