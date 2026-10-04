import logging
import azure.functions as func
import os
import pandas as pd
import pyodbc


# ==========================================================
# VARIAVEIS DE AMBIENTE
# ==========================================================

DB_SERVER = os.getenv("HOST")
DB_DATABASE = os.getenv("DATABASE")
DB_USER = os.getenv("USER")
DB_PASSWORD = os.getenv("PASSWORD")

app = func.FunctionApp()

@app.timer_trigger(schedule="*/1 * * * *", arg_name="myTimer", run_on_startup=False,
              use_monitor=False) 
def timer_trigger(myTimer: func.TimerRequest) -> None:
    
    conn = pyodbc.connect(
        f"DRIVER={{ODBC Driver 18 for SQL Server}};"
        f"SERVER={DB_SERVER};"
        f"DATABASE={DB_DATABASE};"
        f"UID={DB_USER};"
        f"PWD={DB_PASSWORD};"
        "Encrypt=yes;"
        "Connection Timeout=30;"
    )
    
    categorias ="""
    SELECT *
    FROM [db-univille].itsm.categoria 
    """
    
    categorias_selecionada=pd.read_sql(categorias,conn)

    logging.info(f"\n--- TABELA CATEGORIAS ---\n{categorias_selecionada.to_string()}\n------------------------")
    
    #print(categorias_selecionada) descartado no terminal do Azure, pois nao e possivel visualizar o print no terminal do Azure
    conn.close()
    if myTimer.past_due:
        logging.info('The timer is past due!')
    logging.info('Python timer trigger function executed.')