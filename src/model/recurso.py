class Recurso:
    def __init__(self, id_recurso=None, local=None, nome="", tipo_deficiencia="", situacao="", data_verificacao=None):
        self.id_recurso = id_recurso
        self.local = local  # Objeto do tipo Local
        self.nome = nome
        self.tipo_deficiencia = tipo_deficiencia
        self.situacao = situacao
        self.data_verificacao = data_verificacao

    def to_string(self):
        nome_local = self.local.nome if hasattr(self.local, 'nome') else str(self.local)
        return f"ID: {self.id_recurso} | Local: {nome_local} | Recurso: {self.nome} | Status: {self.situacao}"
