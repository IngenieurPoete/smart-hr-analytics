"""
ETL Couche Silver — Nettoyage et validation Bronze → Silver.
C'est ici qu'on fait confiance aux données pour la première fois.
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pandas as pd
import pyodbc
from datetime import datetime
from config import CONNECTION_STRING


class SilverTransformer:
    """
    Lit les tables Bronze, nettoie, valide,
    et charge dans les tables Silver avec les bons types.
    """

    def __init__(self, connection_string: str = CONNECTION_STRING):
        self.conn_str = connection_string
        self.conn = None

    def connect(self) -> None:
        self.conn = pyodbc.connect(self.conn_str)
        print("✓ Connexion SQL Server établie")

    def disconnect(self) -> None:
        if self.conn:
            self.conn.close()
            print("✓ Connexion fermée")

    def _read_bronze(self, table: str) -> pd.DataFrame:
        """Lit une table Bronze dans un DataFrame."""
        return pd.read_sql(f"SELECT * FROM {table}", self.conn)

    def _truncate(self, table: str) -> None:
        cursor = self.conn.cursor()
        cursor.execute(f"TRUNCATE TABLE {table}")
        self.conn.commit()

    def _insert(self, df: pd.DataFrame, table: str) -> None:
        """Insère un DataFrame dans une table Silver."""
        cursor = self.conn.cursor()
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["?" for _ in df.columns])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        cursor.fast_executemany = True
        cursor.executemany(sql, df.values.tolist())
        self.conn.commit()

    # ── Transformations par dataset ───────────────────────────────

    def _transform_employees(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Nettoie et type les employés.
        Règles métier :
        - salaire_mad doit être > 0
        - genre doit être M ou F
        - actif doit être 0 ou 1
        """
        df = df.copy()

        # Typage
        df["salaire_mad"]       = pd.to_numeric(df["salaire_mad"], errors="coerce")
        df["date_embauche"]     = pd.to_datetime(df["date_embauche"], errors="coerce")
        df["date_naissance"]    = pd.to_datetime(df["date_naissance"], errors="coerce")
        df["anciennete_annees"] = pd.to_numeric(df["anciennete_annees"], errors="coerce")
        df["actif"]             = pd.to_numeric(df["actif"], errors="coerce").astype("Int64")

        # Nettoyage
        avant = len(df)
        df = df[df["salaire_mad"] > 0]
        df = df[df["genre"].isin(["M", "F"])]
        df = df.dropna(subset=["date_embauche", "date_naissance", "salaire_mad"])
        apres = len(df)

        if avant != apres:
            print(f"    ⚠ Employees : {avant - apres} lignes rejetées")

        # Formatage dates pour SQL Server
        df["date_embauche"]  = df["date_embauche"].dt.strftime("%Y-%m-%d")
        df["date_naissance"] = df["date_naissance"].dt.strftime("%Y-%m-%d")

        return df

    def _transform_absences(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Règles métier :
        - nb_jours doit être > 0
        - date_fin doit être >= date_debut
        """
        df = df.copy()

        df["absence_id"] = pd.to_numeric(df["absence_id"], errors="coerce").astype("Int64")
        df["nb_jours"]   = pd.to_numeric(df["nb_jours"], errors="coerce").astype("Int64")
        df["date_debut"] = pd.to_datetime(df["date_debut"], errors="coerce")
        df["date_fin"]   = pd.to_datetime(df["date_fin"], errors="coerce")

        avant = len(df)
        df = df[df["nb_jours"] > 0]
        df = df[df["date_fin"] >= df["date_debut"]]
        df = df.dropna(subset=["date_debut", "date_fin"])
        apres = len(df)

        if avant != apres:
            print(f"    ⚠ Absences : {avant - apres} lignes rejetées")

        df["date_debut"] = df["date_debut"].dt.strftime("%Y-%m-%d")
        df["date_fin"]   = df["date_fin"].dt.strftime("%Y-%m-%d")

        return df

    def _transform_payroll(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Règles métier :
        - salaire_base et salaire_verse doivent être > 0
        """
        df = df.copy()

        df["payroll_id"]    = pd.to_numeric(df["payroll_id"], errors="coerce").astype("Int64")
        df["salaire_base"]  = pd.to_numeric(df["salaire_base"], errors="coerce")
        df["salaire_verse"] = pd.to_numeric(df["salaire_verse"], errors="coerce")
        df["prime"]         = pd.to_numeric(df["prime"], errors="coerce").fillna(0)

        avant = len(df)
        df = df[df["salaire_base"] > 0]
        df = df[df["salaire_verse"] > 0]
        apres = len(df)

        if avant != apres:
            print(f"    ⚠ Payroll : {avant - apres} lignes rejetées")

        return df

    def _transform_evaluations(self, df: pd.DataFrame) -> pd.DataFrame:
        """
        Règles métier :
        - score doit être entre 1 et 5
        """
        df = df.copy()

        df["eval_id"]               = pd.to_numeric(df["eval_id"], errors="coerce").astype("Int64")
        df["annee"]                 = pd.to_numeric(df["annee"], errors="coerce").astype("Int64")
        df["score"]                 = pd.to_numeric(df["score"], errors="coerce").astype("Int64")
        df["recommande_promotion"]  = pd.to_numeric(df["recommande_promotion"], errors="coerce").astype("Int64")

        avant = len(df)
        df = df[df["score"].between(1, 5)]
        apres = len(df)

        if avant != apres:
            print(f"  ⚠ Evaluations : {avant - apres} lignes rejetées")

        return df

    # ── Orchestration ─────────────────────────────────────────────

    def run(self) -> None:
        print("\n── Transformation Silver ───────────────────────")

        transformations = [
            ("bronze.employees",   "silver.employees",   self._transform_employees),
            ("bronze.absences",    "silver.absences",    self._transform_absences),
            ("bronze.payroll",     "silver.payroll",     self._transform_payroll),
            ("bronze.evaluations", "silver.evaluations", self._transform_evaluations),
        ]

        for src, dest, transform_fn in transformations:
            df_bronze = self._read_bronze(src)
            df_silver = transform_fn(df_bronze)
            self._truncate(dest)
            self._insert(df_silver, dest)
            print(f"  ✓ {dest:<30} {len(df_silver):>5} lignes")

        print("───────────────────────────────────────────────\n")