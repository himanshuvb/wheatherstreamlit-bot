import streamlit as st
from main import WeatherAssistant
from main import LLMClient

st.title("Weather Data Parser & API Assistant")

city = st.text_input("Enter city name")


if st.button("Get Weather"):
    assistant = WeatherAssistant()
    result = assistant.get_weather_insights(LLMClient().extract_city(city))

    st.write(result["recommendation"])