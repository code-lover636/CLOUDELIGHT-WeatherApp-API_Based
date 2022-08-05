import requests, pytz, datetime
from timezonefinder import TimezoneFinder
from dotenv import load_dotenv
import os

def configure():
    load_dotenv()
    
def weatherdata(loc,unit="celsius"):
    key = os.getenv("api")
    url = f"https://api.openweathermap.org/data/2.5/weather?q={loc}&appid={key}"
    response = requests.get(url).json()
    if response['cod'] == '404': 
        return {"icon":"https://cdn-icons-png.flaticon.com/512/1146/1146869.png",
                "temp":"0", 
                "location":"",
                "time":"Please try another city",
                "day":"No weather data available"}

    data = {"latitude":response["coord"]["lat"] if "coord" in response else 0,
            "longitude":response["coord"]["lon"] if "coord" in response else 0,
            "humidity":str(response["main"]["humidity"])+" %" if "humidity" in response["main"] else 0,
            "pressure":str(response["main"]["pressure"])+" hPa" if "pressure" in response["main"] else 0,
            "description":response["weather"][0]["description"] if "weather" in response else 0,
            "speed":str(response["wind"]["speed"])+" mps" if "wind" in response else 0,
            "visibility":str(response["visibility"])+" m" if "visibility" in response else 0,
            "icon": f"http://openweathermap.org/img/wn/{response['weather'][0]['icon']}@2x.png",
            "temp":response["main"]["temp"] if "temp" in response["main"] else 0,
            "location":response["name"] if "name" in response else 0,
            "timezone":response["timezone"] if "timezone" in response else 0,
            "id":response["id"] if "id" in response else 0}
    
    for key in data:
        if data[key]==0:
            data.pop(key)
    if "rain" in response:
        if "1h" in response["rain"]:
            data["rain"] = str(response["rain"]["1h"])+" mm" 
    
    tf = TimezoneFinder()
    tz = tf.timezone_at(lat=data["latitude"], lng=data["longitude"])
    IST = pytz.timezone(tz)
    datetime_ist = datetime.datetime.now(IST)
    data["time"] = datetime_ist.strftime('%I:%M %p')
    data["day"] = datetime_ist.strftime('%A').title()
    
    # temperature scale
    kelvin = data["temp"]
    celsius = kelvin - 273.15
    faranheit = (celsius * 9/5) + 32
    data["temp"] = round(eval(eval("unit")))
    return data
