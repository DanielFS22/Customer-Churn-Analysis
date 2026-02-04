Perfeito — abaixo está o **README já adaptado**, com a **automação em Python integrada de forma natural**, profissional e alinhada ao mercado.
Você pode **substituir o README atual por este** ou ajustar partes se quiser personalizar depois.

---

# 📊 Customer Churn Analysis Using SQL, Python and Power BI

## 📌 Visão Geral

O cancelamento de clientes (churn) é um dos principais desafios enfrentados por empresas que operam com modelos de assinatura ou relacionamento contínuo. Entender **quem cancela**, **por que cancela** e **quais padrões estão associados a esse comportamento** é essencial para reduzir perdas financeiras e melhorar estratégias de retenção.

Este projeto foi desenvolvido para **simular um cenário real de mercado**, no qual atuo como **Analista de Dados**, responsável não apenas pela análise e visualização dos dados, mas também pela **automação do preparo dos dados**, garantindo qualidade, consistência e eficiência no processo analítico.

---

## 🎯 Objetivo do Projeto

* Analisar o comportamento de clientes e identificar padrões associados ao churn
* Comparar características entre clientes ativos e cancelados
* Gerar insights estratégicos para retenção de clientes
* Simular um fluxo real de dados, desde o tratamento até a visualização
* Demonstrar boas práticas de análise e automação de dados

---

## 🧠 Perguntas de Negócio Respondidas

* Qual é a taxa geral de churn da empresa?
* Clientes com menor tempo de contrato cancelam mais?
* O tipo de contrato influencia diretamente no churn?
* Existe relação entre o valor mensal pago e o cancelamento?
* Quais perfis de clientes apresentam maior risco de churn?

---

## 🗂️ Base de Dados

O projeto utiliza um dataset público de churn de clientes, amplamente utilizado para simulações de problemas reais de negócio.

**Principais atributos do dataset:**

* Idade do cliente
* Tempo de contrato
* Tipo de contrato/plano
* Valor mensal
* Uso de serviços
* Status de churn (ativo ou cancelado)

📌 Os dados brutos passam por um processo automatizado de tratamento antes da análise.

---

## 🔄 Automação e Pipeline de Dados (Python)

Para simular um ambiente corporativo real, foi desenvolvido um **script em Python** responsável por automatizar o processo de preparação dos dados.

### ⚙️ O que a automação faz:

* Leitura dos dados brutos (`raw`)
* Remoção de duplicidades
* Tratamento de valores nulos
* Padronização de categorias
* Criação de variáveis derivadas (ex: faixas de tempo de contrato e valor mensal)
* Exportação dos dados tratados (`processed`) prontos para análise

Esse processo reduz erros manuais, melhora a confiabilidade das análises e permite escalabilidade caso o volume de dados aumente.

---

## 🛠️ Ferramentas e Tecnologias Utilizadas

* **Python (pandas)** — automação, limpeza e transformação dos dados
* **SQL** — análise exploratória e extração de métricas
* **Power BI** — criação de dashboards interativos
* **Excel** — apoio na validação dos dados
* **GitHub** — versionamento e documentação

---

## 📂 Estrutura do Projeto

```text
customer-churn-analysis/
│
├── data/
│   ├── raw/
│   │   └── churn_raw.csv
│   ├── processed/
│   │   └── churn_processed.csv
│
├── scripts/
│   └── data_pipeline.py
│
├── sql/
│   └── analysis_queries.sql
│
├── dashboard/
│   └── churn_dashboard.pbix
│
├── requirements.txt
└── README.md
```

---

## 📊 Dashboard

O dashboard foi desenvolvido no Power BI com foco em **clareza**, **objetividade** e **tomada de decisão**, contendo:

* Visão geral da base de clientes
* Taxa de churn
* Perfil dos clientes cancelados
* Comparação entre clientes ativos e cancelados
* Segmentações por tipo de contrato e valor mensal

📎 *Aqui podem ser adicionadas imagens ou o link do dashboard.*

---

## 💡 Principais Insights

* Clientes com contratos mensais apresentam maior taxa de churn
* O risco de cancelamento é maior nos primeiros meses de contrato
* Clientes em determinadas faixas de valor mensal possuem maior propensão ao churn
* A fidelização aumenta conforme o tempo de relacionamento com o cliente

---

## 📈 Recomendações de Negócio

Com base nos dados analisados, algumas ações estratégicas seriam:

* Incentivar contratos de longo prazo com benefícios adicionais
* Criar ações de retenção focadas nos primeiros meses de contrato
* Monitorar clientes com alto valor mensal e curto tempo de relacionamento
* Desenvolver campanhas personalizadas para perfis de maior risco

---

## 🚀 Aprendizados e Competências Desenvolvidas

* Pensamento analítico orientado a negócio
* Automação de processos de dados com Python
* Análise de dados utilizando SQL
* Criação de dashboards executivos no Power BI
* Comunicação clara de insights e recomendações

---

## 🔮 Próximos Passos

* Implementar modelo de Machine Learning para previsão de churn
* Automatizar a carga dos dados em banco de dados
* Integrar o pipeline em ambiente cloud
* Expandir análises financeiras

---

## 👨‍💻 Autor

**Daniel Fernandes**
Estudante de Ciência da Computação | Analista de Dados em formação

🔗 GitHub: https://github.com/DanielFS22
🔗 LinkedIn: www.linkedin.com/in/danielfs22
