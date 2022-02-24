import os
import pandas as pd
import pyodbc
from dateutil import parser
from datetime import date

pasta_principal = './csv-data'

for diretorio, subpastas, arquivos in os.walk(pasta_principal):
    for arquivo in sorted(arquivos):        
        
        data = pd.read_csv (os.path.join(diretorio, arquivo), sep=";", encoding='Latin-1')   
        df = pd.DataFrame(data)
        
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=localhost\MSSQLSERVER01;'
                            'Database=desafio_final;'
                            'Trusted_Connection=yes;')


        cursor = conn.cursor()        
        
        for row in df.itertuples():
            tipo_arquivo = arquivo.split('-')[0]
            
            if tipo_arquivo == 'clients':
                print("Inserindo Cliente " + str(row[1]))
                cursor.execute(
                            '''
                                INSERT INTO tb_clients (id, nome, email, data_cadastro, telefone)
                                VALUES (?,?,?,?,?)
                            ''',
                            row[1],
                            row[2],
                            row[3],
                            parser.parse(row[4]), 
                            row[5] 
                            )
            elif tipo_arquivo == 'transaction':                
                print("Verificando se o cliente", str(row[2]), " existe")
                cursor.execute(
                    '''
                        SELECT * FROM tb_clients where id = (?)
                    ''',
                    row[2])
        
                records = cursor.fetchall()

                
                if len(records) > 0:
                    print("Inserindo Transação " + str(row[1]))     
                    cursor.execute(
                                '''
                                    INSERT INTO tb_transaction (id, client_id, valor, data)
                                    VALUES (?,?,?,?)
                                ''',
                                row[1],
                                row[2],
                                row[3],
                                parser.parse(row[4])                             
                                )
            conn.commit()
