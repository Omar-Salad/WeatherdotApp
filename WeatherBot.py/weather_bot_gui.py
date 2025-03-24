import tkinter as tk
from tkinter import messagebox
import requests
import pandas as pd
from datetime import datetime
import smtplib
from email.mime.text import MIMEText

# 🔐 CONFIG SECTION — replace with your real credentials
API_KEY = "c78999c42234d1bd92cd36f89ca9032b"
EMAIL_ADDRESS = "your_email@example.com"
EMAIL_PASSWORD = "your_email_password"
RECEIVER_EMAIL = "receiver_email@example.com"

# 🌤 Fetch weather data
def fetch_weather_data(city):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
    response = requests.get(url)

    if response.status_code == 200:
        data = response.json()
        return {
            "City": data["name"],
            "Temperature": data["main"]["temp"],
            "Weather": data["weather"][0]["description"],
            "Humidity": data["main"]["humidity"],
            "Timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    else:
        print(f"🔴 Failed to fetch weather data. Status code: {response.status_code}")
        print(f"🔴 Response: {response.text}")
        return None

# 💾 Save data
def save_to_excel(data):
    df = pd.DataFrame([data])
    df.to_excel("weather_report.xlsx", index=False)

# 📧 Send email
def send_email(city, temp):
    subject = f"Weather Report for {city}"
    body = f"The temperature in {city} is {temp}°C.\nReport sent by WeatherBot."

    msg = MIMEText(body)
    msg['Subject'] = subject
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = RECEIVER_EMAIL

    try:
        server = smtplib.SMTP("smtp.office365.com", 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.sendmail(EMAIL_ADDRESS, RECEIVER_EMAIL, msg.as_string())
        server.quit()
        print("📧 Email sent!")
    except Exception as e:
        print("❌ Email failed:", e)

# 🧠 Handle button click
def get_weather():
    city = entry.get()
    result = fetch_weather_data(city)

    if result:
        output = f"""
City: {result['City']}
Temperature: {result['Temperature']} °C
Weather: {result['Weather']}
Humidity: {result['Humidity']}%
Time: {result['Timestamp']}
        """
        messagebox.showinfo("Weather Report", output)
        save_to_excel(result)
        send_email(result["City"], result["Temperature"])
    else:
        messagebox.showerror("Error", "Could not fetch weather data.")

# 🖼️ GUI Setup
app = tk.Tk()
app.title("WeatherBot App")
app.geometry("300x200")

tk.Label(app, text="Enter city name:").pack(pady=10)
entry = tk.Entry(app)
entry.pack()

tk.Button(app, text="Get Weather", command=get_weather).pack(pady=20)

app.mainloop()
