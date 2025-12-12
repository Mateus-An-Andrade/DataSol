from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from datetime import date


app = Flask(__name__)
CORS(app)


@app.get("/clima")
def clima():

    url = (
      "https://api.open-meteo.com/v1/forecast?latitude=,-22.688504781081985&longitude=,-43.352751556386316&hourly=temperature_2m,direct_radiation&timezone=America%2FSao_Paulo"
    )

    resposta = requests.get(url).json()

    return resposta


@app.get("/production_potential")
def production_potential():

    clima_data = clima()
    irrads = clima_data["hourly"]["direct_radiation"]
    time = clima_data["hourly"]["time"]

    pannel_area = 3.0
    efic = 0.21

    today_api = time[0].split("T")[0]

    today = str(date.today())

    hours =[]
    values = []

    for irrad in range(len(time)):
        if time[irrad].startswith(today):
            potencial_generated = (irrads[irrad] * pannel_area * efic) / 1000
            hours.append(time[irrad][-5:])
            values.append(potencial_generated)



    return {
        "horas": hours,
        "valores": values,
        "today_api": today_api
    }

if __name__ == "__main__":
    app.run(debug=True)