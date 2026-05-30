"""
ETL Couche Gold — Chargement du schéma en étoile.
Silver → Dimensions → Faits (avec surrogate keys).
"""

import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import pandas as pd
import pyodbc
from datetime import date, timedelta
from config import CONNECTION_STRING


class GoldLoader:

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

    def _truncate(self, table: str) -> None:
        """
        Vide une table.
        - Faits : TRUNCATE (rapide, pas de FK sortantes)
        - Dims  : DELETE (nécessaire car référencées par les faits)
        """
        # Les dims ne peuvent pas être TRUNCATEées si des FK existent
        dims = [
            "gold.Dim_Temps", "gold.Dim_Departement",
            "gold.Dim_Poste", "gold.Dim_Ville", "gold.Dim_Employe"
        ]
        cursor = self.conn.cursor()
        if table in dims:
            cursor.execute(f"DELETE FROM {table}")
        else:
            cursor.execute(f"TRUNCATE TABLE {table}")
        self.conn.commit()

    def _read(self, table: str) -> pd.DataFrame:
        return pd.read_sql(f"SELECT * FROM {table}", self.conn)

    def _insert(self, df: pd.DataFrame, table: str) -> None:
        if df.empty:
            print(f"  ⚠ Aucune ligne à insérer — vérifier les jointures")
            return
        cursor = self.conn.cursor()
        cols = ", ".join(df.columns)
        placeholders = ", ".join(["?" for _ in df.columns])
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        cursor.fast_executemany = True
        cursor.executemany(sql, df.values.tolist())
        self.conn.commit()

    # ── Dimensions simples ────────────────────────────────────────

    def _load_dim_temps(self) -> None:
        """Génère toutes les dates entre 2022-01-01 et aujourd'hui."""
        self._truncate("gold.Dim_Temps")

        mois_fr = {
            1:"Janvier", 2:"Février", 3:"Mars", 4:"Avril",
            5:"Mai", 6:"Juin", 7:"Juillet", 8:"Août",
            9:"Septembre", 10:"Octobre", 11:"Novembre", 12:"Décembre"
        }

        start = date(2022, 1, 1)
        end   = date.today()
        records = []

        current = start
        while current <= end:
            records.append({
                "date_complete": current.strftime("%Y-%m-%d"),
                "jour":         current.day,
                "mois":         current.month,
                "nom_mois":     mois_fr[current.month],
                "trimestre":    (current.month - 1) // 3 + 1,
                "annee":        current.year,
                "semaine":      current.isocalendar()[1],
                "est_weekend":  1 if current.weekday() >= 5 else 0,
            })
            current += timedelta(days=1)

        df = pd.DataFrame(records)
        self._insert(df, "gold.Dim_Temps")
        print(f"  ✓ gold.Dim_Temps          {len(df):>5} lignes")

    def _load_dim_simple(self, silver_table: str, gold_table: str,
                          col_source: str, col_dest: str) -> None:
        """Charge une dimension à valeurs uniques."""
        self._truncate(f"{gold_table}")
        df_silver = self._read(silver_table)
        valeurs = df_silver[col_source].dropna().unique()
        df = pd.DataFrame({col_dest: valeurs})
        self._insert(df, gold_table)
        print(f"  ✓ {gold_table:<25} {len(df):>5} lignes")

    def _load_dim_employe(self) -> None:
        """
        Charge Dim_Employe avec logique SCD Type 2.
        Premier chargement : toutes les lignes sont 'courantes'.
        """
        self._truncate("gold.Dim_Employe") 

        df = self._read("silver.employees")

        # Récupérer les surrogate keys des dims
        dept  = self._read("gold.Dim_Departement")
        poste = self._read("gold.Dim_Poste")
        ville = self._read("gold.Dim_Ville")

        # Jointures pour obtenir les SKs
        df = df.merge(dept,  left_on="departement", right_on="nom_departement", how="left")
        df = df.merge(poste, left_on="poste",        right_on="nom_poste",       how="left")
        df = df.merge(ville, left_on="ville",         right_on="nom_ville",       how="left")

        today = date.today().strftime("%Y-%m-%d")

        result = pd.DataFrame({
            "employee_id":       df["employee_id"],
            "nom":               df["nom"],
            "genre":             df["genre"],
            "contrat":           df["contrat"],
            "date_embauche":     df["date_embauche"],
            "date_naissance":    df["date_naissance"],
            "anciennete_annees": df["anciennete_annees"],
            "actif":             df["actif"],
            "departement_sk":    df["departement_sk"],
            "poste_sk":          df["poste_sk"],
            "ville_sk":          df["ville_sk"],
            "date_debut":        today,
            "date_fin":          None,   # NULL = version courante
            "est_courant":       1,
        })

        self._insert(result, "gold.Dim_Employe")
        print(f"  ✓ gold.Dim_Employe        {len(result):>5} lignes")

    # ── Faits ─────────────────────────────────────────────────────

    def _load_fact_absences(self) -> None:
        self._truncate("gold.Fact_Absences")

        abs_df   = self._read("silver.absences")
        emp_df   = self._read("gold.Dim_Employe")[["employee_id","employe_sk"]]
        dept_df  = self._read("gold.Dim_Departement")
        temps_df = self._read("gold.Dim_Temps")[["date_complete","temps_sk"]]
        temps_df["date_complete"] = (
                pd.to_datetime(temps_df["date_complete"])
                .dt.strftime("%Y-%m-%d")
            )
        abs_df["date_debut"] = (
                pd.to_datetime(abs_df["date_debut"])
                .dt.strftime("%Y-%m-%d")
            )

        df = abs_df.merge(emp_df, on="employee_id", how="left")
        df = df.merge(
            dept_df.rename(columns={"nom_departement":"departement"}),
            on="departement", how="left"
        )
        df = df.merge(
            temps_df.rename(columns={"date_complete":"date_debut"}),
            on="date_debut", how="left"
        )

        result = pd.DataFrame({
            "employe_sk":     df["employe_sk"],
            "temps_sk_debut": df["temps_sk"],
            "departement_sk": df["departement_sk"],
            "motif":          df["motif"],
            "nb_jours":       df["nb_jours"],
        }).dropna(subset=["employe_sk","temps_sk_debut","departement_sk"])

        result["employe_sk"]     = result["employe_sk"].astype(int)
        result["temps_sk_debut"] = result["temps_sk_debut"].astype(int)
        result["departement_sk"] = result["departement_sk"].astype(int)
        result["nb_jours"]       = result["nb_jours"].astype(int)

        self._insert(result, "gold.Fact_Absences")
        print(f"  ✓ gold.Fact_Absences      {len(result):>5} lignes")


    def _load_fact_paie(self) -> None:
        self._truncate("gold.Fact_Paie")

        pay_df   = self._read("silver.payroll")
        emp_df   = self._read("gold.Dim_Employe")[["employee_id","employe_sk"]]
        dept_df  = self._read("gold.Dim_Departement")
        poste_df = self._read("gold.Dim_Poste")
        temps_df = self._read("gold.Dim_Temps")[["date_complete","temps_sk"]]

        # Normalise les deux côtés en string "YYYY-MM-DD"
        pay_df["date_complete"] = (
            pd.to_datetime(pay_df["mois"] + "-01")
            .dt.strftime("%Y-%m-%d")
        )
        temps_df["date_complete"] = (
            pd.to_datetime(temps_df["date_complete"])
            .dt.strftime("%Y-%m-%d")
        )

        df = pay_df.merge(emp_df, on="employee_id", how="left")
        df = df.merge(
            dept_df.rename(columns={"nom_departement":"departement"}),
            on="departement", how="left"
        )
        df = df.merge(
            poste_df.rename(columns={"nom_poste":"poste"}),
            on="poste", how="left"
        )
        df = df.merge(temps_df, on="date_complete", how="left")

        # Debug — à retirer après validation
        print(f"    debug — lignes avant dropna : {len(df)}")
        print(f"    debug — NaN employe_sk      : {df['employe_sk'].isna().sum()}")
        print(f"    debug — NaN temps_sk        : {df['temps_sk'].isna().sum()}")
        print(f"    debug — NaN departement_sk  : {df['departement_sk'].isna().sum()}")

        result = pd.DataFrame({
            "employe_sk":     df["employe_sk"],
            "temps_sk":       df["temps_sk"],
            "departement_sk": df["departement_sk"],
            "poste_sk":       df["poste_sk"],
            "salaire_base":   df["salaire_base"],
            "salaire_verse":  df["salaire_verse"],
            "prime":          df["prime"],
        }).dropna(subset=["employe_sk","temps_sk","departement_sk","poste_sk"])

        if result.empty:
            print("  ⚠ Fact_Paie vide — vérifier les jointures")
            return

        result["employe_sk"]     = result["employe_sk"].astype(int)
        result["temps_sk"]       = result["temps_sk"].astype(int)
        result["departement_sk"] = result["departement_sk"].astype(int)
        result["poste_sk"]       = result["poste_sk"].astype(int)

        self._insert(result, "gold.Fact_Paie")
        print(f"  ✓ gold.Fact_Paie          {len(result):>5} lignes")

    def _load_fact_evaluations(self) -> None:
        self._truncate("gold.Fact_Evaluations")

        eval_df = self._read("silver.evaluations")
        emp_df  = self._read("gold.Dim_Employe")[["employee_id","employe_sk"]]
        dept_df = self._read("gold.Dim_Departement")

        df = eval_df.merge(emp_df, on="employee_id", how="left")
        df = df.merge(
            dept_df.rename(columns={"nom_departement":"departement"}),
            on="departement", how="left"
        )

        result = pd.DataFrame({
            "employe_sk":           df["employe_sk"],
            "departement_sk":       df["departement_sk"],
            "annee":                df["annee"],
            "score":                df["score"],
            "mention":              df["mention"],
            "recommande_promotion": df["recommande_promotion"],
        }).dropna(subset=["employe_sk","departement_sk"])

        result["employe_sk"]           = result["employe_sk"].astype(int)
        result["departement_sk"]       = result["departement_sk"].astype(int)
        result["annee"]                = result["annee"].astype(int)
        result["score"]                = result["score"].astype(int)
        result["recommande_promotion"] = result["recommande_promotion"].astype(int)

        self._insert(result, "gold.Fact_Evaluations")
        print(f"  ✓ gold.Fact_Evaluations   {len(result):>5} lignes")
        
        
    def _clear_all(self) -> None:
        """
        Vide toutes les tables Gold dans l'ordre inverse des FK.
        Faits d'abord → Dim_Employe → Dims simples.
        """
        ordre_suppression = [
            "gold.Fact_Evaluations",  # faits en premier
            "gold.Fact_Paie",
            "gold.Fact_Absences",
            "gold.Dim_Employe",       # dim qui référence d'autres dims
            "gold.Dim_Departement",   # dims simples en dernier
            "gold.Dim_Poste",
            "gold.Dim_Ville",
            "gold.Dim_Temps",
        ]
        cursor = self.conn.cursor()
        for table in ordre_suppression:
            cursor.execute(f"DELETE FROM {table}")
        self.conn.commit()
        print("  ✓ Tables Gold vidées (ordre FK respecté)")

    # ── Orchestration ─────────────────────────────────────────────

    def run(self) -> None:
        print("\n── Chargement Gold ─────────────────────────────")
        self._clear_all()  
        print("  [Dimensions]")
        self._load_dim_temps()
        self._load_dim_simple("silver.employees", "gold.Dim_Departement",
                               "departement", "nom_departement")
        self._load_dim_simple("silver.employees", "gold.Dim_Poste",
                               "poste", "nom_poste")
        self._load_dim_simple("silver.employees", "gold.Dim_Ville",
                               "ville", "nom_ville")
        self._load_dim_employe()

        print("  [Faits]")
        self._load_fact_absences()
        self._load_fact_paie()
        self._load_fact_evaluations()

        print("───────────────────────────────────────────────\n")