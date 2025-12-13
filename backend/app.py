from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from datetime import date
import random


app = Flask(__name__)
CORS(app)


@app.get("/clima")
def clima():

    url = (
      "https://api.open-meteo.com/v1/forecast?latitude=,-22.688504781081985&longitude=,-43.352751556386316&hourly=temperature_2m,direct_radiation&timezone=America%2FSao_Paulo"
    )

    resposta = requests.get(url).json()

    return resposta

#===========================================================================================================================

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
#b1

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
#b2

                                                        #Acima temos a função de produção de energia. De modo detalhado funciona da seguinte forma: do bloco 1 (#b1) acima temos a requisição da função clima que tem a chave API necessária para o funcionamento do sistema, colocada em uma variavel assim e sendo tratada para pegar dados especificos como a hora, e a direção da radiação solar, a variavel today serve como parametro para garantir que o sistema pegue somente o dia atual. O bloco 2 temos um loop for calculando a produção estimada com os parametros de area do painel, a hora do dia para saber a radiação e a potencia gerada e tudo isso é retornado ao front-end em forma de JSON.
#===========================================================================================================================

@app.get("/consumption_daily")
def build_hours():
    return [f"{h:02d}:00" for h in range(24)]

def consumption_energ():


    consumption_for_day = []
    hours =  hours = build_hours()



    
    for hour in range(24):

        if 0 <= hour < 5:
            consumption_for_day.append(round(random.uniform(0,0.8),2))
            #dawn_consumption = 0 - 0.8

        elif 5 <= hour < 12:
            consumption_for_day.append(round(random.uniform(3, 4.5),2))
            #morning_consumption =

        elif 12 <= hour < 18:
            consumption_for_day.append(round(random.uniform(3, 4.5),2))
            #afternoon_consumption =  3.0 - 4.5

        elif 18 <= hour < 24:
            consumption_for_day.append(round(random.uniform(2, 3.9),2))
            #nigth_consumption = 2 - 3.9


    return{"horas":hours ,"valores":consumption_for_day}

                                                                    #Acima temos um loop for, que estabelece um range entre 0 a 24, isso para as horas, e a cada hora é gerado uma estimativa de consumo de energia que pode crescer ou diminuir a depender da hora do dia. Os dados são retornados ao JSON.

#===========================================================================================================================

@app.get("/consumption_vs_production")
def consumption_vs_production():
    
    consumo = consumption_energ()
    producao = production_potential()

    return{
            "horas": consumo["horas"],   # fonte única de labels
            "consumo": consumo["valores"],
            "producao": producao["valores"]
    }


if __name__ == "__main__":
    app.run(debug=True)