from conexion.mysql_queries import MySQLQueries
from model.local import Local  

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

class ControllerLocal:
    @staticmethod  
    def listar():
        linhas = executar("SELECT id_local, nome, tipo, endereco, cidade FROM locais ORDER BY id_local", fetch=True)
        colunas = ["ID", "Nome", "Tipo", "Endereço", "Cidade"]
        return colunas, linhas
    
    @staticmethod  
    def possui_filhos(id_local):
        """Verifica se existem recursos vinculados a este local antes de excluir"""
        linhas = executar("SELECT COUNT(*) AS total FROM recursos WHERE id_local = %s", (id_local,), fetch=True)
        if linhas and len(linhas) > 0:
            # Como a resposta vem dentro de uma lista de dicionários: [{'total': 0}]
            total = linhas[0]['total']
            return total > 0
        return False

    @staticmethod
    def buscar(id_local): 
        rows = executar("SELECT id_local, nome, tipo, endereco, cidade FROM locais WHERE id_local = %s", (id_local,), True)
        if rows and len(rows) > 0:
            # Pega apenas o primeiro dicionário da lista de resultados
            r = rows[0]
            return Local(id_local=r['id_local'], nome=r['nome'], tipo=r['tipo'], endereco=r['endereco'], cidade=r['cidade'])
        return None

    @staticmethod
    def inserir(local):
        """Recebe o objeto Local enviado pelo principal.py e insere no MySQL"""
        db = MySQLQueries()
        db.connect()
        cursor = db.conexao.cursor()
        query = "INSERT INTO locais (nome, tipo, endereco, cidade) VALUES (%s, %s, %s, %s)"
        cursor.execute(query, (local.nome, local.tipo, local.endereco, local.cidade))
        db.conexao.commit()
        local.id_local = cursor.lastrowid  
        cursor.close()
        db.close()
        return local

    @staticmethod
    def atualizar(local):
        """Recebe o objeto Local alterado e atualiza no MySQL"""
        executar(
            "UPDATE locais SET nome=%s, tipo=%s, endereco=%s, cidade=%s WHERE id_local=%s", 
            (local.nome, local.tipo, local.endereco, local.cidade, local.id_local)
        )
        return local

    @staticmethod
    def excluir(id_local, apagar_filhos=False):
        """Exclui o local e remove os recursos filhos"""
        if apagar_filhos:
            executar("DELETE FROM recursos WHERE id_local=%s", (id_local,))
        executar("DELETE FROM locais WHERE id_local=%s", (id_local,))
        return True
