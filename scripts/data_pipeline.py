import datetime as dt
import pandas as pd
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho para os dados brutos
RAW_DATA_PATH = BASE_DIR / "data" / "raw"

# Função responsável por carregar qualquer dataset CSV da pasta raw
def load_dataset(file_name):
    file_path = RAW_DATA_PATH / file_name
    df = pd.read_csv(file_path)
    return df

# Função para inspecionar rapidamente o dataset
def inspect_data(df, name):
    print(f"\n{name}")
    print(df.shape)
    print(df.info())
    print(df.isnull().sum())

# Esse bloco só executa se rodarmos este arquivo diretamente
if __name__ == "__main__":
    
    #carregar datasets
    customers = load_dataset("olist_customers_dataset.csv")
    orders = load_dataset("olist_orders_dataset.csv")
    payments = load_dataset("olist_order_payments_dataset.csv")

    print("Dataset carregado com sucesso!")

    # Inspeção inicial para entender estrutura e possíveis nulos
    inspect_data(customers, "Customers")
    inspect_data(orders, "Orders")
    inspect_data(payments, "Payments")


    #Merge custumers + orders
    customers_orders_df = customers.merge(
        orders,
        on="customer_id",
        how="left"             # how="left" mantém todos os clientes mesmo que não tenham pedido
    )

    print("\nApós merge customers + orders:")
    print(customers_orders_df.shape)

    #Merge com  Payments - Junta a base anterior com pagamentos usando order_id
    df_final = customers_orders_df.merge(
        payments,
        on="order_id",
        how="left"
    )

    print("\nBase final consolidada: ")
    print(df_final.shape)

    df_final["order_purchase_timestamp"] = pd.to_datetime(
        df_final["order_purchase_timestamp"]
    )




    # Criação de métricas por cliente

    # Agrupa por cliente único
    # Cria métricas importantes para análise de churn
    customers_metrics = df_final.groupby("customer_unique_id").agg(
        total_orders=("order_id", "nunique"),               # Total de pedidos únicos
        total_revenue=("payment_value", "sum"),             # Receita total do cliente
        last_purchase=("order_purchase_timestamp", "max")   # Data da última compra
    ).reset_index() # Remove o índice hierárquico criado pelo groupby

    print('\nMétricas por Cliente:')
    print(customers_metrics.head())
    print(df_final.duplicated().sum())

    # Days Since Last Purchase
    reference_date = df_final["order_purchase_timestamp"].max()

    customers_metrics["days_since_last_purchase"] = (
        reference_date - customers_metrics["last_purchase"]
    ).dt.days

    # Avarage Ticket
    customers_metrics["average_ticket"] = (
        customers_metrics["total_revenue"] /
        customers_metrics["total_orders"]
    )

    #verificação de valores nulos dentro da "customers_metrics"
    print("\nNulos em customers_metrics:")
    print(customers_metrics.isnull().sum())

    customers_metrics["churn"] = (
        customers_metrics["days_since_last_purchase"] > 90
    ).astype(int)

    customers_metrics.to_csv(
        BASE_DIR / "data" / "processed" / "churn_processed.csv",
        index=False
    )

