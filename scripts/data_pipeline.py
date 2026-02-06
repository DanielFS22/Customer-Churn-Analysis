import pandas as pd
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent

# Caminho para os dados brutos
RAW_DATA_PATH = BASE_DIR / "data" / "raw"

def load_dataset(file_name):
    file_path = RAW_DATA_PATH / file_name
    df = pd.read_csv(file_path)
    return df

if __name__ == "__main__":
    df = load_dataset("olist_customers_dataset.csv")  # troque pelo nome real do CSV
    print("Dataset carregado com sucesso!")
    print(df.head())
    print(list(RAW_DATA_PATH.iterdir()))


 # Criei um pipeline inicial em Python para validar e carregar múltiplos datasets de um 
 # e-commerce real, garantindo estrutura e reprodutibilidade do projeto.