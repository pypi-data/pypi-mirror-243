################ IMPORTS ################
import requests
import os
import json
import base64
from datetime import datetime
##########################################
def Status (BOT_Status,ClientToken,BOT_ID):
    try:
        UrlAPIStatus = 'https://hypercoe-api-hml.triasoftware.com.br/api/bot/change-status-by-bot'

        # ID - Active=0, Running=1, Paused=2, Error=3
        dados = {'id': BOT_ID, 'status': BOT_Status}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIStatus, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Status do Bot Alterado com sucesso")
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Status: ", erro)
    return erro