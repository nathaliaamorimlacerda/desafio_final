# desafio_final
# Repositório Data Azure - Desafio final

# Descrição do projeto

## Sumário

# 1 - Descrição do projeto
# 2 - Tecnologias usadas
# 3 - Criação do banco de dados
# 4 - Exportação de dados e carregando o banco de dados em Python
# 5 - Relatórios de análise no SQL
# 6 - Relatórios no Power BI
# 7 - Hospedagem na nuvem

## 3 - Criação do banco de dados

# Recebemos uma carga de arquivos em csv contendo 4 tabelas de clientes e 63 de transações. Visando a descoberta de fraudes. Para fazer a importação desses dados no python o primeiro passo foi criar um banco de dados no SQL e duas tabelas relacionadas as informações contidas na carga de arquivos, que não aceitasse valores nulos e com chave primaria em seus IDs e a chave estrangeira no cliente_id referenciado da tabela de clientes, validando a integridade dos dados, e mostrando o vínculo forte entre as tabelas, como podemos ver no script:

# CREATE DATABASE DESAFIO_FINAL;
# GO
# USE DESAFIO_FINAL;
# GO
# CREATE TABLE TB_CLIENTS(
# 	ID INT NOT NULL,
# 	NOME VARCHAR(250) NOT NULL,
# 	EMAIL VARCHAR(250) NOT NULL,
# 	DATA_CADASTRO DATETIME NOT NULL,
# 	TELEFONE VARCHAR(16),
# 	PRIMARY KEY (ID)
# );
# GO

# CREATE TABLE TB_TRANSACTION(
# 	ID INT NOT NULL,
# 	CLIENT_ID INT NOT NULL,
# 	VALOR FLOAT NOT NULL,
# 	DATA DATETIME,
# 	PRIMARY KEY (ID),
# 	FOREIGN KEY (CLIENT_ID) REFERENCES TB_CLIENTS(ID)
# );

## 4 - Exportação de dados e carregando o banco de dados em Python

# Encontrando o caminho das tabelas de clients e transaction:

### pasta_principal  = '.\csv.data’'

# Importamos a biblioteca OS para automatizar alguns processos, a função os.walk() lista o nome dos arquivos clients e transaction e 
# Percorremos o caminho de arquivos com o laço for:

### for diretorio, subpastas, arquivos in os.walk(pastaPrincipal):

# Porém, todas as tabelas de transection e clients estão de forma desordenada, usamos o sorted() listamos e ordenamos todas as tabelas para que, primeiro,
# o doc. clients sejam inseridos antes do doc. transaction:

### for diretorio, subpastas, arquivos in os.walk(pastaPrincipal):
   ### for arquivo in sorted(arquivos):


# Atribuímos o conteúdo dos arquivos a variável data:

  ###  data = pd.read_csv (os.path.join(diretorio, arquivo), sep=";", encoding='UTF-8')  
 

# Utilizamos a biblioteca  pandas para ler o arquivo csv, mostrando o caminho que o programa deve ser executado. 
# O sep=”;” é a forma de separação que o doc. deve ser exibido.
# (Variamos  o método de codificação na nossa máquina, umas usaram ‘UFT-8’ , outras ‘Latin-1’)


# Atribuímos a variável data a um DataFrame para que os arquivos sejam exibidos de forma tabular.
  ### df = pd.DataFrame(data)


# Atribuímos a conexão ao sql server a variável conn e a usamos para fazer a interação com o sql.

### conn = pyodbc.connect('Driver={ODBC Driver 17 for SQL Server};'
   ### 'Server=localhost\MSSQLSERVER01;'
   ### 'Database=desafio_final;'
   ### 'Trusted_Connection=yes;')
 
   ### cursor = conn.cursor()       
 
 
# Fizemos uma interação no dataframe e usamos o itertuples() para acessar os valores das colunas através do nome e posição das linhas.

### for row in df.itertuples():              
  ### tipoArquivo = arquivo.split('-')[0]
      

# A função split() vai quebrar os traços dos arquivos e ler apenas a posição [0],  que seria o nome. 
# Isso identificaria o arquivo que estamos trabalhando. 

# A condição if identifica apenas se o arquivo é igual ao doc. clients,  caso seja, entra nessa condição iniciando da [1] posição que são os ID dos clientes. 
# (Colocamos a [1] posição apenas para ignorar a primeira coluna index[0], que seria a quantidade de clientes.)

### if tipoArquivo == 'clients':
   ### print("Inserindo Cliente " + str(row[1]))
   ### cursor.execute('''
                      
