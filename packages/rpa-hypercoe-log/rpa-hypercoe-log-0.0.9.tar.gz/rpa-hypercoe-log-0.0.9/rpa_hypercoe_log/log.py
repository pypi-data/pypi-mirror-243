################ IMPORTS ################
import requests
import os
import json
import base64
from datetime import datetime
##########################################
def Log (level,typeError,message,pathfile,ID_Iteration,finalLog,ClientToken):
    try:
        UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
        dataatual = datetime.now()
        date = dataatual.strftime("%Y-%m-%dT%H:%M:%S")

        #Converter arquivo em Base64 caso tenha dados na variavel
        if len(pathfile) > 4:
            try:
                with open(pathfile, 'rb') as file:
                    arquivo_bytes = file.read()
                # Converter o arquivo para base64
                arquivo_base64 = base64.b64encode(arquivo_bytes).decode('utf-8')
                fileBase64 = arquivo_base64
            except Exception as erro:
                print(f"Erro na tentativa de converter o arquivo em Base64: ", erro)
                fileBase64 = ""
        else:
            fileBase64 = ""

        # Level - info=0, warn=1, error=2
        dados = {'date': date, 'level': level, 'typeError': typeError, 'message': message, 'fileBase64': fileBase64 ,'iterationId': ID_Iteration, 'finalLog':finalLog}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPILog, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            print("Log registrado com sucesso:", message)
        else:
            print("Erro na requisição. Status code:", response.status_code)

    except Exception as erro:
        print(f"Erro API Log: ", erro)
        return erro