"""Consulta o clima e envia um estado à matriz do Arduino UNO Q."""

import json
import time
import urllib.parse
import urllib.request

from arduino.app_utils import App, Bridge

# Coordenadas de Rio Branco, Acre, Brasil.
LATITUDE = -9.9754
LONGITUDE = -67.8249
CONSULTA_A_CADA_SEGUNDOS = 10 * 60
URL_BASE = "https://api.open-meteo.com/v1/forecast"

# Códigos WMO de céu limpo, principalmente limpo e parcialmente nublado.
CODIGOS_TEMPO_BOM = {0, 1, 2}


def consultar_clima():
    parametros = urllib.parse.urlencode(
        {
            "latitude": LATITUDE,
            "longitude": LONGITUDE,
            "current": "weather_code,temperature_2m",
            "timezone": "auto",
        }
    )
    url = f"{URL_BASE}?{parametros}"
    requisicao = urllib.request.Request(
        url,
        headers={"User-Agent": "OpenSenseLab-weather-matrix/1.0"},
    )
    with urllib.request.urlopen(requisicao, timeout=15) as resposta:
        dados = json.loads(resposta.read().decode("utf-8"))

    atual = dados["current"]
    codigo = int(atual["weather_code"])
    temperatura = float(atual["temperature_2m"])
    return codigo, temperatura


def atualizar_clima():
    try:
        codigo, temperatura = consultar_clima()
        estado = 0 if codigo in CODIGOS_TEMPO_BOM else 1
        Bridge.call("set_weather_state", estado, timeout=5)
        descricao = "bom" if estado == 0 else "ruim/instável"
        print(
            f"Clima: {descricao}; código WMO {codigo}; "
            f"temperatura {temperatura:.1f} °C"
        )
    except Exception as erro:
        print(f"Falha ao consultar/enviar o clima: {erro}")
        try:
            Bridge.call("set_weather_state", 2, timeout=5)
        except Exception as erro_bridge:
            print(f"Falha de comunicação com o sketch: {erro_bridge}")


def loop():
    atualizar_clima()
    time.sleep(CONSULTA_A_CADA_SEGUNDOS)


App.run(user_loop=loop)
