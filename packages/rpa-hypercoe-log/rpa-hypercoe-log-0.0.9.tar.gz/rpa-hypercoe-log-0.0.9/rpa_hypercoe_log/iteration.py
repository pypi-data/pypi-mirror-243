################ IMPORTS ################
import requests
import os
import json
import base64
from datetime import datetime
##########################################
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