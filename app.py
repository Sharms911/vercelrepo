from flask import Flask, render_template, request, url_for
import requests
from datetime import datetime, timedelta
import calendar
import matplotlib

matplotlib.use('Agg')
from matplotlib import pyplot
from flask import redirect
from PIL import Image

app = Flask(__name__)


@app.route('/')
def index(dt_txt=None):

    try:
        response = requests.get('http://ip-api.com/json')
        data = response.json()
        city = data['city']
        country = data['country']
        lon = data['lon']
        lat = data['lat']
    except Exception as e:
        print("Error occurred while retrieving city:", e)

    api_key = '219ee2cd1c341d93688001529dc36a06'

    url = "http://api.openweathermap.org/data/2.5/forecast?q=" + city + "&appid=" + api_key
    response = requests.get(url).json()

    forecast_list = response["list"]
    forecast_data = []
    index = 0
    while index < len(forecast_list):
        dt = forecast_list[index]['dt']
        temp = round(forecast_list[index]["main"]["temp"] - 273.15)
        desc = forecast_list[index]["weather"][0]["description"]
        icon = forecast_list[index]["weather"][0]["icon"]
        tempmin = round(forecast_list[index]["main"]["temp_min"] - 273.15)
        tempmax = round(forecast_list[index]["main"]["temp_max"] - 273.15)
        weather_data = forecast_list[index]["weather"]
        if "rain" in weather_data:
            precipitation = weather_data["rain"].get("3h", 0)
        else:
            precipitation = 0

        humidity = forecast_list[index]["main"]["humidity"]
        posted_day = datetime.fromtimestamp(dt).strftime("%A")
        posted_hour = datetime.fromtimestamp(dt).strftime("%H")
        posted_minute = datetime.fromtimestamp(dt).strftime("%M")
        if int(posted_hour) <= 11:
            posted_am_pm = "am"
        elif int(posted_hour) == 12:
            posted_am_pm = "pm"
        else:
            posted_am_pm = "pm"
            posted_hour = str(int(posted_hour) - 12)
        wind = forecast_list[index]['wind']['speed']

        imageurl = f"https://maps.googleapis.com/maps/api/staticmap?center={lat},{lon}&zoom=12&size=400x400&key=AIzaSyCp-LazNcSfVtsjCeDXgk8i42vsmHgYHU4"
        print(imageurl)

        dict = {
            "dt": dt,
            "temp": temp,
            "desc": desc,
            "icon": "http://openweathermap.org/img/w/" + icon + ".png",
            "tempmin": tempmin,
            "tempmax": tempmax,
            "precipitation": precipitation,
            "humidity": humidity,
            "wind": wind,
            "posted_day": posted_day,
            "posted_hour": posted_hour,
            "posted_minute": posted_minute,
            "posted_am_pm": posted_am_pm,
            "city": city,
            "lon": lon,
            "lat": lat,
            "imageurl": imageurl
        }

        forecast_data.append(dict)

        index += 8
        # GRAPH FOR TEMPERATURE
        temptoday = int(response['list'][0]['main']['temp'])
        temptoday1 = int(response['list'][1]['main']['temp'])
        temptoday2 = int(response['list'][2]['main']['temp'])
        temptoday3 = int(response['list'][3]['main']['temp'])
        temptoday4 = int(response['list'][4]['main']['temp'])
        temptoday5 = int(response['list'][5]['main']['temp'])
        temptoday6 = int(response['list'][6]['main']['temp'])
        temptoday7 = int(response['list'][7]['main']['temp'])
        templist = [temptoday, temptoday1, temptoday2, temptoday3, temptoday4, temptoday5, temptoday6, temptoday7]
        hour_data = ["12am", "3am", "6am", "9am", "12pm", "3pm", "6pm", "9pm"]
        pyplot.figure(figsize=(14, 3))
        pyplot.plot(hour_data, templist)
        pyplot.savefig("static/graph.png")
        image = Image.open('static/graph.png')
        crop_box = (130, 0, 1280, 300)
        cropped_image = image.crop(crop_box)
        cropped_image = cropped_image.convert('RGB')
        cropped_image.save('static/cropped_graph.png')

        #RAIN GRAPH
        raintoday = response["list"][1].get("rain", {}).get("3h", 0) * 100
        raintoday1 = response["list"][2].get("rain", {}).get("3h", 0) * 100
        raintoday2 = response["list"][3].get("rain", {}).get("3h", 0) * 100
        raintoday3 = response["list"][4].get("rain", {}).get("3h", 0) * 100
        raintoday4 = response["list"][5].get("rain", {}).get("3h", 0) * 100
        raintoday5 = response["list"][6].get("rain", {}).get("3h", 0) * 100
        raintoday6 = response["list"][7].get("rain", {}).get("3h", 0) * 100
        rainlist = [raintoday1, raintoday2, raintoday3, raintoday4, raintoday5, raintoday6, ]
        min_length = min(len(hour_data), len(rainlist))
        hour_data = hour_data[:min_length]
        rainlist = rainlist[:min_length]
        pyplot.figure(figsize=(14, 3))
        pyplot.plot(hour_data, rainlist)
        pyplot.savefig("static/raingraph.png")
        image = Image.open('static/raingraph.png')
        crop_box = (130, 0, 1280, 300)
        cropped_image = image.crop(crop_box)
        cropped_image = cropped_image.convert('RGB')
        cropped_image.save('static/cropped_raingraph.png')

        #GRAPH FOR THE WIND
        windtoday = response['list'][0]['wind']['speed']
        windtoday1 = response['list'][3]['wind']['speed']
        windtoday2 = response['list'][6]['wind']['speed']
        windtoday3 = response['list'][9]['wind']['speed']
        windtoday4 = response['list'][12]['wind']['speed']
        windtoday5 = response['list'][15]['wind']['speed']
        windtoday6 = response['list'][18]['wind']['speed']
        windtoday7 = response['list'][21]['wind']['speed']
        hour_data = [0, 3, 6, 9, 12, 15, 18, 21]
        windlist = [windtoday, windtoday1, windtoday2, windtoday3, windtoday4, windtoday5, windtoday6, windtoday7]
        pyplot.figure(figsize=(14, 3))
        pyplot.plot(hour_data, windlist)
        pyplot.savefig("static/windgraph.png")
        image = Image.open('static/windgraph.png')
        crop_box = (130, 0, 1280, 300)
        cropped_image = image.crop(crop_box)
        cropped_image = cropped_image.convert('RGB')
        cropped_image.save('static/cropped_windgraph.png')

    return render_template('index.html', forecast_data=forecast_data)


if __name__ == '__main__':
    app.run(debug=True)
