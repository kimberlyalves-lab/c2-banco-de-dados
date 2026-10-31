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
        linhas_brutas = executar("SELECT id_local, nome, tipo, endereco, cidade FROM locais ORDER BY id_local", fetch=True)
        colunas = ["ID", "Nome", "Tipo", "Endereço", "Cidade"]
        
        linhas_formatadas = []
        if linhas_brutas:
            for r in linhas_brutas:
                if isinstance(r, dict):
                    linhas_formatadas.append((r['id_local'], r['nome'], r['tipo'], r['endereco'], r['cidade']))
                else:
                    linhas_formatadas.append(r)
        return colunas, linhas_formatadas
    
    @staticmethod  
    def possui_filhos(id_local):
        """Verifica se existem recursos vinculados a este local antes de excluir"""
        linhas = executar("SELECT COUNT(*) AS total FROM recursos WHERE id_local = %s", (id_local,), fetch=True)
        if linhas:
            # Como a resposta vem em uma lista de dicionários ou dicionário direto
            r = linhas[0] if isinstance(linhas, list) else linhas
            if isinstance(r, dict):
                return r['total'] > 0
            elif isinstance(r, (list, tuple)):
                return r[0] > 0
        return False

    @staticmethod
    def buscar(id_local): 
        """Busca um local específico pelo ID e converte em objeto Local para o principal.py"""
        rows = executar("SELECT id_local, nome, tipo, endereco, cidade FROM locais WHERE id_local = %s", (id_local,), True)
        if rows:
            r = rows[0] if isinstance(rows, list) else rows
            if isinstance(r, dict):
                return Local(id_local=r['id_local'], nome=r['nome'], tipo=r['tipo'], endereco=r['endereco'], cidade=r['cidade'])
            else:
                return Local(id_local=r[0], nome=r[1], tipo=r[2], endereco=r[3], cidade=r[4])
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
        """Exclui o local e remove os recursos filhos em cascata se solicitado"""
        if apagar_filhos:
            executar("DELETE FROM recursos WHERE id_local=%s", (id_local,))
        executar("DELETE FROM locais WHERE id_local=%s", (id_local,))
        return True
