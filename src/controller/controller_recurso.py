from conexion.mysql_queries import MySQLQueries
from model.recurso import Recurso

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
           """Busca um recurso pelo ID e converte em objeto Recurso para o principal.py"""
        rows = executar("SELECT id_recurso, id_local, nome, tipo_deficiencia, situacao, data_verificacao FROM recursos WHERE id_recurso = %s", (id_recurso,), fetch=True)
        if rows and len(rows) > 0:
            r = rows[0]
            return Recurso(
                id_recurso=r['id_recurso'], 
                local=r['id_local'], 
                nome=r['nome'], 
                tipo_deficiencia=r['tipo_deficiencia'], 
                situacao=r['situacao'], 
                data_verificacao=r['data_verificacao']
            )
        return None


    @staticmethod
    def inserir(recurso):
        """Recebe o objeto Recurso enviado pelo principal.py e grava no MySQL"""
        query = """
            INSERT INTO recursos (id_local, nome, tipo_deficiencia, situacao, data_verificacao) 
            VALUES (%s, %s, %s, %s, %s)
        """
        id_local_val = recurso.local.id_local if hasattr(recurso.local, 'id_local') else recurso.local
        executar(query, (id_local_val, recurso.nome, recurso.tipo_deficiencia, recurso.situacao, recurso.data_verificacao))
        return recurso

    @staticmethod
    def atualizar(recurso):
        """Atualiza os dados do recurso no banco de dados"""
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
        return True