# Após isso, o cursor vai fazer a interação diretamente no banco de dados inserindo as linhas e colunas.

   ### INSERT INTO tb_clients (id, nome, email, data_cadastro, telefone)
   ### VALUES (?,?,?,?,?)
                         ''',
   ### row[1],# Coluna ID,
   ### row[2],# Coluna nome,
   ### row[3],# Coluna Email
   ### parser.parse(row[4]), # Coluna data de cadastro
   ### row[5] # Coluna Telefone
   ### )

# A função parar.parse() transforma uma str de data, para um datetime.

# Nessa próxima condição verificamos se o ID do arquivo clients existe.

### elif tipoArquivo == 'transaction':               
   ### print("Verificando se o cliente", str(row[2]), " existe")
   ### cursor.execute(
      '''
   ### SELECT * FROM tb_clients where id = (?)
      ''',
   ### row[2])
      
# Aqui verificamos se a variável records está vazia, caso esteja é porque o cliente não existe e podemos ignorá-lo.

  ### records = cursor.fetchall()
  ### if len(records) > 0:
   ### print("Inserindo TransaÃ§Ã£o " + str(row[1]))
   
# Executando o comando para inserir as transações
                   
   ### cursor.execute(
    '''
   ### INSERT INTO tb_transaction (id, client_id, valor, data)
   ### VALUES (?,?,?,?)
    ''',
    
   ### row[1],# Coluna ID,
   ### row[2],# Coluna Client Id,
   ### row[3],# Coluna Valor
   ### parser.parse(row[4]) # Coluna data                           
                               )
   ### conn.commit()
          
# Caso o records seja maior que 0,  o cursor vai fazer a interação diretamente no banco de dados inserindo os registros.


## 5 - Relatórios de análise no SQL

# Após a inserção dos valores nas tabelas podemos gerar alguns relatórios através dos selectes, 1° mostrando a quantidade total de clientes, que foram 401:
# select * from tb_clients

# Depois quantas transações foram feitas: 6722
# --(nem todos os clientes fizeram transações pois aparecem valores e data null)
# select C.id, C.nome, T.data, T.valor
# 	from tb_clients C
# left join tb_transaction T on C.id=T.client_id


# A quantidade de clientes que não fizeram transações que foram 341.
# -- clientes sem transações - 341 linhas
# select C.id, C.nome, T.data, T.valor
# 	from tb_clients C
# left join tb_transaction T on C.id=T.client_id
# where T.data is null
# order by C.id


# E por fim quantos clientes fizeram transações (60 clientes) e quantas transações cada cliente fez
# select T.client_id,
# 	count (*) as "número de transações"
# 	from tb_transaction T
# 	group by T.client_id

## 6 - Relatórios no Power BI

# Para realizar o cálculo e descobrir os clientes fraudados, utilizamos o DAX, a biblioteca de funções e operadores do Power BI.

# Criamos três colunas: segundo, categoria e transação.
# A coluna segundo é baseada na análise do cálculo do espaçamento de tempo entre as transações de cada cliente:

# SEGUNDO =
# VAR TEMP =
# TOPN (1, FILTER ('TB_TRANSACTION', 'TB_TRANSACTION'[CLIENT_ID] = EARLIER ( 'TB_TRANSACTION'[CLIENT_ID] ) && 'TB_TRANSACTION'[DATA] < EARLIER ( 'TB_TRANSACTION'[DATA] )),
# [DATA], DESC) RETURN DATEDIFF ( MINX ( TEMP, [DATA] ), [DATA], SECOND )


# A coluna segundo recebe a variável temp, que por sua vez possui uma *expressão onde é feito o cálculo que nos retorna a diferença de tempo entre as transações, agrupando os # dados por cliente e data e comparando se os dois tempos verificados são do mesmo cliente.


# A próxima coluna criada foi categoria, que verifica se a coluna segundo é menor que 120 segundos, se sim, retorna 0, em caso negativo, retorna 1.

# CATEGORIA = IF(TB_TRANSACTION[SEGUNDO] >= 1 && TB_TRANSACTION[SEGUNDO] < 120, 1, 0 

# A última coluna criada foi transação, para melhor visualização do resultado no reslatório, a mesma verifica a coluna categoria e retorna 1 em caso de fraude e 0, caso negativo.

# TRANSAÇÃO = IF(TB_TRANSACTION[CATEGORIA] = 0 , "Normal","Fraude")

# 7 - Hospedagem na nuvem

# Instalações realizadas na VM pelo Azure CLI:
### sudo apt install 
### - mysql-client-core-8.0
### - mysqlserver
### - update
### - pandas
### - pyodbc
### -unzip

# documentação lida para criar um database na VM pelo CLI:

### https://azure.microsoft.com/pt-br/blog/create-your-own-dedicated-mysql-server-for-your-azure-websites/

# entretanto não conseguimos ainda reparar o erro de acesso ao servidor, desta forma, utilizamos a implantação dos dados pelo SQL client no Desktop.
