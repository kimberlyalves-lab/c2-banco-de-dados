from controller.controller_local import ControllerLocal
from controller.controller_recurso import ControllerRecurso
from model.local import Local
from model.recurso import Recurso
from reports.relatorios import Relatorios
from utils import config
from utils.helpers import (limpar_tela, pausar, ler_texto, ler_inteiro, ler_data,
                           confirmar, imprimir_tabela)
from utils.splash_screen import SplashScreen

ctrl_local = ControllerLocal()
ctrl_recurso = ControllerRecurso()
relatorios = Relatorios()


# - utilidades
def escolher_entidade(titulo):
    print(config.MENU_ENTIDADES.format(titulo=titulo.upper(), linha="=" * 40))
    return ler_inteiro("Opção", 0, 2)


def escolher_situacao(atual=None):
    print(config.MENU_SITUACAO)
    while True:
        sufixo = f" [{atual}]" if atual else ""
        v = input(f"Opção{sufixo}: ").strip()
        if v == "" and atual:
            return atual
        if v in ("1", "2", "3"):
            return config.SITUACOES[int(v) - 1]
        print("  Opção inválida.")


def escolher_local_existente(atual: Local = None):
    colunas, linhas = ctrl_local.listar()
    if not linhas:
        print("\n  Cadastre um local antes de cadastrar recursos.")
        return None
    imprimir_tabela(colunas, linhas)
    while True:
        sufixo = f" [{atual.id_local}]" if atual else ""
        v = input(f"ID do local{sufixo}: ").strip()
        if v == "" and atual:
            return atual
        if v.isdigit():
            local = ctrl_local.buscar(int(v))
            if local:
                return local
        print("  Local não encontrado.")


def laco_operacao(titulo, acao):
    """Menu de entidades + 'deseja continuar?' (itens 6.b/6.c/6.d do edital)."""
    while True:
        limpar_tela()
        entidade = escolher_entidade(titulo)
        if entidade == 0:
            return
        acao(entidade)
        if not confirmar(f"\nDeseja continuar em '{titulo}'?"):
            return


#  inserir
def inserir(entidade):
    if entidade == 1:
        nome = ler_texto("Nome do local")
        tipo = ler_texto("Tipo (ex.: Escola, Praça, Loja)")
        endereco = ler_texto("Endereço", obrigatorio=False)
        cidade = ler_texto("Cidade")
        novo = ctrl_local.inserir(Local(None, nome, tipo, endereco, cidade))
    else:
        local = escolher_local_existente()
        if not local:
            return
        nome = ler_texto("Nome do recurso (ex.: Rampa, Piso tátil)")
        tipo_def = ler_texto("Tipo de deficiência atendida (Física, Visual, Auditiva...)")
        situacao = escolher_situacao()
        data = ler_data("Data da verificação")
        novo = ctrl_recurso.inserir(Recurso(None, local, nome, tipo_def, situacao, data))
    print("\n  Registro inserido com sucesso:")
    print("  " + novo.to_string())


# remover
def remover(entidade):
    ctrl = ctrl_local if entidade == 1 else ctrl_recurso
    colunas, linhas = ctrl.listar()
    if not linhas:
        print("\n  Não há registros para remover.")
        return
    imprimir_tabela(colunas, linhas)
    id_reg = ler_inteiro("ID do registro a remover (0 cancela)", 0)
    if id_reg == 0:
        return
    registro = ctrl.buscar(id_reg)
    if not registro:
        print("\n  Registro não encontrado.")
        return
    print("\n  " + registro.to_string())
    if not confirmar("Deseja realmente remover este registro?"):
        return
    if entidade == 1:
        if ctrl_local.possui_filhos(id_reg):
            print("\n  Este local possui recursos de acessibilidade vinculados.")
            if not confirmar("Deseja remover também os recursos vinculados?"):
                print("  Remoção cancelada: o local não pode ser excluído com recursos vinculados.")
                return
            ctrl_local.excluir(id_reg, apagar_filhos=True)
        else:
            ctrl_local.excluir(id_reg)
    else:
        ctrl_recurso.excluir(id_reg)
    print("\n  Registro removido com sucesso.")


#  atualizar
def atualizar(entidade):
    ctrl = ctrl_local if entidade == 1 else ctrl_recurso
    colunas, linhas = ctrl.listar()
    if not linhas:
        print("\n  Não há registros para atualizar.")
        return
    imprimir_tabela(colunas, linhas)
    id_reg = ler_inteiro("ID do registro a atualizar (0 cancela)", 0)
    if id_reg == 0:
        return
    atual = ctrl.buscar(id_reg)
    if not atual:
        print("\n  Registro não encontrado.")
        return
    print("\n  " + atual.to_string())
    print("  (Pressione ENTER para manter o valor atual)\n")
    if entidade == 1:
        atual.nome = ler_texto("Nome do local", atual=atual.nome)
        atual.tipo = ler_texto("Tipo", atual=atual.tipo)
        atual.endereco = ler_texto("Endereço", obrigatorio=False, atual=atual.endereco or "")
        atual.cidade = ler_texto("Cidade", atual=atual.cidade)
        atualizado = ctrl_local.atualizar(atual)
    else:
        atual.local = escolher_local_existente(atual.local)
        atual.nome = ler_texto("Nome do recurso", atual=atual.nome)
        atual.tipo_deficiencia = ler_texto("Tipo de deficiência", atual=atual.tipo_deficiencia)
        atual.situacao = escolher_situacao(atual.situacao)
        atual.data_verificacao = ler_data("Data da verificação", atual.data_verificacao)
        atualizado = ctrl_recurso.atualizar(atual)
    print("\n  Registro atualizado:")
    print("  " + atualizado.to_string())


# -relatórios
def menu_relatorios():
    while True:
        limpar_tela()
        print(config.MENU_RELATORIOS)
        op = ler_inteiro("Opção", 0, 2)
        if op == 0:
            return
        if op == 1:
            relatorios.recursos_por_local()
        else:
            relatorios.recursos_detalhados()
        pausar()


#  main
def main():
    limpar_tela()
    try:
        SplashScreen().mostrar()
    except Exception as erro:
        print(f"Erro ao conectar ao banco de dados: {erro}")
        print("Verifique as variáveis DB_HOST, DB_USER, DB_PASSWORD, DB_NAME (veja o README).")
        return
    pausar()
    while True:
        limpar_tela()
        print(config.MENU_PRINCIPAL)
        op = ler_inteiro("Opção", 0, 4)
        try:
            if op == 1:
                menu_relatorios()
            elif op == 2:
                laco_operacao("Inserir registros", inserir)
            elif op == 3:
                laco_operacao("Remover registros", remover)
            elif op == 4:
                laco_operacao("Atualizar registros", atualizar)
            else:
                print("\nEncerrando o sistema. Até logo!")
                return
        except Exception as erro:
            print(f"\n  Erro ao acessar o banco de dados: {erro}")
            pausar()


if __name__ == "__main__":
    main()
