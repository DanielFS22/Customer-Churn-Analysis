import pandas as pd
import mysql.connector
from sqlalchemy import create_engine, text

# ── Credenciais Railway ──────────────────────────────────────
DB_HOST = "yamabiko.proxy.rlwy.net"
DB_PORT = 38578
DB_USER = "root"
DB_PASS = "sEkuMaDhcJzsXVmWpKPXEdhtIfcUZsrQ"
DB_NAME = "railway"

# ── Caminhos dos CSVs ────────────────────────────────────────
# Ajuste os caminhos conforme a estrutura do seu projeto
PATH_CUSTOMERS = "data/raw/olist_customers_dataset.csv"
PATH_ORDERS    = "data/raw/olist_orders_dataset.csv"
PATH_PAYMENTS  = "data/raw/olist_order_payments_dataset.csv"

print("Lendo CSVs...")
customers = pd.read_csv(PATH_CUSTOMERS)
orders    = pd.read_csv(PATH_ORDERS)
payments  = pd.read_csv(PATH_PAYMENTS)

# ── Merge ────────────────────────────────────────────────────
print("Fazendo merge...")
orders = orders[orders["order_status"] == "delivered"]

df = orders.merge(customers, on="customer_id", how="left")
df = df.merge(payments.groupby("order_id")["payment_value"].sum().reset_index(),
              on="order_id", how="left")

df["order_purchase_timestamp"] = pd.to_datetime(df["order_purchase_timestamp"])

# ── Feature Engineering ──────────────────────────────────────
print("Calculando features...")
reference_date = df["order_purchase_timestamp"].max()

agg = df.groupby("customer_id").agg(
    total_orders   = ("order_id",                  "count"),
    total_revenue  = ("payment_value",             "sum"),
    last_purchase  = ("order_purchase_timestamp",  "max"),
    average_ticket = ("payment_value",             "mean"),
).reset_index()

agg["days_since_last_purchase"] = (reference_date - agg["last_purchase"]).dt.days
agg["churn"] = (agg["days_since_last_purchase"] > 90).astype(int)
agg["last_purchase"] = agg["last_purchase"].dt.date
agg["total_revenue"]  = agg["total_revenue"].round(2)
agg["average_ticket"] = agg["average_ticket"].round(2)

print(f"Total de registros: {len(agg)}")
print(f"Churn rate: {agg['churn'].mean()*100:.1f}%")

# ── Criar tabela no Railway ──────────────────────────────────
print("Conectando ao Railway MySQL...")
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

with engine.connect() as con:
    con.execute(text("""
        CREATE TABLE IF NOT EXISTS customers_churn (
            customer_id              VARCHAR(255) PRIMARY KEY,
            total_orders             INT,
            total_revenue            FLOAT,
            last_purchase            DATE,
            days_since_last_purchase INT,
            average_ticket           FLOAT,
            churn                    BOOLEAN
        )
    """))
    con.execute(text("TRUNCATE TABLE customers_churn"))
    con.commit()
    print("Tabela criada/limpa com sucesso.")

# ── Inserir dados ────────────────────────────────────────────
print("Inserindo dados no Railway...")
agg.to_sql(
    name="customers_churn",
    con=engine,
    if_exists="append",
    index=False,
    chunksize=1000
)

print("Concluido! Banco Railway populado com sucesso.")