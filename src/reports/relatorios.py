from conexion.mysql_queries import MySQLQueries
from utils.helpers import imprimir_tabela

def executar_query_relatorio(caminho_sql):
    """Lê o arquivo .sql externo e executa no MySQL retornando as linhas brutas"""
    db = MySQLQueries()
    db.connect()
    try:
        # Abre e lê o arquivo de consulta SQL correspondente
        with open(caminho_sql, 'r', encoding='utf-8') as f:
            query = f.read()
            
        cursor = db.conexao.cursor(dictionary=True)
        cursor.execute(query)
        linhas_brutas = cursor.fetchall()
        cursor.close()
        
        # Converte a lista de dicionários em uma lista de tuplas/valores que a imprimir_tabela entende
        resultado_tabela = []
        for linha in linhas_brutas:
            resultado_tabela.append(list(linha.values()))
            
        return resultado_tabela
    finally:
        db.close()

class Relatorios:
    def recursos_por_local(self):
        """Relatório com AGRUPE/SUMARIZAÇÃO (Item 6.a.1.i do Edital)"""
        try:
            # Caminho do arquivo .sql criado na pasta sql
            linhas = executar_query_relatorio("sql/relatorio_recursos_por_local.sql")
            colunas = ["Situação do Recurso", "Quantidade Total"]
            
            if linhas:
                imprimir_tabela(colunas, linhas)
            else:
                print("\n  Nenhum recurso cadastrado no banco de dados para agrupar.")
        except Exception as e:
            print(f"\nErro ao ler o relatório: {e}")

    def recursos_detalhados(self):
        """Relatório com JUNÇÃO/JOIN (Item 6.a.1.ii do Edital)"""
        try:
            linhas = executar_query_relatorio("sql/relatorio_detalhado.sql")
            colunas = ["Nome do Local", "Cidade", "Recurso", "Situação"]
            
            if linhas:
                imprimir_tabela(colunas, linhas)
            else:
                print("\n  Nenhum dado cruzado encontrado (certifique-se de que os locais possuem recursos vinculados).")
        except Exception as e:
            print(f"\nErro ao ler o relatório: {e}")
