import os
import re
import pandas as pd


def read_excel_or_csv(file_path):
    _, file_extension = os.path.splitext(file_path)

    if file_extension == ".csv":
        # Lecture d'un fichier CSV
        try:
            data = pd.read_csv(file_path)
            return data
        except Exception as e:
            return f"Error reading CSV file: {e}"
    elif file_extension == ".xlsx":
        # Lecture d'un fichier Excel (XLSX)
        try:
            data = pd.read_excel(file_path)
            return data
        except Exception as e:
            return f"Error reading Excel file : {e}"
    else:
        return "Please enter a .csv or .xlsx file."


def verify_product_table(data):
    if isinstance(data, pd.DataFrame):
        # Vérification des colonnes nécessaires
        required_columns = ["product_name", "Qte_unitaire"]
        if all(col in data.columns for col in required_columns):
            # Vérification des types de données
            types_check = all(
                data["product_name"].apply(lambda x: isinstance(x, str))
                and data["Qte_unitaire"].apply(lambda x: isinstance(x, float))
            )
            if types_check:
                return "La table de produits est conforme."
            else:
                return "Les types de données dans la table de produits ne correspondent pas aux critères."
        else:
            return "La table de produits ne contient pas toutes les colonnes nécessaires (product_name, Qte_unitaire)."
    else:
        return "Entrée non valide. Veuillez fournir une DataFrame (table de données)."


def verify_sales_table(data):
    if isinstance(data, pd.DataFrame):
        # Vérification des colonnes nécessaires
        required_columns = ["Date", "Quantité", "Reference"]
        if all(col in data.columns for col in required_columns):
            # Vérification des types de données et de format pour les colonnes spécifiques
            date_check = all(
                isinstance(data["Date"], pd.Series)
                and data["Date"].dtype == "datetime64[ns]"
            )
            quantity_check = all(data["Quantité"].apply(lambda x: isinstance(x, float)))
            reference_check = all(
                data["Reference"].apply(
                    lambda x: bool(re.match(r"^[A-Za-z0-9]+$", str(x)))
                )
            )

            if date_check and quantity_check and reference_check:
                return "La table de ventes est conforme."
            else:
                return "Les données dans la table de ventes ne respectent pas les critères spécifiés."
        else:
            return "La table de ventes ne contient pas toutes les colonnes nécessaires (Date, Quantité, Reference)."
    else:
        return "Entrée non valide. Veuillez fournir une DataFrame (table de données)."
