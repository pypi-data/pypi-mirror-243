<!-- coding: utf-8 -->
# RPA HyperCoe Log: 

## Kit de componentes para o registrar os Logs dos robôs com a plataforma HyperCoe.

### Intalação
    >>> pip install rpa-hypercoe-log

### Como usar a biblioteca:
    >>> from rpa_hypercoe_log import Funcao

###  Exemplo de como usar a função de registro de log
- Funcao.Status(bot_id,clienttoken,bot_status)
- Funcao.Iteration(bot_id,clienttoken) 
- Funcao.Log(level,typeError,message,pathfile,ID_Iteration,finalLog,ClientToken)

###  Descrições gerais das funções
- Funcao.Status - Altera i Status de processamento do bot em questão.
- Funcao.Iteration - Captura o ID da iteração para ser utilizado como parâmetro na função de Log.
- Funcao.Log - Registra o Log de execução do bot.


### Definição dos parâmetros:
- **rpa-hypercoe-log**
    - **bot_status** - Valor inteiro correspondente ao status do bot sendo # Active=0, Running=1, Paused=2, Error=3 (Campo obrigatório)
    - **bot_id** - Valor inteiro referente ao ID do bot que será gerado no momento de criação do robô pelo agente do HyperCoe (Campo obrigatório)
    - **clienttoken** - Valor string do Token que será disponibilizado pelo Portal HyperCoe (Campo obrigatório)
    - **level** - Valor inteiro correspondente ao tipo de informação que será regsitrado no log, sendo # Info=0, Warn=1, Error=2 (Campo obrigatório)
    - **typeError** - Valor string com a mensagem em caso de erro. (Campo não obrigatório)
    - **message** - Valor string com a mensagem de log (Campo obrigatório)
    - **pathfile** - Valor string com o caminho absoluto para envio de evidência (Campo não obrigatório)
    - **ID_Iteration** - Valor inteiro capturado pela api "Iteration" (Campo obrigatório)
    - **finalLog** - Valor boleano (False/True) que deverá ser padrão False e somente utilizar o parametro True no último registro de log do robô (Campo não obrigatório)