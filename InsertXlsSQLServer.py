import pandas as pd
import pyodbc

# Caminho para a planilha Excel
file_path = r'C:\Users\SuaMaquina\Desktop\PastaOrigemScript\teste.xlsx'

# Lê o arquivo Excel
df = pd.read_excel(file_path)

# Conexão com o banco de dados
conn = pyodbc.connect('Driver={SQL Server};'
                      'Server=SuaMaquina\\InstaciaSQL;'
                      'Database=NomeBaseDeDados;'
                      'Trusted_Connection=yes;')

# Cria um cursor
cursor = conn.cursor()

# Trunca a tabela dimEndereco antes de inserir novos dados
try:
    cursor.execute("TRUNCATE TABLE [dimEndereco]")
    print("Tabela dimEndereco truncada com sucesso.")
except Exception as e:
    print(f"Erro ao truncar a tabela: {e}")

# Verificação se o DataFrame contém as colunas necessárias
required_columns = ['Traffic_Report_ID', 'Published_Date', 'Issue_Reported', 'Location', 'Address', 'Status']

if not all(col in df.columns for col in required_columns):
    raise ValueError(f"Faltando colunas no arquivo CSV. Necessário: {required_columns}")

# Itera sobre as linhas do DataFrame e insere no banco de dados
try:
    for index, row in df.iterrows():
        # Converte Published_Date para datetime e verifica
        published_date = pd.to_datetime(row['Published_Date'], errors='coerce')

        # Verifica se a data foi convertida corretamente
        if pd.isnull(published_date):
            raise ValueError(f"Data inválida na linha {index + 1}: {row['Published_Date']}")

        # Garante que todos os valores são tratados como string, exceto a data
        traffic_report_id = str(row['Traffic_Report_ID']) if pd.notnull(row['Traffic_Report_ID']) else None
        issue_reported = str(row['Issue_Reported']) if pd.notnull(row['Issue_Reported']) else None
        location = str(row['Location']) if pd.notnull(row['Location']) else None
        address = str(row['Address']) if pd.notnull(row['Address']) else None
        status = str(row['Status']) if pd.notnull(row['Status']) else None

        # Insere os dados no banco de dados, garantindo os tipos adequados
        cursor.execute('''
            INSERT INTO [dimEndereco] 
            (Traffic_Report_ID, Published_Date, Issue_Reported, Location, Address, Status)
            VALUES (?, ?, ?, ?, ?, ?)
        ''', traffic_report_id, published_date, issue_reported, location, address, status)

    # Confirma as alterações
    conn.commit()
    print("Dados inseridos com sucesso!")

except Exception as e:
    print(f"Erro ao inserir dados: {e}")

finally:
    # Fecha o cursor e a conexão
    cursor.close()
    conn.close()
