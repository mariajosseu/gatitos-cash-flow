import os
import pandas as pd

from utils import CATEGORY_STANDARDIZATION, DETAIL_STANDARDIZATION, DETAIL_TO_SUBCATEGORY


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
    df["Año-Mes"] = df["Fecha"].dt.to_period("M")
    df["Año"] = df["Fecha"].dt.year
    df["Mes"] = df["Fecha"].dt.month
    # estandarizacion
    df["Detalle"] = df["Detalle"].replace(DETAIL_STANDARDIZATION)
    df["Categoría"] = df["Categoría"].replace(CATEGORY_STANDARDIZATION)
    # editar casos especiales
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Mercadito Navidad"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Aeropuerto"), "Detalle"] = "Cafe aeropuerto"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Revolut"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "UCPH"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "IKEA"), "Detalle"] = "IKEA Restaurant"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Tivoli"), "Detalle"] = "Gasoline Grill Tivoli"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Academic Books"), "Categoría"] = "Ocio"
    df.loc[(df["Categoría"] == "Comida") & (df["Detalle"] == "Normal"), "Categoría"] = "Cuidado Personal"
    df.loc[(df["Categoría"] == "Cuidado Personal") & (df["Detalle"] == "PureGym"), "Categoría"] = "Gimnasio"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Fonda"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Viaje"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Studenterhuset"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Tivoli"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Evento Navidad"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "Un Mercato"), "Categoría"] = "Salidas"
    df.loc[(df["Categoría"] == "Ocio") & (df["Detalle"] == "GitHub"), "Categoría"] = "Estudios"
    df.loc[(df["Categoría"] == "Trabajo") & (df["Detalle"] == "DHL"), "Categoría"] = "Trámites"
    df.loc[(df["Categoría"] == "Servicios") & (df["Detalle"] == "iCloud"), "Categoría"] = "Telefonía"
    df.loc[(df["Categoría"] == "Telefonía") & (df["Detalle"] == "Elgiganten"), "Categoría"] = "Tecnología"
    df.loc[(df["Categoría"] == "Telefonía") & (df["Detalle"] == "AppleCare"), "Categoría"] = "Tecnología"
    df["Subcategoría"] = df.apply(
        lambda row: DETAIL_TO_SUBCATEGORY.get(row["Categoría"], {}).get(row["Detalle"], row["Categoría"]),
        axis=1
    )

    basic_subcategories = [
        "Rejsekort", "Rejsebillet", "Swapfiets", "Arriendo", "Supermercado", "Telefonía", "Transporte"
    ]
    df["Fecha"] = pd.to_datetime(df["Fecha"])
    df["Gasto Básico"] = df["Subcategoría"].apply(lambda subcategory: subcategory in basic_subcategories)
    return df


if __name__ == "__main__":
    print(DATA_PATH)
    df = read_expenses_files()
    df = process_expenses(df)
    print(df.head())
