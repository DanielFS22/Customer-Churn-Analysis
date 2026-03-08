# 📊 Customer Churn Analysis — Python · SQL · Flask · Chart.js

## 📌 Visão Geral

O cancelamento de clientes (churn) é um dos principais desafios enfrentados por empresas que operam com relacionamento contínuo ou recorrência de compra. Entender **quem está deixando de comprar**, **quando isso acontece** e **quais padrões estão associados a esse comportamento** é essencial para reduzir perdas e melhorar estratégias de retenção.

Este projeto simula um cenário real de mercado onde atuo como **Analista de Dados**, responsável por:

- Construção do pipeline de dados (ETL completo)
- Tratamento e consolidação de múltiplas bases
- Criação de métricas estratégicas de churn
- Persistência em banco relacional MySQL
- Desenvolvimento de API REST com Flask
- Dashboard interativo web com visualizações dinâmicas

---

## 🎯 Objetivo do Projeto

- Construir um pipeline completo de ETL utilizando Python
- Consolidar múltiplas tabelas em uma visão única por cliente
- Criar métricas estratégicas de churn (feature engineering)
- Persistir os dados em banco MySQL via SQLAlchemy
- Expor os dados através de uma API REST com Flask
- Visualizar os dados em um dashboard web interativo com Chart.js

---

## 🏗️ Arquitetura do Projeto

```
Raw CSVs → Python ETL → churn_processed.csv → MySQL → Flask API → Dashboard Web
```

O projeto simula um fluxo corporativo real, onde os dados passam por tratamento automatizado antes de serem consumidos para análise e visualização.

---

## 🔄 Pipeline de Dados (Python + MySQL)

Pipeline completo em Python responsável pelas etapas de:

### 1️⃣ Extração
Leitura dos datasets brutos do e-commerce brasileiro (Olist):
- `olist_customers_dataset.csv`
- `olist_orders_dataset.csv`
- `olist_order_payments_dataset.csv`

### 2️⃣ Transformação

- Merge entre tabelas via `customer_id` e `order_id`
- Conversão de colunas de data
- Agregação por cliente único
- Feature engineering com métricas estratégicas:

| Métrica | Descrição |
|---|---|
| `total_orders` | Total de pedidos únicos por cliente |
| `total_revenue` | Receita total gerada pelo cliente |
| `last_purchase` | Data da última compra |
| `days_since_last_purchase` | Dias desde a última compra |
| `average_ticket` | Ticket médio por pedido |
| `churn` | 1 se mais de 90 dias sem compra, 0 caso contrário |

```python
churn = days_since_last_purchase > 90
```

### 3️⃣ Carga (Load)

- Geração do dataset tratado: `churn_processed.csv`
- Inserção automatizada no MySQL via `mysql-connector`
- Validação da carga via queries SQL

Total de registros inseridos: **96.096 clientes**

---

## 🌐 API REST (Flask + SQLAlchemy)

Backend desenvolvido com Flask expondo os dados via endpoints REST:

| Endpoint | Descrição |
|---|---|
| `GET /` | Serve o dashboard web |
| `GET /clientes_total` | Total de clientes na base |
| `GET /churn_rate` | Taxa de churn, total e percentual |
| `GET /churn` | Distribuição ativo vs churn |
| `GET /receita_media` | Receita média por cliente |
| `GET /ticket_medio` | Ticket médio por pedido |
| `GET /segmento` | Churn rate por segmento de cliente |
| `GET /distribuicao_dias` | Clientes por faixa de dias sem compra |

A conexão com o banco é feita via **SQLAlchemy**, eliminando os warnings do pandas e garantindo compatibilidade total com `pd.read_sql`.

---

## 📊 Dashboard Web (HTML · CSS · JavaScript · Chart.js)

Interface interativa dark theme com **duas abas**:

### Aba Dashboard
- 5 KPI cards — Total de Clientes, Em Churn, Churn Rate, Receita Média e Ticket Médio
- Gráfico de rosca — Distribuição Ativo vs Churn
- Gráfico de barras — Churn Rate por Segmento (com cores dinâmicas de risco)
- Gráfico de barras — Distribuição por faixa de dias sem compra
- Gráfico de barras — Total de clientes por segmento
- Tabela com badges de status por segmento (Estável / Atenção / Crítico)

### Aba Explorador de Dados
- Gerador de gráfico dinâmico — escolha a fonte de dados, métrica e tipo de visualização
- Painel de resumo com todos os KPIs em cards
- Tabela comparativa de segmentos com barra de risco visual proporcional

---

## 📂 Estrutura do Projeto

```text
Customer-Churn-Analysis/
│
├── data/
│   ├── raw/
│   │   ├── olist_customers_dataset.csv
│   │   ├── olist_orders_dataset.csv
│   │   └── olist_order_payments_dataset.csv
│   └── processed/
│       └── churn_processed.csv
│
├── scripts/
│   ├── data_pipeline.py        # ETL completo
│   └── database.py             # Conexão MySQL
│
├── SQL/
│   ├── create_table.sql        # Schema da tabela
│   ├── analysis_queries.sql    # Queries analíticas
│   └── validation_queries.sql  # Validação da carga
│
├── Dashboard/
│   ├── app.py                  # API Flask + SQLAlchemy
│   ├── index.html              # Dashboard web
│   ├── style.css               # Dark theme
│   └── script.js               # Lógica e gráficos
│
├── .gitignore
├── requirements.txt
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

| Tecnologia | Uso |
|---|---|
| **Python · pandas** | ETL e feature engineering |
| **MySQL** | Persistência relacional |
| **SQLAlchemy** | Conexão segura com o banco |
| **Flask · flask-cors** | API REST e servidor web |
| **HTML · CSS · JavaScript** | Dashboard interativo |
| **Chart.js** | Visualizações dinâmicas |
| **SQL** | Queries analíticas e validação |
| **Git · GitHub** | Versionamento |

---

## 🚀 Como Rodar o Projeto

**1. Instalar dependências:**
```bash
pip install -r requirements.txt
```

**2. Garantir que o MySQL está rodando** com o banco `churn_project` populado (rodar `data_pipeline.py` se necessário).

**3. Iniciar o servidor Flask:**
```bash
cd Dashboard
python app.py
```

**4. Abrir no navegador:**
```
http://127.0.0.1:5000
```

> ⚠️ Sempre acesse pelo endereço Flask — nunca abra o `index.html` diretamente no navegador, pois o CORS bloqueará as requisições.

---

## 💡 Competências Demonstradas

- Pipeline ETL completo em Python
- Feature engineering aplicada a dados de negócio
- Modelagem de métricas estratégicas (churn, ticket médio, segmentação)
- Integração Python + MySQL + SQLAlchemy
- Desenvolvimento de API REST com Flask
- Construção de dashboard web interativo do zero
- Visualização de dados com Chart.js
- Organização de projeto orientado a portfólio
- Versionamento com Git e boas práticas de repositório

---

## 🔮 Próximos Passos

- [ ] Implementar modelo preditivo de churn (Machine Learning)
- [ ] Adicionar autenticação na API
- [ ] Automatizar carga incremental de dados
- [ ] Deploy em ambiente cloud (Heroku / Railway / Render)
- [ ] Implementar testes automatizados

---

## 👨‍💻 Autor

**Daniel Fernandes**
Estudante de Ciência da Computação | Analista de Dados em formação

🔗 GitHub: [github.com/DanielFS22](https://github.com/DanielFS22)
🔗 LinkedIn: [linkedin.com/in/danielfs22](https://www.linkedin.com/in/danielfs22)