from robots import simular_colheita
from utils import salvar_json, salvar_txt
from db_oracle import (
    inserir_colheita,
    conectar_oracle,
    listar_colheitas,
    listar_robos,
    inserir_robo
)

def menu():
    while True:
        print("\n=== MENU GERAL ===")
        print("1. Gerenciar Robôs")
        print("2. Simular colheita")
        print("3. Listar coletas registradas")
        print("4. Exportar coletas (JSON/TXT)")
        print("5. Inserir colheita manual")
        print("6. Sair")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            menu_robos()
        elif opcao == "2":
            simular()
        elif opcao == "3":
            listar()
        elif opcao == "4":
            exportar()
        elif opcao == "5":
            inserir_manual()
        elif opcao == "6":
            print("Encerrando aplicação...")
            break
        else:
            print("Opção inválida. Tente novamente.")

def menu_robos():
    conn = conectar_oracle()
    while True:
        print("\n=== MENU DE ROBÔS ===")
        print("1. Cadastrar novo robô")
        print("2. Listar robôs")
        print("3. Editar robô")
        print("4. Voltar ao menu principal")
        opcao = input("Escolha uma opção: ")

        if opcao == "1":
            cadastrar_robo(conn)
        elif opcao == "2":
            listar_robos_ui(conn)
        elif opcao == "3":
            editar_robo(conn)
        elif opcao == "4":
            break
        else:
            print("Opção inválida. Tente novamente.")

def simular():
    conn = conectar_oracle()
    robos = listar_robos(conn)
    if not robos:
        print("⚠️ Nenhum robô cadastrado. Cadastre ao menos um robô antes de simular colheita.")
        return
    resultados = simular_colheita(robos)
    for coleta in resultados:
        inserir_colheita(conn, coleta)
    print(f"{len(resultados)} coletas simuladas e salvas no banco de dados Oracle.")

def listar():
    conn = conectar_oracle()
    colheitas = listar_colheitas(conn)
    print("\n=== REGISTROS DE COLHEITA ===")
    for c in colheitas:
        print(f"ID {c['id']} | Robô: {c['modelo']} | Maturidade: {c['maturidade']}% | Status: {c['status']}")


def exportar():
    conn = conectar_oracle()
    colheitas = listar_colheitas(conn)
    salvar_json(colheitas, "data/export_colheitas.json")
    salvar_txt(colheitas, "data/export_colheitas.txt")
    print("Dados exportados com sucesso!")

def inserir_manual():
    conn = conectar_oracle()
    robos = []
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_robo, modelo FROM robos")
        robos = cursor.fetchall()

    if not robos:
        print("⚠️ Nenhum robô cadastrado.")
        return

    print("\n=== SELECIONE O ROBÔ ===")
    for r in robos:
        print(f"{r[0]} - {r[1]}")
    id_robo = input("Digite o número do robô desejado: ")
    if id_robo not in [str(r[0]) for r in robos]:
        print("⚠️ Robô não encontrado.")
        return

    try:
        lat = float(input("Latitude: ").replace(",", "."))
        lon = float(input("Longitude: ").replace(",", "."))
    except ValueError:
        print("❌ Latitude/Longitude inválida.")
        return

    maturidade = int(input("Maturidade (0-100): "))
    status = input("Status (colhido/descartado): ")

    if abs(lat) > 999.999999 or abs(lon) > 999.999999:
        print("Erro: latitude/longitude muito grandes. Use até 6 casas decimais e total de 10 dígitos.")
        return

    coleta = {
        "id_robo": int(id_robo),
        "latitude": lat,
        "longitude": lon,
        "maturidade": maturidade,
        "status": status
    }

    inserir_colheita(conn, coleta)
    print("✅ Colheita inserida manualmente com sucesso.")


def cadastrar_robo(conn):
    modelo = input("Modelo do robô: ")
    status = input("Status (ativo/inativo): ")
    localizacao = input("Última localização (texto): ")
    inserir_robo(conn, modelo, status, localizacao)
    print("Robô cadastrado com sucesso.")

def listar_robos_ui(conn):
    print("\n=== LISTA DE ROBÔS ===")
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_robo, modelo, status, ultima_localizacao FROM robos")
        robos = cursor.fetchall()
        for robo in robos:
            print(f"ID: {robo[0]} | Modelo: {robo[1]} | Status: {robo[2]} | Última Localização: {robo[3]}")

def editar_robo(conn):
    id_robo = input("Digite o ID do robô que deseja editar: ")
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_robo FROM robos WHERE id_robo = :1", [id_robo])
        if not cursor.fetchone():
            print("⚠️ Robô não encontrado.")
            return

    novo_modelo = input("Novo modelo: ")
    novo_status = input("Novo status (ativo/inativo): ")
    nova_localizacao = input("Nova localização: ")

    with conn.cursor() as cursor:
        cursor.execute("""
            UPDATE robos
            SET modelo = :1, status = :2, ultima_localizacao = :3
            WHERE id_robo = :4
        """, (novo_modelo, novo_status, nova_localizacao, id_robo))
    conn.commit()
    print("Robô atualizado com sucesso.")

if __name__ == "__main__":
    menu()