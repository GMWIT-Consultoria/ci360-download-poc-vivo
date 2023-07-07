import pandas as pd
import psycopg2
import os

# Import execute_values from psycopg2.extras
from psycopg2.extras import execute_values

#import pyodbc
# Caminho dos arquivos csv 

PATH_BASE_info_PLAN = os.path.dirname(os.path.realpath(__file__))
PATH_FILES = '.\dscwh'


md_picklist = pd.read_csv(PATH_FILES +'\MD_PICKLIST.csv',
                          delimiter='^')  # MD_PICKLIST.csv
md_planning_info_custom_prop = pd.read_csv(
    PATH_FILES + '\PLANNING_INFO_CUSTOM_PROP.csv', delimiter='^')  # PLANNING_INFO_CUSTOM_PROP.csv
md_planning_info = pd.read_csv(
    PATH_FILES + '\PLANNING_INFO.csv', delimiter='^')  # PLANNING_INFO.csv


#LEITURA DA PLANILHA
todos_dados = pd.read_excel(f'{PATH_BASE_info_PLAN}\Files\clientes_vivo360.xlsx', engine='openpyxl')


#CONEXAO COM O BANCO DE DADOS

# Establish connection to the PostgreSQL server
connection = psycopg2.connect(
    host="10.96.12.46",
    port="11432",
    database="cidb",
    user="sas",
    password="Orion123"
)

# Create a cursor object to interact with the database
cursor = connection.cursor()

# # If the table doesn't exist, create it
# cursor.execute("CREATE TABLE CLIENTES_VIVO360 (id_cliente TEXT, produto TEXT, sgto TEXT)")
# connection.commit()
# print("Table CI360_INFO created.")

# If the table exists, drop its content
cursor.execute("TRUNCATE TABLE CLIENTES_VIVO360")
connection.commit()
print("Content of table CLIENTES_VIVO360 dropped.")

# Save todos_dados to CLIENTES_VIVO360 table
if not todos_dados.empty:
    records = todos_dados.to_records(index=False)
    columns = ', '.join(todos_dados.columns)
    insert_query = f"INSERT INTO CLIENTES_VIVO360 ({columns}) VALUES %s"

    execute_values(cursor, insert_query, records)
    connection.commit()
    print("Data saved to CLIENTES_VIVO360 table.")

# Close the cursor and the database connection
cursor.close()
connection.close()
print("Banco gerado com sucesso")