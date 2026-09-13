import os
import json
import requests
from dotenv import load_dotenv
from typing import Optional, Dict, Any
from utils.config import SYSTEM_PROMPT
from utils.parser import WeatherParser
from google import genai

# TODO: Load environment variables]
env = load_dotenv()

class WeatherAPIClient:
    """Client for fetching weather data from OpenWeatherMap API."""
    
    def __init__(self, api_key: Optional[str] = None):
        # TODO: Initialize API key from parameter or env var WEATHER_API_KEY
        self.api_key = api_key or os.getenv("WEATHER_API_KEY")

        # TODO: Raise ValueError if no key
        if not self.api_key:
            raise ValueError("API key is required")

        # TODO: Set base URL for weather API
        
#Expected Weather API Request:

#Use the OpenWeatherMap current-weather endpoint.

#https://api.openweathermap.org/data/2.5/weather

#The request must use these parameters:

#{
#  "q": "London",
#  "appid": "YOUR_API_KEY",
#  "units": "metric"
#}
        self.base_url = "https://api.openweathermap.org/data/2.5/weather"
    
    def get_weather(self, city: str) -> Dict[str, Any]:
        """Fetch weather data for a given city."""
        # TODO: Make an HTTP GET request to the weather API using the city,
        #       API key, metric units, and a timeout of 10 seconds
       
        # TODO: For HTTP 401, raise ValueError with "Invalid API key"
        # TODO: For HTTP 404, raise ValueError with "City '<city>' not found"
        # TODO: For HTTP 429, raise ValueError with "API rate limit exceeded"
        # TODO: For other HTTP errors, raise ValueError with the HTTP status code as given "API error: {status_code}"
        # TODO: For a timeout, raise ValueError with "Request timeout - please try again"
        # TODO: For a connection error, raise ValueError with "Network error - please check your connection"
        # TODO: For any other exception, raise ValueError with the exception message "Unexpected error: {error}"
        # TODO: Return the JSON response when the request is successful
        try:
            params = {
                "q": city,
                "appid": self.api_key,
                "units": "metric"
            }
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()  # Raise an error for bad responses
            #print(f"Weather API response for {city}: {response.json()}")  # Debugging line
            return response.json()
        except requests.exceptions.HTTPError as http_err:
            if response.status_code == 401:
                raise ValueError("Invalid API key")
            elif response.status_code == 404:
                raise ValueError(f"City '{city}' not found")
            elif response.status_code == 429:
                raise ValueError("API rate limit exceeded")
            else:
                raise ValueError(f"API error: {response.status_code}")
        except requests.exceptions.Timeout:
            raise ValueError("Request timeout - please try again")              
        except requests.exceptions.ConnectionError:
            raise ValueError("Network error - please check your connection")
        except Exception as e:
            raise ValueError(f"Unexpected error: {str(e)}")


class LLMClient:
    """Client for calling Gemini API to generate weather insights."""
    
    def __init__(self, api_key: Optional[str] = None):
        # TODO: Initialize API key from parameter or env var GEMINI_API_KEY
        self.api_key = api_key or os.getenv("GEMINI_API_KEY")

        # TODO: Raise ValueError if no key
        if not self.api_key:
            raise ValueError("API key is required")

        # TODO: Initialize Gemini client
        self.client = genai.Client(api_key=self.api_key)

        # TODO: Get the model name from the environment variable "GEMINI_MODEL"
        #       using os, and use "gemini-2.5-flash" as the default model
        self.model = os.getenv("GEMINI_MODEL") or "gemini-2.5-flash"
    
    def generate_insights(self, weather_data: Dict[str, Any]) -> str:
        """Generate weather insights and recommendations using LLM."""
        # TODO: Format 'weather_data' parameter for LLM prompt using the function: _format_weather_for_llm
        formatted_weather = self._format_weather_for_llm(weather_data)
        # TODO: Insert the formatted weather data into SYSTEM_PROMPT
        prompt = SYSTEM_PROMPT.format(weather_data=formatted_weather)
        # TODO: Generate content using the configured model and prompt
        # TODO: Return a fallback message if the generated response is empty
        # TODO: Return the generated response after removing extra whitespace
        # TODO: Handle any exception and return an appropriate error message

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )
            
            generated_text = response.text
            if not generated_text:
                return "No insights could be generated for the provided weather data."
            return generated_text
        except Exception as e:
            raise ValueError(f"Error generating insights: {str(e)}")
        

    def _format_weather_for_llm(self, weather_data: Dict[str, Any]) -> str:
        """Format weather data for LLM prompt."""
        # TODO: Format City using 'Unknown' if not provided
        # TODO: Format Country using 'Unknown' if not provided
        # TODO: Format Temperature in °C using 'N/A' if not provided
        # TODO: Format Feels Like in °C using 'N/A' if not provided
        # TODO: Format Description using 'N/A' if not provided
        # TODO: Format Humidity in % using 'N/A' if not provided
        # TODO: Format Wind Speed in m/s using 'N/A' if not provided
        # TODO: Return the formatted weather information as a string
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
    def extract_city(self, user_input: str) -> str:
        """Extract the city name from a natural-language weather query."""

        prompt = f"""
        Extract the city name from the following user input.
        user might only give city name, or might give a full sentence like "What's the weather in London?".
        extract city and give city name only one word the city itself
        User input: {user_input}

        Return ONLY the city name.
        Do not return any explanation.
        """

        try:
            response = self.client.models.generate_content(
                model=self.model,
                contents=prompt
            )

            city = response.text.strip()

            if not city:
                raise ValueError("Could not determine city from input.")

            return city

        except Exception as e:
            raise ValueError(f"Error extracting city: {str(e)}")


