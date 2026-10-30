import os

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')

def pausar():
    input("\nPressione ENTER para continuar...")

def ler_texto(mensagem, obrigatorio=True, atual=None):
    sufixo = f" [{atual}]" if atual else ""
    while True:
        v = input(f"{mensagem}{sufixo}: ").strip()
        if v == "" and atual is not None:
            return atual
        if v == "" and obrigatorio:
            print("  Campo obrigatório!")
            continue
        return v if v != "" else None

def ler_inteiro(mensagem, minimo, maximo=None):
    while True:
        v = input(f"{mensagem}: ").strip()
        if v.isdigit():
            num = int(v)
            if num >= minimo and (maximo is None or num <= maximo):
                return num
        print("  Opção ou número inválido.")

def confirmar(mensagem):
    while True:
        v = input(f"{mensagem} (S/N): ").strip().upper()
        if v in ('S', 'SIM'): return True
        if v in ('N', 'NAO', 'NÃO'): return False

def imprimir_tabela(colunas, linhas):
    print("\n" + "-" * 60)
    print(" | ".join(colunas))
    print("-" * 60)
    for linha in linhas:
        print(" | ".join(str(item) for item in linha))
    print("-" * 60)

from datetime import datetime

def ler_data(mensagem, atual=None):
    sufixo = f" [{atual}]" if atual else ""
    while True:
        v = input(f"{mensagem} (AAAA-MM-DD){sufixo}: ").strip()
        if v == "" and atual:
            return atual
        try:
            return datetime.strptime(v, "%Y-%m-%d").date()
        except ValueError:
            print("  Formato de data inválido! Use AAAA-MM-DD.")
