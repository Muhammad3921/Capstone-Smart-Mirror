import requests
from tkinter import *
from PIL import ImageTk, Image
import urllib.request
import json

API_KEY = "004add7c3feb40a7ab5233650230410" #move to .env file

data = requests.get("http://api.weatherapi.com/v1/current.json?key=%s&q=%s" % (API_KEY, "Toronto")).json()
def getCurrentWeather(location: str) -> str:
    global data
    request = "http://api.weatherapi.com/v1/current.json?key=%s&q=%s" % (API_KEY, location)
    data = requests.get(request).json()
    return json.dumps(data)

#setting hour = -1 or any number outside of [0..24] gets rid of hourly weather
def getForecast(location: str, days = 3, date = "", hour = "", lang = "") -> str:
    global data
    request = "http://api.weatherapi.com/v1/forecast.json?key=%s&q=%s&days=%d&dt=%s&hour=%s&lang=%s" % (API_KEY, location, days, date, hour, lang)
    data = requests.get(request).json()
    return json.dumps(data)

def updateGUI(frame: Frame) -> Frame:
    region = data['location']['name']
    temp = "Temperature: %d°" % data['current']['temp_c']
    feelsLike = "Feels like: %d°" % data['current']['feelslike_c']
    condition_text = data['current']['condition']['text']
    icon_url = "https:%s" % data['current']['condition']['icon']
    urllib.request.urlretrieve(icon_url, "icon.png")
    condition_icon = ImageTk.PhotoImage(Image.open("icon.png"))

    region_label = Label(frame, text = region).pack()
    temp_label = Label(frame, text = temp).pack()
    feelsLike_label = Label(frame, text = feelsLike).pack()
    conditionIcon_label = Label(frame, image = condition_icon).pack()
    condition_label = Label(frame, text = condition_text).pack()

    return frame