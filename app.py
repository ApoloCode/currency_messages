import os
from twilio.rest import Client
from configuration import TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN, PHONE_NUMBER, API_KEY_CURRENCY
import time

from requests import Request, Session
from requests.exceptions import ConnectionError, Timeout, TooManyRedirects
import json

import pandas as pd
import requests
from tqdm import tqdm

from datetime import datetime

# Funcion para hacer el request de las divisas
def request_currency(api_key,lista_currency,target):
    resultado = {}
    for currency in lista_currency:
        url_currency = "https://exchange-rates.abstractapi.com/v1/live/?api_key="+api_key+"&base="+currency+"&target="+target
        try :
            response = requests.get(url_currency).json()
        except Exception as e:
            print(e)
        resultado[currency] = round(float(response['exchange_rates']['MXN']), 2)
        time.sleep(1)
    return resultado

# Función para mandar el mensaje
def send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN,data):
    account_sid = TWILIO_ACCOUNT_SID
    auth_token = TWILIO_AUTH_TOKEN
    client = Client(account_sid, auth_token)

    monedas = ""
    for x in data.keys():
        monedas = monedas + "-" + x + ": $" + "{:,.2f}".format(data[x], 2) + '\n\n'
    monedas

    message = client.messages.create(
        from_='whatsapp:+14155238886',
        body='Los tipos de cambio para el dia de hoy a pesos mexicanos (MXN) son los siguientes: \n\n'+monedas+'Que tengas un buen dia!',
        to='whatsapp:+5215536475137'
    )
    
    return message.sid

# Función principal del programa
def main():
    lista_currency = ['USD', 'BTC', 'BCH', 'LTC', 'ETH', 'DOGE']
    api_key = API_KEY_CURRENCY
    target = 'MXN'

    data = request_currency(api_key, lista_currency, target)

    # Send Message
    message_id = send_message(TWILIO_ACCOUNT_SID,TWILIO_AUTH_TOKEN, data)


    print('Mensaje Enviado con exito ' + message_id)

if __name__ == "__main__":
    main()