import oracledb

def conectar_oracle():
    connection = oracledb.connect(
        user="system",
        password="123456",
        dsn="localhost:1521/XEPDB1",
        mode=oracledb.DEFAULT_AUTH
    )
    return connection

def inserir_colheita(conn, coleta):
    with conn.cursor() as cursor:
        sql = """
            INSERT INTO soja_colheita (id_robo, latitude, longitude, maturidade, status)
            VALUES (:1, :2, :3, :4, :5)
        """
        cursor.execute(sql, (
            coleta['id_robo'],
            coleta['latitude'],
            coleta['longitude'],
            coleta['maturidade'],
            coleta['status']
        ))
    conn.commit()

def listar_colheitas(conn):
    with conn.cursor() as cursor:
        cursor.execute("""
            SELECT sc.id_colheita, r.modelo, sc.latitude, sc.longitude, sc.maturidade, sc.status
            FROM soja_colheita sc
            JOIN robos r ON sc.id_robo = r.id_robo
            ORDER BY sc.data_coleta DESC
        """)
        rows = cursor.fetchall()
        colheitas = []
        for row in rows:
            colheitas.append({
                "id": row[0],
                "modelo": row[1],
                "latitude": row[2],
                "longitude": row[3],
                "maturidade": row[4],
                "status": row[5]
            })
        return colheitas

def listar_robos(conn):
    with conn.cursor() as cursor:
        cursor.execute("SELECT id_robo FROM robos")
        return [str(r[0]) for r in cursor.fetchall()]

def inserir_robo(conn, modelo, status, localizacao):
    with conn.cursor() as cursor:
        cursor.execute("""
            INSERT INTO robos (modelo, status, ultima_localizacao)
            VALUES (:1, :2, :3)
        """, (modelo, status, localizacao))
    conn.commit()