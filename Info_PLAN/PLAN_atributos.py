# import dos modulos
import pandas as pd
import numpy as np
from datetime import datetime
import pyodbc
import os

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

# Nova Coluna  concatenando o data_type|attr_nm
md_planning_info_custom_prop['attr_nm'] = md_planning_info_custom_prop['attr_nm'].replace({'Tipo SGTO':'SGTO_VLR','Oferta Easy':'OFERTA_EASY','Flg Funcionario':'FL_FUNCIONARIO','Plan':'ID_SIST_PGTO','Tipo Fibra':'PSSE_FIBRA'})
md_planning_info_custom_prop['data_type'] = md_planning_info_custom_prop['data_type'].replace({'TEXT':'STRING','INTERGER':'NUMBER'})
md_planning_info_custom_prop['COLUMN_OFFER'] = md_planning_info_custom_prop['data_type'] + '|' + md_planning_info_custom_prop['attr_nm']

# subset pegando as colunas do PLANNING_INFO.csv
subset_planning_info = md_planning_info[[
    'planning_id', 'planning_number', 'planned_start_dttm', 'planned_end_dttm', 'planning_status']]

# subset pegando as colunas do PLANNING_INFO_CUSTOM_PROP.csv
subset_custom_prop = md_planning_info_custom_prop[[
    'planning_id', 'COLUMN_OFFER', 'attr_id', 'attr_val']]

# subset pegando as colunas do MD_PICKLIST.csv
subset_picklist = md_picklist[['attr_id', 'plist_val', 'plist_cd']]

# Fazendo o join entre as tabelas PLANNING_INFO.csv e INFO_CUSTOM_PROP.csv
plan_atributos = pd.merge(subset_planning_info,
                          subset_custom_prop, on='planning_id')

# Fazendo o join no resultado plan_atributos e MD_PICKLIST.csv
plan_atributos = pd.merge(plan_atributos, subset_picklist, on='attr_id')

# checando o planning_id e attr_id
plan_atributos['CHV_COMPOSTA'] = plan_atributos['planning_id'] + \
    '|' + plan_atributos['attr_id']

# Renomeando as colunas
plan_atributos = plan_atributos.rename(columns={
    'planning_number': 'CHV_OFERTA',
    'planned_start_dttm': 'DT_INIC_VIGENCIA',
    'planned_end_dttm': 'DT_FIM_VIGENCIA',
    'planning_status': 'STATUS'
})

# Compara se o valor do attr_val esta na plist_cd
def valor_attr(row):
    if str(row['plist_cd']) in str(row['attr_val']):
        return row['plist_val']
    return None
      


plan_atributos['VALUE_OFFER'] = plan_atributos.apply(lambda row: valor_attr(
    row), axis=1)  # passem a função e a apliquem em cada valor da série
plan_atributos = plan_atributos.dropna()  # retira os valores nulls

novo_plan_atributos = plan_atributos.groupby(
    'CHV_COMPOSTA')['VALUE_OFFER'].apply('; '.join).reset_index()
plan_atributos = plan_atributos[['CHV_COMPOSTA', 'CHV_OFERTA', 'COLUMN_OFFER',
                                 'DT_INIC_VIGENCIA', 'DT_FIM_VIGENCIA', 'STATUS']].drop_duplicates()

plan_atributos = plan_atributos.merge(novo_plan_atributos, on='CHV_COMPOSTA')

planos = plan_atributos[['CHV_OFERTA', 'COLUMN_OFFER',
                         'VALUE_OFFER', 'DT_INIC_VIGENCIA', 'DT_FIM_VIGENCIA']]

plan_atributos_filtrado = plan_atributos.query('STATUS == "APPROVED"')
resultado = plan_atributos_filtrado[[
    'CHV_OFERTA', 'COLUMN_OFFER', 'VALUE_OFFER', 'DT_INIC_VIGENCIA', 'DT_FIM_VIGENCIA']]

print(f'Arquivo Gerado Com sucesso: Total de Planos {planos.shape}')
print(f'Arquivo Gerado Com sucesso: Total de Planos Aprovados {resultado.shape}' )

now = datetime.today().strftime('%Y-%m-%d %H.%M.%S%Z')
planos.to_excel(f'{PATH_BASE_info_PLAN}\Files\planos.xlsx', index=False)
resultado.to_excel(f'{PATH_BASE_info_PLAN}\Files\planos_approved.xlsx', index=False)

#LEITURA DA PLANILHA
todos_dados = pd.read_excel(f'{PATH_BASE_info_PLAN}\Files\planos_approved.xlsx')


#CONEXAO COM O BANCO DE DADOS

""" conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SAS-AAP.demo.sas.com;'
                      'Database=CIDB;'
                      'Trusted_Connection=yes;')


cursor = conn.cursor()
#cursor.execute('SELECT TOP 1000 CHV_OFERTA ,COLUMN_OFFER   ,VALUE_OFFER   ,DT_INIC_VIGENCIA   ,DT_FIM_VIGENCIA  FROM CDM.CRM_TB_ATTR_MOTOR')

#APAGAR REGISTROS NA TABELA
cursor.execute('TRUNCATE TABLE CDM.CRM_TB_ATTR_MOTOR')
cursor.commit()

#PERCORRENDO LINHA A LINHA DA TABELA E INSERINDO NO BANCO DE DADOS
for indice, cada_linha in todos_dados.iterrows():
    cursor.execute("insert into CDM.CRM_TB_ATTR_MOTOR (CHV_OFERTA ,COLUMN_OFFER   ,VALUE_OFFER   ,DT_INIC_VIGENCIA   ,DT_FIM_VIGENCIA) values (?,?,?,?,?) ",cada_linha.CHV_OFERTA,cada_linha.COLUMN_OFFER,cada_linha.VALUE_OFFER,cada_linha.DT_INIC_VIGENCIA,cada_linha.DT_FIM_VIGENCIA, )

conn.commit()
cursor.close() 
 """