import random

def avaliar_maturidade():
    return random.randint(60, 100)

def gerar_localizacao():
    lat = round(random.uniform(-22.0, -21.0), 6)
    long = round(random.uniform(-47.0, -46.0), 6)
    return (lat, long)

def simular_colheita(robos):
    resultados = []
    for robo in robos:
        for _ in range(random.randint(3, 5)):
            maturidade = avaliar_maturidade()
            status = "colhido" if maturidade >= 85 else "descartado"
            lat, long = gerar_localizacao()
            resultados.append({
                "id_robo": robo,
                "latitude": lat,
                "longitude": long,
                "maturidade": maturidade,
                "status": status
            })
    return resultados