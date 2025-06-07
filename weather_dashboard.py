import requests
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime

# --- Configuration ---
API_KEY = '9457f2aefa1d082c7a4e227ce1a0f56f'
CITY_NAME = 'London'  
UNITS = 'metric' 

# --- OpenWeatherMap API Endpoint ---
BASE_URL = f"http://api.openweathermap.org/data/2.5/forecast?q={CITY_NAME}&appid={API_KEY}&units={UNITS}"

# --- 1. Fetch Data from API ---
def fetch_weather_data(url):
    """Fetches weather data from the given URL."""
    try:
        response = requests.get(url)
        response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

# --- 2. Process Data ---
def process_weather_data(data):
    """Processes the raw JSON data to extract relevant information."""
    if not data or 'list' not in data:
        print("No data or invalid data format received.")
        return [], [], [], []

    timestamps = []
    temperatures = []
    feels_like_temps = []
    humidities = []

    for item in data['list']:
        dt_txt = item['dt_txt']
        temp = item['main']['temp']
        feels_like = item['main']['feels_like']
        humidity = item['main']['humidity']

        timestamps.append(datetime.strptime(dt_txt, '%Y-%m-%d %H:%M:%S'))
        temperatures.append(temp)
        feels_like_temps.append(feels_like)
        humidities.append(humidity)

    return timestamps, temperatures, feels_like_temps, humidities

# --- 3. Create Visualizations (Dashboard) ---
def create_weather_dashboard(timestamps, temperatures, feels_like_temps, humidities, city_name, units):
    """Creates a dashboard of weather visualizations."""
    if not timestamps:
        print("No data to visualize.")
        return

    plt.style.use('seaborn-v0_8-darkgrid') 
    fig, axs = plt.subplots(3, 1, figsize=(12, 18)) 
    fig.suptitle(f'5-Day Weather Forecast for {city_name}', fontsize=20)

    # Plot 1: Temperature Over Time
    sns.lineplot(x=timestamps, y=temperatures, marker='o', ax=axs[0], color='skyblue', label='Actual Temp')
    sns.lineplot(x=timestamps, y=feels_like_temps, marker='x', ax=axs[0], color='salmon', linestyle='--', label='Feels Like')
    axs[0].set_title('Temperature Forecast', fontsize=16)
    axs[0].set_xlabel('Date and Time', fontsize=12)
    axs[0].set_ylabel(f'Temperature (°{units.capitalize()})', fontsize=12)
    axs[0].tick_params(axis='x', rotation=45)
    axs[0].legend()
    axs[0].grid(True)

    # Plot 2: Humidity Over Time
    sns.lineplot(x=timestamps, y=humidities, marker='o', ax=axs[1], color='lightgreen')
    axs[1].set_title('Humidity Forecast', fontsize=16)
    axs[1].set_xlabel('Date and Time', fontsize=12)
    axs[1].set_ylabel('Humidity (%)', fontsize=12)
    axs[1].tick_params(axis='x', rotation=45)
    axs[1].grid(True)

    # Plot 3: Temperature Distribution (using a histogram or density plot)
    sns.histplot(temperatures, kde=True, ax=axs[2], color='lightcoral', bins=10)
    axs[2].set_title('Temperature Distribution', fontsize=16)
    axs[2].set_xlabel(f'Temperature (°{units.capitalize()})', fontsize=12)
    axs[2].set_ylabel('Frequency', fontsize=12)
    axs[2].grid(True)

    plt.tight_layout(rect=[0, 0.03, 1, 0.96]) 
    plt.show()

# --- Main Execution ---
if __name__ == "__main__":
    print(f"Fetching weather data for {CITY_NAME}...")
    raw_data = fetch_weather_data(BASE_URL)

    if raw_data:
        timestamps, temperatures, feels_like_temps, humidities = process_weather_data(raw_data)
        if timestamps: 
            create_weather_dashboard(timestamps, temperatures, feels_like_temps, humidities, CITY_NAME, UNITS)
        else:
            print("Could not process weather data for visualization.")
    else:
        print("Failed to fetch weather data. Please check your API key, city name, and internet connection.")
