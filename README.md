# 📊 Customer Churn Analysis Using Python, SQL and Power BI

## 📌 Visão Geral

O cancelamento de clientes (churn) é um dos principais desafios enfrentados por empresas que operam com relacionamento contínuo ou recorrência de compra. Entender **quem está deixando de comprar**, **quando isso acontece** e **quais padrões estão associados a esse comportamento** é essencial para reduzir perdas e melhorar estratégias de retenção.

Este projeto simula um cenário real de mercado onde atuo como **Analista de Dados**, responsável por:

- Construção do pipeline de dados
- Tratamento e consolidação das bases
- Criação de métricas estratégicas
- Persistência em banco relacional
- Preparação da base para visualização executiva

---

## 🎯 Objetivo do Projeto

- Construir um pipeline completo de ETL utilizando Python
- Consolidar múltiplas tabelas em uma visão única por cliente
- Criar métricas estratégicas de churn
- Persistir os dados em banco MySQL
- Servir como base para um dashboard executivo no Power BI

---

## 🏗️ Arquitetura do Projeto

```

Raw Data → Python (ETL & Feature Engineering) → Processed CSV → MySQL → Power BI (em desenvolvimento)

````

O projeto simula um fluxo corporativo real, onde os dados passam por tratamento automatizado antes de serem consumidos para análise.

---

## 🔄 Pipeline de Dados (Python + MySQL)

Foi desenvolvido um pipeline completo em Python responsável pelas etapas de:

### 1️⃣ Extração
Leitura dos datasets brutos:
- `customers`
- `orders`
- `payments`

---

### 2️⃣ Transformação

- Merge entre tabelas
- Conversão de colunas de data
- Agregação por cliente
- Criação de métricas estratégicas:

**Métricas criadas:**

- `total_orders`
- `total_revenue`
- `last_purchase`
- `days_since_last_purchase`
- `average_ticket`
- `churn` (regra de negócio: cliente com mais de 90 dias sem compra)

```python
churn = days_since_last_purchase > 90
````

Essa etapa simula o processo de **feature engineering aplicado a dados de negócio**.

---

### 3️⃣ Carga (Load)

* Geração do dataset tratado: `churn_processed.csv`
* Inserção automatizada no MySQL
* Validação da carga via query SQL

Total de registros inseridos: **96.096**

```sql
SELECT COUNT(*) FROM customers_churn;
```

---

## 🗄️ Banco de Dados

Banco: `churn_project`
Tabela: `customers_churn`

A tabela é alimentada diretamente pelo script Python via conexão MySQL, simulando um fluxo de dados empresarial com persistência relacional.

---

## 📂 Estrutura do Projeto

```text
customer-churn-analysis/
│
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders.csv
│   │   └── payments.csv
│   │
│   └── processed/
│       └── churn_processed.csv
│
├── scripts/
│   ├── data_pipeline.py
│   └── database.py
│
├── sql/
│   └── validation_queries.sql
│
├── dashboard/
│   └── churn_dashboard.pbix (em desenvolvimento)
│
├── requirements.txt
└── README.md
```

---

## 🛠️ Tecnologias Utilizadas

* **Python (pandas)** — ETL e feature engineering
* **MySQL** — Persistência relacional
* **SQL** — Validação e consultas analíticas
* **MySQL Workbench** — Gerenciamento do banco
* **Power BI** — Visualização executiva (em desenvolvimento)
* **Git & GitHub** — Versionamento

---

## 📊 Próxima Etapa: Visualização

O próximo passo do projeto é conectar o Power BI diretamente ao banco MySQL para:

* Construir KPIs estratégicos
* Criar visão executiva de churn
* Analisar perfis de risco
* Simular tomada de decisão orientada a dados

---

## 💡 Competências Demonstradas

* Construção de pipeline ETL em Python
* Modelagem de métricas de negócio
* Integração Python + MySQL
* Estruturação de projeto orientado a portfólio
* Organização de arquitetura de dados
* Pensamento analítico aplicado a churn

---

## 🔮 Próximos Passos

* Implementar modelo preditivo de churn
* Automatizar carga incremental
* Publicar dashboard interativo
* Integrar pipeline em ambiente cloud

---

## 👨‍💻 Autor

**Daniel Fernandes**
Estudante de Ciência da Computação | Analista de Dados em formação

🔗 GitHub: [https://github.com/DanielFS22](https://github.com/DanielFS22)
🔗 LinkedIn: [www.linkedin.com/in/danielfs22](http://www.linkedin.com/in/danielfs22)

Amanhã a gente começa o Dia 05 — Power BI conectado ao MySQL 🚀
```
