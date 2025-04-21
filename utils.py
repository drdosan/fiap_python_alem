import json
import os

def salvar_json(dados, caminho):
    with open(caminho, 'w', encoding='utf-8') as f:
        json.dump(dados, f, indent=4)

def salvar_txt(dados, caminho):
    with open(caminho, 'w', encoding='utf-8') as f:
        for item in dados:
            linha = f"{item['id_robo']} | {item['latitude']},{item['longitude']} | {item['maturidade']}% | {item['status']}\n"
            f.write(linha)

def limpar_tela():
    os.system('cls' if os.name == 'nt' else 'clear')