class WeatherAssistant:
    """Main assistant that coordinates weather data fetching and insights generation."""
    
    def __init__(self):
        # TODO: Initialize WeatherAPIClient Class
        self.weather_client = WeatherAPIClient()
        # TODO: Initialize LLMClient Class
        self.llm_client = LLMClient()
        # TODO: Initialize WeatherParser Class
        self.parser = WeatherParser()
    
    def get_weather_insights(self, city: str) -> Dict[str, Any]:
        """Get weather data and generate insights for a given city."""

        # TODO: Fetch the raw weather data for the given city
        # TODO: Parse the raw weather data into a structured format
        # TODO: Validate the parsed weather data using the function: validate_weather_data and raise an appropriate error if invalid
        # TODO: Generate weather insights using the parsed weather data
        # TODO: Return a structured response containing city, country, temperature,
        #       feels_like, description, humidity, wind_speed, recommendation, and insights
        # TODO: Handle any exception and return the error along with the city and
        #       an appropriate recommendation message

        try:
            raw_weather_data = self.weather_client.get_weather(city)
            parsed_weather_data = self.parser.parse_weather_data(raw_weather_data)
            if not self.parser.validate_weather_data(parsed_weather_data):
                raise ValueError("Invalid weather data received from API.")
            insights = self.llm_client.generate_insights(parsed_weather_data)
            return {
                "city": parsed_weather_data.get('city', 'Unknown'),
                "country": parsed_weather_data.get('country', 'Unknown'),
                "temperature": parsed_weather_data.get('temperature', 'N/A'),
                "feels_like": parsed_weather_data.get('feels_like', 'N/A'),
                "description": parsed_weather_data.get('description', 'N/A'),
                "humidity": parsed_weather_data.get('humidity', 'N/A'),
                "wind_speed": parsed_weather_data.get('wind_speed', 'N/A'),
                "recommendation": insights,
                "insights": insights
            }
        except Exception as e:
            return {
                "city": city,
                "error": str(e),
                "recommendation": "Unable to provide insights due to an error." + str(e)
            }

def main():
    """Main function to demonstrate the weather assistant functionality."""
    test_cities = [
        "London",
        "New York", 
        "Tokyo",
        "Paris",
        "Sydney"
    ]
    
    print("Weather Data Parser & API Assistant")
    print("=" * 50)
    
    assistant = WeatherAssistant()
    
    for city in test_cities:
        print(f"\nGetting weather insights for {city}...")
        try:
            result = assistant.get_weather_insights(city)
            print(f"Temperature: {result.get('temperature', 'N/A')}°C")
            print(f"Description: {result.get('description', 'N/A')}")
            print(f"Recommendation: {result.get('recommendation', 'N/A')}")
        except Exception as e:
            print(f"Error: {str(e)}")
        print("-" * 50)


if __name__ == "__main__":
    main()
