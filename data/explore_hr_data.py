"""
Exploration rapide des datasets RH générés.
But : comprendre les données avant de concevoir le DW.
"""

import pandas as pd

def explore(filepath: str, nom: str) -> None:
    df = pd.read_csv(filepath)
    print(f"\n{'='*50}")
    print(f"  {nom}")
    print(f"{'='*50}")
    print(f"Dimensions     : {df.shape[0]} lignes × {df.shape[1]} colonnes")
    print(f"Colonnes       : {list(df.columns)}")
    print(f"\nAperçu :")
    print(df.head(3).to_string())
    print(f"\nValeurs nulles :")
    print(df.isnull().sum()[df.isnull().sum() > 0])
    print(f"\nStatistiques :")
    print(df.describe(include='all').loc[['count','unique','mean','min','max']].to_string())

if __name__ == "__main__":
    explore("data/raw/employees.csv", "EMPLOYEES")
    explore("data/raw/absences.csv",  "ABSENCES")