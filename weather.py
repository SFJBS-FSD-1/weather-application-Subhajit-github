import requests
import datetime
import os
from flask import Flask, render_template, request

app = Flask(__name__)  #creating a flask instance


@app.route("/", methods=["GET", "POST"])
def weather():
    if request.method == "POST":
        city = request.form['city']
        apiKey= "8fe6d1156da5eeada955de2c33be8cbe"
        unit = "metric"
        url = "https://api.openweathermap.org/data/2.5/weather?q="+city+"&appid=" +apiKey+ "&units=" + unit + ""
        response = requests.get(url).json()
        if response["cod"] == 200:
            icon = response["weather"][0]["icon"]
            image_url = "http://openweathermap.org/img/wn/" + icon + "@2x.png"
            data = {"icon": image_url,
                "lon_key": response.get("coord")["lon"],
               "lat_key": response.get("coord")["lat"],
               "temp_key": response.get("main")["temp"],
               "city_key": response.get("name"),
               "sunrise": datetime.datetime.fromtimestamp(response.get('sys')['sunrise']),
               "sunset": datetime.datetime.fromtimestamp(response.get('sys')['sunset']),
               "status": 200}
            return render_template("index.html", my_name="Subhajit", data=data)
        elif response["cod"] == "404":
            data = {"message": "This city does not exist. Please enter correct city and try again!", "status": 404 }
            return render_template("index.html", my_name="Subhajit", data=data)
        else:
            data = {"message": response["message"], "status": response["cod"]}
            return render_template("index.html", my_name="Subhajit", data=data)

    else:
        data = None
        return render_template("index.html", my_name="Subhajit", data=data)

port = int(os.environ.get("PORT", 5000))

if __name__ == "__main__":
    app.run(port=port)

