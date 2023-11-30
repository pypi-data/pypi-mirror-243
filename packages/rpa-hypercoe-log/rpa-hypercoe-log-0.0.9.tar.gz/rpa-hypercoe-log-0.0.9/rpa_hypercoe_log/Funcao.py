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

def Iteration (ClientToken,BOT_ID):
    try:
        UrlAPIExecution = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-execution-by-bot'
        UrlAPIIteracao = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-iteration-by-bot'
        
        # ID - Active=0, Running=1, Paused=2, Error=3
        dados = {'botId': BOT_ID}

        # Headers da requisição (caso necessário)
        headers = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        response = requests.post(UrlAPIExecution, json=dados, headers=headers)

        # Verifique o status da resposta
        if response.status_code == 200:  # 200 indica sucesso
            result = response.json()
            ExecutionID = result['dados']['id']
        else:
            print("Erro na requisição. Execution code:", response.status_code)

        # Dados que você quer enviar no corpo da requisição (em formato JSON, por exemplo)
        dadosIteracao = {'executionId': ExecutionID}
        
        # Headers da requisição (caso necessário)
        headersIteracao = {'Content-Type': 'application/json', 'ClientToken': ClientToken}

        # Realize a requisição
        responseIteracao = requests.post(UrlAPIIteracao, json=dadosIteracao, headers=headersIteracao)

        # Verifique o status da resposta
        if responseIteracao.status_code == 200:  # 200 indica sucesso
            resultIteracao = responseIteracao.json()
            IteracaoID = resultIteracao['dados']['id']
            print("Iteration ID:", IteracaoID)  # Retorna os dados da resposta em formato JSON
            return IteracaoID
        else:
            print("Erro na requisição. Iteration code:", responseIteracao.status_code)
                
    except Exception as erro:
            print(f"Erro API Execution: ", erro)
            return erro