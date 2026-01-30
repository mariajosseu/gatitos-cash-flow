import os
import pandas as pd


DATA_PATH = os.path.join(os.path.dirname(__file__), 'gastos')


def read_expenses_files():
    """List all files in the gastos directory, recursively."""
    expenses_dataframes = []
    for root, _, files in os.walk(DATA_PATH):
        for file in files:
            if file.endswith('.xlsx'):
                expenses_dataframes.append(read_expenses_file(os.path.join(DATA_PATH, root, file)))
    return pd.concat(expenses_dataframes)


def read_expenses_file(path: str) -> pd.DataFrame:
    """Read a single expenses file and return as a DataFrame."""
    columns = ["Fecha", "Detalle", "Categoría", "Tipo", "Pagado por", "Monto USD", "Monto CLP", "Monto Neto"]
    df = pd.read_excel(os.path.join(DATA_PATH, path), skiprows=3)[columns]
    df = df.dropna(subset=["Fecha"])
    return df


def process_expenses(df: pd.DataFrame) -> pd.DataFrame:
    basic_categories = ["Transporte", "Arriendo", "Comida"]
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Gasto Básico"] = df["Categoría"].apply(lambda category: category in basic_categories)
    df["Año-Mes"] = df["Fecha"].dt.to_period("M")
    df["Año"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    return df


if __name__ == "__main__":
    print(DATA_PATH)
    df = read_expenses_files()
    df = process_expenses(df)
    print(df.head())
