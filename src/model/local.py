class Local:
    def __init__(self, id_local=None, nome="", tipo="", endereco="", cidade=""):
        self.id_local = id_local
        self.nome = nome
        self.tipo = tipo
        self.endereco = endereco
        self.cidade = cidade

    def to_string(self):
        return f"ID: {self.id_local} | Nome: {self.nome} | Tipo: {self.tipo} | Cidade: {self.cidade}"
