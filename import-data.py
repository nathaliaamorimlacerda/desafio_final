import os
import pandas as pd
import pyodbc
from dateutil import parser

# Definindo o diretório proncipal aonde contem todos os arquivos csv
pastaPrincipal = './csv-data'

# Varrendo o diretório principal para começar a leitura de todos os aquivos existentes
for diretorio, subpastas, arquivos in os.walk(pastaPrincipal):
    for arquivo in arquivos:        
        # lendo o arquivo csv e atribuindo o conteudo na variavel data
        # no primeito parâmetro do método "read_csv()"" informamos o arquivo 
        # que aqui será definido em "os.path.join(diretorio, arquivo)"
        # e no segundo qual o separador utilizado
        data = pd.read_csv (os.path.join(diretorio, arquivo), sep=";")   

        # Atribuindo o conteudo a um dataFrame
        df = pd.DataFrame(data)
        
        # Abrindo conexão com o banco de dados
        conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
                            'Server=localhost\MSSQLSERVER01;'
                            'Database=desafio_final;'
                            'Trusted_Connection=yes;')

        cursor = conn.cursor()

        # A cada iteração do laço for o conteudo de uma linha é atribuido a variável row. 
        # desta forma conseguimos acessar o valor de cada coluna atraves do nome ou posição
        # da coluna. Ex: row.id ou row[0]
        for row in df.itertuples():               
            # Recuperando o nome do aquivo que esta sendo trabalho e quebrando pelo "-".
            # desta forma conseguimos identificar se o arquivo é de cliente ou transação
            tipoArquivo = arquivo.split('-')[0]
            
            if tipoArquivo == 'clients':
                print("Inserindo Cliente " + str(row[1]))
                cursor.execute(
                            '''
                                INSERT INTO tb_clients (id, nome, email, data_cadastro, telefone)
                                VALUES (?,?,?,?,?)
                            ''',
                            row[1],# Coluna ID, 
                            row[2],# Coluna nome,
                            row[3],# Coluna Email
                            parser.parse(row[4]), # Coluna data de cadastro
                            row[5] # Coluna Telefone 
                            )
            elif tipoArquivo == 'transaction':
                print("Inserindo Transação " + str(row[1]))
                cursor.execute(
                            '''
                                INSERT INTO tb_transaction (id, client_id, valor, data)
                                VALUES (?,?,?,?)
                            ''',
                            row[1],# Coluna ID, 
                            row[2],# Coluna Client Id,
                            row[3],# Coluna Valor
                            parser.parse(row[4]) # Coluna data                            
                            )
            conn.commit()