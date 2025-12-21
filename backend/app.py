from flask import Flask, jsonify, request
import requests
from flask_cors import CORS
from datetime import date
import random
import psycopg2
from psycopg2.extras import RealDictCursor
from psycopg2.extras import DictCursor
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = psycopg2.connect(
        host=os.getenv("DB_HOST"),
        port=os.getenv("DB_PORT"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD")
    )
    return conn

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
            potencial_generated = ((irrads[irrad] * pannel_area * efic) / 1000)*30000
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
def consumption_energ():
    TOTAL_HOUSES = 2000

    hours = [f"{h:02d}:00" for h in range(24)]
    consumption_for_day = []

    for hour in range(24):

        if 0 <= hour < 5:
            base = random.uniform(0, 0.8)

        elif 5 <= hour < 12:
            base = random.uniform(3, 4.5)

        elif 12 <= hour < 18:
            base = random.uniform(3, 4.5)

        else:  # 18–23
            base = random.uniform(2, 3.9)

        consumption_for_day.append(
            round(base * TOTAL_HOUSES, 2)
        )

    return {
        "horas": hours,
        "valores": consumption_for_day
    }
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

#===========================================================================================================================

@app.route("/report_production_menu", methods=["POST"])
def report_prod_and_cons_menu():

    if request.method == 'POST':
        data_report = request.get_json()
        report_data = data_report.get("btn_report")


        production = production_potential()
        consumption = consumption_energ()
        total_production = round(sum(production["valores"]), 2)

#---------------------------------------------------------------------------------------------------------------------------
        if report_data == "SECTORS_PRODUCTION":

            sectors = ["ALFA", "BRAVO", "CHARLIE", "DELTA", "ECHO"]

            percentages = []
            remaining = 1.0

            for i in range(len(sectors) - 1):
                value = round(random.uniform(0.10, 0.25), 2)
                percentages.append(value)
                remaining -= value

            percentages.append(round(max(remaining, 0), 2))

            labels = []
            values = []

            for sector, percent in zip(sectors, percentages):
                labels.append(sector)
                values.append(round(total_production * percent, 2))

            return {
                "labels": labels,
                "values": values,
                "total_production": total_production
            }
                                                        #Acima a condicional da função relatórios. A condicional faz com que o sistema: verifique o json retornado do front end, se for relatórios de produção por setores ele deverá simular a produção com base na radiação solar retornado da api climatica, escolhendo as porcentagens em que cada setor contribui para produção, deve colocar os valores em uma lista e retornar esses dados em forma de JSON para o front criar dados
#---------------------------------------------------------------------------------------------------------------------------       
        elif report_data == "PANNELS":

            total_pannels = 22000

            production_energ_for_pannel = round(total_production / total_pannels,4)

            labels = [f"Painel {i+1}"for i in range(total_pannels)]
            values = [production_energ_for_pannel for _ in range(total_pannels)]

            return {"labels": labels[:50],
                            "values": values[:50],
                            "total_production": total_production,
                            "production_energ_for_pannel": production_energ_for_pannel}
        
                                                    #Acima a condicional da função relatórios. A condicional faz com que o sistema: verifique o json retornado do front end, se for relatórios de produção por paineis dos setores ele deverá simular a produção com base na radiação solar retornado da api climatica, em que cada painel do setor produz de modo uniforme isso por que as condições para todos os paineis é a mesma. Ele deve colocar os valores em uma lista e retornar esses dados em forma de JSON para o front criar dados
        
#---------------------------------------------------------------------------------------------------------------------------

        elif report_data == "SECTORS_CONSUMPTION":

            consumption = consumption_energ()
            total_consumption = round(sum(consumption["valores"]), 2)
            
            sectors = ["ALFA", "BRAVO", "CHARLIE", "DELTA", "ECHO"]

            percentages = []
            remaining = 1.0

            for i in range(len(sectors) - 1):
                value = round(random.uniform(0.10, 0.25), 2)
                percentages.append(value)
                remaining -= value

            percentages.append(round(max(remaining, 0), 2))

            labels = []
            values = []

            for sector, percent in zip(sectors, percentages):
                labels.append(sector)
                values.append(round(total_consumption * percent, 2))

            return {
                "labels": labels,
                "values": values,
                "total_consumption": total_consumption
            }
        
                                            #Acima a condicional da função relatórios. A condicional faz com que o sistema: verifique o json retornado do front end, se for relatórios de consumo por setores ele deverá simular o consumo com base na função de consumo consumption_energ(). Ele deve colocar os valores em uma lista e retornar esses dados em forma de JSON para o front criar dados.
        
#---------------------------------------------------------------------------------------------------------------------------

        elif report_data == "INDIVIDUAL":
            data_report.get("SECTOR_IND")
            conn = get_db_connection()
            cursor = conn.cursor()
            sector_cons_ind = data_report.get("SECTOR_IND")

            sector_labels = []
            sector_values = []

            if sector_cons_ind:
                cursor.execute('''SELECT * FROM resident WHERE sector_resident ILIKE %s''', (f"%{sector_cons_ind}%",))
                sector_result = cursor.fetchall()
            
            for row in sector_result:
                sector_labels.append(row[0])         
                sector_values.append(row[4])
                
            cursor.close()
            conn.close()

            return {
                "sector": sector_labels,
                "value_invoice": sector_values
            }


@app.route("/panels_info", methods = ["POST"])
def panels_info():
    data_infor_panel = request.get_json()

    infor_panel = data_infor_panel.get("reference_sector")
    index_pannel = data_infor_panel.get("dt_index_ref")

    print(infor_panel)
    print(index_pannel)

    data_report_detail_panel = production_potential()

    total_production_sector = sum(data_report_detail_panel["valores"])

    contribuition_panel = sum(data_report_detail_panel["valores"])/30000

    percent_panel = (contribuition_panel / total_production_sector) * 100

    return {"setor": infor_panel,
            "painel": index_pannel,
            "percent_panel":percent_panel,
            }


@app.get("/shipping_unic")
def shipping_unic_invoice():
    request.json()



if __name__ == "__main__":
    app.run(debug=True)