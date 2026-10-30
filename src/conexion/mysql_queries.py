# src/conexion/mysql_queries.py
import mysql.connector
from mysql.connector import Error

class MySQLQueries:
    def __init__(self):
        # acesso ao banco de dados 
        self.host = "localhost"
        self.user = "root"         
        self.password = "Rebeca2010@"  
        self.database = "acessibilidade"
        self.conexao = None

    def connect(self):
        """Abre a conexão com o banco de dados"""
        try:
            self.conexao = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
        except Error as erro:
            print(f"Erro ao conectar ao MySQL: {erro}")
            raise erro

    def close(self):
        """Fecha a conexão de forma segura"""
        if self.conexao and self.conexao.is_connected():
            self.conexao.close()

    def execute(self, query: str, params: tuple = None):
        """Executa comandos que alteram dados: INSERT, UPDATE, DELETE (Puro, sem ORM)"""
        if not self.conexao or not self.conexao.is_connected():
            self.connect()
            
        cursor = self.conexao.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.conexao.commit()  
        except Error as erro:
            self.conexao.rollback() 
            print(f"Erro de execução SQL: {erro}")
            raise erro
        finally:
            cursor.close()

    def read(self, query: str, params: tuple = None):
        """Executa comandos de leitura (SELECT) retornando colunas e linhas estruturadas"""
        if not self.conexao or not self.conexao.is_connected():
            self.connect()
            
        # dictionary=True faz com que cada linha retorne como dicionário para o principal.py
        cursor = self.conexao.cursor(dictionary=True)
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
                
            linhas = cursor.fetchall()
            colunas = [desc[0] for desc in cursor.description] if cursor.description else []
            return colunas, linhas
        except Error as erro:
            print(f"Erro de leitura SQL: {erro}")
            raise erro
        finally:
            cursor.close()
