"""
ETL Couche Bronze — Chargement brut des CSV vers SQL Server.
Aucune transformation. Fidélité totale à la source.
"""

import pandas as pd
import pyodbc
from pathlib import Path


class BronzeLoader:
    """
    Charge les fichiers CSV bruts dans les tables bronze.*
    Principe : copie exacte, aucun jugement sur les données.
    """

    def __init__(self, connection_string: str, data_dir: str = "data/raw"):
        self.conn_str = connection_string
        self.data_dir = Path(data_dir)
        self.conn = None

    def connect(self) -> None:
        """Établit la connexion à SQL Server."""
        self.conn = pyodbc.connect(self.conn_str)
        print("✓ Connexion SQL Server établie")

    def disconnect(self) -> None:
        """Ferme proprement la connexion."""
        if self.conn:
            self.conn.close()
            print("✓ Connexion fermée")

    def _truncate_table(self, table: str) -> None:
        """Vide la table avant rechargement (idempotence)."""
        cursor = self.conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table}")
        self.conn.commit()

    def _load_csv_to_table(self, filename: str, table: str) -> int:
        """
        Charge un CSV vers une table Bronze.
        Retourne le nombre de lignes insérées.
        """
        filepath = self.data_dir / filename

        if not filepath.exists():
            raise FileNotFoundError(f"Fichier introuvable : {filepath}")

        # Tout en string — Bronze ne caste rien
        df = pd.read_csv(filepath, dtype=str).fillna("")

        self._truncate_table(table)

        cursor = self.conn.cursor()
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["?" for _ in df.columns])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"

        cursor.fast_executemany = True
        cursor.executemany(sql, df.values.tolist())
        self.conn.commit()

        return len(df)

    def run(self) -> None:
        """Point d'entrée : charge tous les CSV en Bronze."""
        print("\n── Chargement Bronze ──────────────────────────")

        fichiers = {
            "employees.csv":   "bronze.employees",
            "absences.csv":    "bronze.absences",
            "payroll.csv":     "bronze.payroll",
            "evaluations.csv": "bronze.evaluations",
        }

        total = 0
        for fichier, table in fichiers.items():
            n = self._load_csv_to_table(fichier, table)
            print(f"  ✓ {table:<30} {n:>5} lignes")
            total += n

        print(f"\n  Total : {total} lignes chargées en Bronze")
        print("───────────────────────────────────────────────\n")