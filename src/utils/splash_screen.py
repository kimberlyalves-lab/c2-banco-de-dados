from conexion.mysql_queries import MySQLQueries

class SplashScreen:
    def mostrar(self):
        
        print("#" * 65)
        print("#              SISTEMA DE ACESSIBILIDADE E RECURSOS             #")
        print("#                                                               #")
        print("#   CRIADO POR: KIMBERLY ALVES DOS SANTOS                       #")
        print("#                                                               #")
        print("#   DISCIPLINA: BANCO DE DADOS                                  #")
        print("#               2026/2                                          #")
        print("#   PROFESSOR:  HOWARD ROATTI                                   #")
        print("#" * 65)
        print("Inicializando conexão com o banco de dados...")
        
        try:
            db = MySQLQueries()
            col_l, lin_l = db.read("SELECT COUNT(1) AS total FROM locais")
            col_r, lin_r = db.read("SELECT COUNT(1) AS total FROM recursos")
            
            total_locais = lin_l[0]['total'] if lin_l else 0
            total_recursos = lin_r[0]['total'] if lin_r else 0
            
            print(f"\n📊 [STATUS DO SISTEMA]")
            print(f"   -> {total_locais} locais mapeados no banco.")
            print(f"   -> {total_recursos} recursos de acessibilidade cadastrados.")
        except Exception as e:
            print(f"\nModo offline: {e}")
        
        print("=" * 65)
