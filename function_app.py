import logging

import os

import requests

import azure.functions as func

app = func.FunctionApp()

# Setando configurações para a execução da trigger

# Esse app... é um decorator, serve para dizer ao Azure Functions
# que o que vem a seguir é uma função
# com gatilho de tempo nesse caso.

@app.timer_trigger(
    schedule="0 */5 * * * *", # setando para executar a cada 5 minutos
    arg_name="myTimer2",
    run_on_startup=False,
    use_monitor=False
)

# Criando função que será executada a cada 5 minutos, chamando a função HttpTrigger

def TimerCallHttp(myTimer2: func.TimerRequest) -> None:

    logging.info("Timer Trigger executado!")

    url = os.environ.get("HTTP_FUNCTION_URL")

    # URL da função HttpTrigger que será chamada pelo TimerTrigger

    # Configurado para lidar com testes locais e uso da Azure

    parametro = "VaiCorinthians"

    try:

        response = requests.get(
            url,
            params={"nome": parametro} # Passando o parâmetro 'nome' para a função HttpTrigger
        )

        logging.info(
            f"Resposta da HTTP Function: {response.text}" # Log de resposta da função HttpTrigger
        )

    except Exception as e:

        logging.error(
            f"Erro ao chamar a HTTP Function: {e}"

            # Log resumido de erro
        )


# ============================================================
# HTTP TRIGGER
# ============================================================

import logging

import azure.functions as func

@app.route(
    route="HttpTrigger",
    auth_level=func.AuthLevel.ANONYMOUS
)

def HttpTrigger(req: func.HttpRequest) -> func.HttpResponse:

    logging.info("Python HTTP trigger recebeu um request.")

    nome = req.params.get("nome") # Usamos método get para receber o parâmetro nome, caso seja executado pela time trigger vai receber "VaiCorinthians" e caso seja executado pelo navegador vai receber o parâmetro que for passado na URL, exemplo: ?nome=TurmaC

    if nome:

        # Log caso o parâmetro seja recebido, seja pelo navegador ou pela time trigger

        logging.info(f"Parametro recebido: {nome}")

        # Resposta engraçada porque tô com homem de ferro na cabeça

        texto_resposta = f"Jarvis, parametro recebido: {nome}! Sucesso de 100%"

        # Retornando a resposta para o navegador ou para a time trigger

        return func.HttpResponse(texto_resposta)

    # Return caso dê tudo errado

    return func.HttpResponse(
        "Jarvis temos um problema, nenhum parametro recebido. Por favor passe o parametro pela URL",

        status_code=400 # HTTP para erro
    )