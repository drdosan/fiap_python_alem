# 🌱 ECRS - Enxame de Colheita Robótica Seletiva (Simulador em Python)

Este projeto simula um sistema de colheita inteligente para soja utilizando o conceito de **enxames de robôs autônomos**, controlados por lógica computacional, com **armazenamento dos dados em um banco de dados Oracle**.

---

## 🎯 Objetivo

Oferecer uma aplicação educacional e funcional que:
- Simule robôs colhendo soja com base na maturidade das plantas
- Armazene os dados em tabelas relacionais Oracle com integridade
- Exporte os registros em arquivos `.json` e `.txt`
- Possua menu interativo via terminal para facilitar o uso

---

## ⚙️ Estrutura do Projeto

```
ECRS_Coleta_Soja/
│
├── main.py                 # Aplicação principal com menu
├── robots.py               # Lógica dos robôs simuladores
├── db_oracle.py            # Conexão e manipulação do banco Oracle
├── utils.py                # Funções auxiliares de exportação e tela
├── soja_colheita.sql       # Script SQL para criar as tabelas Oracle
├── data/                   # Pasta onde os arquivos JSON e TXT são salvos
└── README.md               # Este documento
```

---

## 🧠 Como Funciona

### 📌 Menu Principal

Ao executar o `main.py`, você verá o seguinte menu:

```
=== MENU GERAL ===
1. Gerenciar Robôs
2. Simular colheita
3. Listar coletas registradas
4. Exportar coletas (JSON/TXT)
5. Inserir colheita manual
6. Sair
```

---

## 🤖 Gerenciamento de Robôs

No menu de robôs você pode:

- Cadastrar um novo robô (apenas informando modelo, status e localização)
- Listar todos os robôs cadastrados
- Editar robôs existentes
- IDs dos robôs são **gerados automaticamente** e usados como chave estrangeira na tabela de colheita

---

## 🔄 Operações de Colheita

### Simular colheita
- Gera entre 3 a 5 coletas por robô existente
- Se maturidade ≥ 85%, status = "colhido", senão "descartado"
- As coletas são salvas diretamente no banco Oracle

### Inserir colheita manual
- Você informa o ID de um robô existente, a localização e maturidade da soja
- O sistema salva os dados na tabela `soja_colheita`

---

## 🗃️ Banco de Dados Oracle

### Tabelas utilizadas

```sql
CREATE TABLE robos (
    id_robo NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    modelo VARCHAR2(50),
    status VARCHAR2(20),
    ultima_localizacao VARCHAR2(100)
);

CREATE TABLE soja_colheita (
    id_colheita NUMBER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
    id_robo NUMBER,
    latitude NUMBER(10,6),
    longitude NUMBER(10,6),
    maturidade NUMBER(3),
    status VARCHAR2(20),
    data_coleta TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT fk_robo FOREIGN KEY (id_robo) REFERENCES robos(id_robo)
);
```

---

## 📦 Requisitos

- Python 3.8+
- oracledb (`pip install oracledb`)
- Oracle XE (instância local)
- Para funcionamento da aplicação, adicionar os parametros de conexão do banco de dados a ser utilizado no arquivo `db_oracle.py`

---

## 🧪 Exemplo de execução

```bash
python main.py
```

---

## 👨‍💻 Autor

Desenvolvido para fins acadêmicos e práticos com foco em automação, agricultura digital e bancos de dados relacionais.

Alunos:
- VERA MARIA CHAVES DE SOUZA - RM 565497
- PATRÍCIA DE JESUS FERREIRA - RM 565558
- DIOGO REBELLO DOS SANTOS - RM 565286
- MARCOS VINÍCIUS DOS SANTOS FERNANDES - RM 565555
- ANDRÉ DE OLIVEIRA SANTOS BURGER - RM 565150