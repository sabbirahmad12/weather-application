import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import pandas as pd
from PIL import Image, ImageTk
import io
import os
from tkinter import colorchooser
from background_manager import BackgroundManager

class WeatherApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Weather Application")
        self.root.geometry("423x630")
        self.root.resizable(False, False)
        
        # API Configuration
        self.API_KEY = "67df88fa82ed1e54ee4a1516ae1fe6e2"
        self.BASE_URL = "http://api.openweathermap.org/data/2.5/weather"
        self.FORECAST_URL = "http://api.openweathermap.org/data/2.5/forecast"
        
        # Variables
        self.temp_unit = tk.StringVar(value="C")
        self.search_history = []
        
        # Create main container
        self.main_frame = ttk.Frame(self.root, padding="10")
        self.main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        title_label = ttk.Label(
            self.main_frame,
            text="Weather Application",
            font=('Helvetica', 24, 'bold')
        )
        title_label.grid(row=0, column=0, columnspan=2, pady=(20, 20))
        
        # Initialize background manager
        self.bg_manager = BackgroundManager(self.main_frame)
        
        # Location Input Section
        self.create_location_section()
        
        # Weather Information Display
        self.create_weather_display()
        
        # Forecast Section
        self.create_forecast_section()
        
        # Date & Time Display
        self.create_datetime_display()
        
        # Footer
        self.create_footer()
        
        # Initialize Excel logging
        self.initialize_excel_log()
        
        # Update time display
        self.update_datetime()
    
    def create_location_section(self):
        # Add title directly in main frame
        
        
        location_frame = ttk.LabelFrame(self.main_frame, text="Location", padding="10")
        location_frame.grid(row=1, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # City entry with history
        self.city_var = tk.StringVar()
        self.city_combo = ttk.Combobox(location_frame, textvariable=self.city_var, width=30)
        self.city_combo.grid(row=0, column=0, padx=5)
        self.city_combo.bind('<Return>', lambda e: self.get_weather())
        
        # Get Weather button
        get_weather_btn = ttk.Button(location_frame, text="Get Weather", command=self.get_weather)
        get_weather_btn.grid(row=0, column=1, padx=5)
        
        # Temperature unit toggle
        unit_frame = ttk.Frame(location_frame)
        unit_frame.grid(row=0, column=2, padx=5)
        
        ttk.Radiobutton(unit_frame, text="°C", variable=self.temp_unit, 
                       value="C", command=self.update_temperature_display).pack(side=tk.LEFT)
        ttk.Radiobutton(unit_frame, text="°F", variable=self.temp_unit, 
                       value="F", command=self.update_temperature_display).pack(side=tk.LEFT)
    
    def create_weather_display(self):
        weather_frame = ttk.LabelFrame(self.main_frame, text="Weather Information", padding="5")
        weather_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Weather Icon
        self.weather_icon_label = ttk.Label(weather_frame)
        self.weather_icon_label.grid(row=0, column=0, rowspan=2, padx=10)
        
        # Temperature and Condition
        self.temp_label = ttk.Label(weather_frame, text="Temperature: --°C", font=("Arial", 14))
        self.temp_label.grid(row=0, column=1, sticky=tk.W)
        
        self.condition_label = ttk.Label(weather_frame, text="Condition: --")
        self.condition_label.grid(row=1, column=1, sticky=tk.W)
        
        # Detailed Information
        details_frame = ttk.Frame(weather_frame)
        details_frame.grid(row=2, column=0, columnspan=2, pady=10)
        
        self.feels_like_label = ttk.Label(details_frame, text="Feels Like: --°C")
        self.feels_like_label.grid(row=0, column=0, sticky=tk.W, padx=5)
        
        self.humidity_label = ttk.Label(details_frame, text="Humidity: --%")
        self.humidity_label.grid(row=0, column=1, sticky=tk.W, padx=5)
        
        self.wind_label = ttk.Label(details_frame, text="Wind: -- km/h")
        self.wind_label.grid(row=1, column=0, sticky=tk.W, padx=5)
        
        self.pressure_label = ttk.Label(details_frame, text="Pressure: -- hPa")
        self.pressure_label.grid(row=1, column=1, sticky=tk.W, padx=5)
        
        self.visibility_label = ttk.Label(details_frame, text="Visibility: -- km")
        self.visibility_label.grid(row=2, column=0, sticky=tk.W, padx=5)
        
        self.sunrise_label = ttk.Label(details_frame, text="Sunrise: --")
        self.sunrise_label.grid(row=2, column=1, sticky=tk.W, padx=5)
        
        self.sunset_label = ttk.Label(details_frame, text="Sunset: --")
        self.sunset_label.grid(row=3, column=0, sticky=tk.W, padx=5)
    
    def create_forecast_section(self):
        forecast_frame = ttk.LabelFrame(self.main_frame, text="5-Day Forecast", padding="5")
        forecast_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=5)
        
        # Create frames for each day
        self.forecast_labels = []
        for i in range(5):
            day_frame = ttk.Frame(forecast_frame)
            day_frame.grid(row=0, column=i, padx=5, pady=5)
            
            # Day label
            day_label = ttk.Label(day_frame, text=f"Day {i+1}")
            day_label.grid(row=0, column=0)
            
            # Weather icon
            icon_label = ttk.Label(day_frame)
            icon_label.grid(row=1, column=0)
            
            # Temperature
            temp_label = ttk.Label(day_frame, text="--°C")
            temp_label.grid(row=2, column=0)
            
            # Condition
            condition_label = ttk.Label(day_frame, text="--")
            condition_label.grid(row=3, column=0)
            
            self.forecast_labels.append({
                'day': day_label,
                'icon': icon_label,
                'temp': temp_label,
                'condition': condition_label
            })
    
    def create_datetime_display(self):
        datetime_frame = ttk.Frame(self.main_frame)
        datetime_frame.grid(row=4, column=0, columnspan=2, pady=5)
        
        self.date_label = ttk.Label(datetime_frame, text="Date: --")
        self.date_label.grid(row=0, column=0, padx=5)
        
        self.time_label = ttk.Label(datetime_frame, text="Time: --")
        self.time_label.grid(row=0, column=1, padx=5)
        
        self.last_updated_label = ttk.Label(datetime_frame, text="Last Updated: --")
        self.last_updated_label.grid(row=0, column=2, padx=5)
    
    def create_footer(self):
        footer_frame = ttk.Frame(self.main_frame)
        footer_frame.grid(row=5, column=0, columnspan=2, pady=10)
        
        copyright_label = ttk.Label(
            footer_frame, 
            text="© 2025 Weather Application. All rights reserved.",
            font=('Helvetica', 8)
        )
        copyright_label.grid(row=0, column=0, padx=5)
        
    
    def get_weather(self):
        city = self.city_var.get()
        if not city:
            messagebox.showerror("Error", "Please enter a city name")
            return
        
        try:
            # Get current weather
            params = {
                'q': city,
                'appid': self.API_KEY,
                'units': 'metric'
            }
            
            response = requests.get(self.BASE_URL, params=params)
            data = response.json()
            
            if response.status_code == 200:
                self.update_weather_display(data)
                self.log_to_excel(data)
                
                # Get forecast
                forecast_response = requests.get(self.FORECAST_URL, params=params)
                forecast_data = forecast_response.json()
                if forecast_response.status_code == 200:
                    self.update_forecast_display(forecast_data)
                
                # Update search history
                if city not in self.search_history:
                    self.search_history.append(city)
                    self.city_combo['values'] = self.search_history
                
                # Update background color based on weather
                self.bg_manager.update_background(data['weather'][0]['main'])
            else:
                messagebox.showerror("Error", f"Error: {data['message']}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Failed to fetch weather data: {str(e)}")
    
    def update_weather_display(self, data):
        # Update main weather information
        temp = data['main']['temp']
        feels_like = data['main']['feels_like']
        condition = data['weather'][0]['main']
        humidity = data['main']['humidity']
        wind_speed = data['wind']['speed']
        pressure = data['main']['pressure']
        visibility = data['visibility'] / 1000  # Convert to km
        
        # Update sunrise and sunset times
        sunrise = datetime.fromtimestamp(data['sys']['sunrise']).strftime('%H:%M')
        sunset = datetime.fromtimestamp(data['sys']['sunset']).strftime('%H:%M')
        
        # Convert temperature based on selected unit
        if self.temp_unit.get() == "F":
            temp = (temp * 9/5) + 32
            feels_like = (feels_like * 9/5) + 32
            temp_unit = "°F"
        else:
            temp_unit = "°C"
        
        # Update labels
        self.temp_label.config(text=f"Temperature: {temp:.1f}{temp_unit}")
        self.condition_label.config(text=f"Condition: {condition}")
        self.feels_like_label.config(text=f"Feels Like: {feels_like:.1f}{temp_unit}")
        self.humidity_label.config(text=f"Humidity: {humidity}%")
        self.wind_label.config(text=f"Wind: {wind_speed} km/h")
        self.pressure_label.config(text=f"Pressure: {pressure} hPa")
        self.visibility_label.config(text=f"Visibility: {visibility:.1f} km")
        self.sunrise_label.config(text=f"Sunrise: {sunrise}")
        self.sunset_label.config(text=f"Sunset: {sunset}")
        
        # Update last updated time
        current_time = datetime.now().strftime('%H:%M:%S')
        self.last_updated_label.config(text=f"Last Updated: {current_time}")
        
        # Update weather icon
        icon_code = data['weather'][0]['icon']
        self.update_weather_icon(icon_code)
    
    def update_forecast_display(self, data):
        # Get forecast for next 5 days (every 24 hours)
        forecast_list = data['list']
        day_forecasts = []
        
        for i in range(0, len(forecast_list), 8):  # 8 entries per day (3-hour intervals)
            if len(day_forecasts) < 5:  # Only get 5 days
                day_forecasts.append(forecast_list[i])
        
        # Update forecast labels
        for i, forecast in enumerate(day_forecasts):
            if i < len(self.forecast_labels):
                # Convert temperature based on selected unit
                temp = forecast['main']['temp']
                if self.temp_unit.get() == "F":
                    temp = (temp * 9/5) + 32
                    temp_unit = "°F"
                else:
                    temp_unit = "°C"
                
                # Update labels
                self.forecast_labels[i]['day'].config(
                    text=datetime.fromtimestamp(forecast['dt']).strftime('%a'))
                self.forecast_labels[i]['temp'].config(text=f"{temp:.1f}{temp_unit}")
                self.forecast_labels[i]['condition'].config(
                    text=forecast['weather'][0]['main'])
                
                # Update icon
                icon_code = forecast['weather'][0]['icon']
                self.update_forecast_icon(i, icon_code)
    
    def update_forecast_icon(self, index, icon_code):
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}.png"
            response = requests.get(icon_url)
            image_data = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image_data)
            self.forecast_labels[index]['icon'].configure(image=photo)
            self.forecast_labels[index]['icon'].image = photo
        except Exception as e:
            print(f"Failed to load forecast icon: {str(e)}")
    
    def update_temperature_display(self):
        # Refresh display with new temperature unit
        if hasattr(self, 'last_weather_data'):
            self.update_weather_display(self.last_weather_data)
            if hasattr(self, 'last_forecast_data'):
                self.update_forecast_display(self.last_forecast_data)
    
    def initialize_excel_log(self):
        # Create data folder if it doesn't exist
        data_folder = "data"
        if not os.path.exists(data_folder):
            os.makedirs(data_folder)
            
        self.excel_file = os.path.join(data_folder, "weather_log.xlsx")
        if not os.path.exists(self.excel_file):
            df = pd.DataFrame(columns=[
                "Date", "Time", "City", "Temperature", "Condition",
                "Humidity", "Wind Speed", "Pressure", "Visibility"
            ])
            df.to_excel(self.excel_file, index=False)
    
    def update_datetime(self):
        current_time = datetime.now()
        self.date_label.config(text=f"Date: {current_time.strftime('%Y-%m-%d')}")
        self.time_label.config(text=f"Time: {current_time.strftime('%H:%M:%S')}")
        self.root.after(1000, self.update_datetime)
    
    def update_weather_icon(self, icon_code):
        try:
            icon_url = f"http://openweathermap.org/img/wn/{icon_code}@2x.png"
            response = requests.get(icon_url)
            image_data = Image.open(io.BytesIO(response.content))
            photo = ImageTk.PhotoImage(image_data)
            self.weather_icon_label.configure(image=photo)
            self.weather_icon_label.image = photo
        except Exception as e:
            print(f"Failed to load weather icon: {str(e)}")
    
    def log_to_excel(self, data):
        try:
            # Create new data dictionary
            new_data = {
                "Date": datetime.now().strftime('%Y-%m-%d'),
                "Time": datetime.now().strftime('%H:%M:%S'),
                "City": self.city_var.get(),
                "Temperature": data['main']['temp'],
                "Condition": data['weather'][0]['main'],
                "Humidity": data['main']['humidity'],
                "Wind Speed": data['wind']['speed'],
                "Pressure": data['main']['pressure'],
                "Visibility": data['visibility'] / 1000
            }
            
            # Read existing data or create new DataFrame
            if os.path.exists(self.excel_file):
                df = pd.read_excel(self.excel_file)
                # Convert new_data to DataFrame with same columns
                new_df = pd.DataFrame([new_data], columns=df.columns)
                # Concatenate with proper dtypes
                df = pd.concat([df, new_df], ignore_index=True)
            else:
                # Create new DataFrame if file doesn't exist
                df = pd.DataFrame([new_data])
            
            # Save to Excel
            df.to_excel(self.excel_file, index=False)
            
        except Exception as e:
            print(f"Failed to log to Excel: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = WeatherApp(root)
    root.mainloop() 