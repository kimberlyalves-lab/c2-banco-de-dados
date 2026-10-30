from conexion.mysql_queries import MySQLQueries

def executar(sql, params=None, fetch=False):
    db = MySQLQueries()
    db.connect()
    try:
        if fetch:
            colunas, linhas = db.read(sql, params)
            return linhas 
        else:
            db.execute(sql, params)  
    finally:
        db.close()

class ControllerRecurso:
    @staticmethod
    def listar():
        linhas = executar("SELECT id_recurso, id_local, nome, tipo_deficiencia, situacao, data_verificacao FROM recursos ORDER BY id_recurso", fetch=True)
        colunas = ["ID", "ID Local", "Nome", "Tipo Deficiência", "Situação", "Data Verificação"]
        return colunas, linhas

    @staticmethod
    def buscar(id_recurso):
        rows = executar("SELECT id_recurso, id_local, nome, tipo_deficiencia, situacao, data_verificacao FROM recursos WHERE id_recurso = %s", (id_recurso,), True)
        return rows if rows else None

    @staticmethod
    def inserir(recurso):
        """Recebe o objecto Recurso enviado pelo principal.py e grava no MySQL usando execute"""
        query = """
            INSERT INTO recursos (id_local, nome, tipo_deficiencia, situacao, data_verificacao) 
            VALUES (%s, %s, %s, %s, %s)
        """
        # Se recurso.local for um objeto, pegamos o ID dele
        id_local_val = recurso.local.id_local if hasattr(recurso.local, 'id_local') else recurso.local
        
        executar(query, (id_local_val, recurso.nome, recurso.tipo_deficiencia, recurso.situacao, recurso.data_verificacao))
        return recurso

    @staticmethod
    def atualizar(recurso):
        """Atualiza os dados do recurso usando o método execute do banco"""
        query = """
            UPDATE recursos 
            SET id_local=%s, nome=%s, tipo_deficiencia=%s, situacao=%s, data_verificacao=%s 
            WHERE id_recurso=%s
        """
        id_local_val = recurso.local.id_local if hasattr(recurso.local, 'id_local') else recurso.local
        
        executar(query, (id_local_val, recurso.nome, recurso.tipo_deficiencia, recurso.situacao, recurso.data_verificacao, recurso.id_recurso))
        return recurso

    @staticmethod
    def excluir(id_recurso):
        executar("DELETE FROM recursos WHERE id_recurso=%s", (id_recurso,))
