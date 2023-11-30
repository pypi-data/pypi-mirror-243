
#OPERACOES SAP
USER_SAP = 'rpa_adm'
PASSWORD_SAP = 'tk08#adm'

#EMAIL
#DESTINATARIOS_EMAIL = "thiago.carmo@tekno.com.br; gabriel.pereira@tekno.com.br"
# "guivaresbgn@gmail.com; thiago.carmo@tekno.com.br; gabriel.pereira@tekno.com.br"
DESTINATARIOS_EMAIL = "joao.buso@triasoftware.com.br"

# LINK DE ACESSO
dev = r"http://tgcsda01.tekno.corp:8010/sap/opu/odata/sap/"
qas = r"http://tgcsqa01.tekno.corp:8000/sap/opu/odata/sap/"
prd = r"http://tgcspa01.tekno.corp:8000/sap/opu/odata/sap/"
       
url = prd
ambiente = 'PRD'
endpoint = "ZTEKSD_RPA_BC_SRV/ZTEKSD_RPA_INSERT_VALUESet"

#CAMINHO_PRINT
#Obtenha o diretório atual do arquivo .py
import os
DIRETORIOATUAL = os.path.dirname(os.path.abspath(__file__))
#Obtenha o diretório pai
DIRETORIOAPAI = os.path.dirname(DIRETORIOATUAL)
CAMINHO_ARQUIVO = f"{DIRETORIOAPAI} \Prints\print.png"
CAMINHOS_ANEXOS_SUCESSO = [CAMINHO_ARQUIVO]

#TOKEN API HYPERCOE
ClientToken = 'OTJiZTNiMGEtNjNiYy00YmNmLWFhZWUtMzhjZWRiMTY0OGU0LkhZUEVSX0NPRV9UT0tFTg=='

#URL API HYPERCOE
UrlAPIStatus = 'https://hypercoe-api-hml.triasoftware.com.br/api/bot/change-status-by-bot'
UrlAPILog = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-log-by-bot'
UrlAPIExecution = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-execution-by-bot'
UrlAPIIteracao = 'https://hypercoe-api-hml.triasoftware.com.br/api/execution/add-iteration-by-bot'