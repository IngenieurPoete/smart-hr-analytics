"""
Générateur de données RH simulées — contexte entreprise marocaine.
Projet : Smart HR Analytics System
Auteur : [Ton nom] — ISMAGI CI2 IA & BI-DS
"""

import pandas as pd
import numpy as np
from datetime import date, timedelta
import random
import os

# ── Reproductibilité totale ───────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)

# ── Référentiels métier marocains ─────────────────────────────────
DEPARTEMENTS = [
    "Commercial", "Ressources Humaines", "Finance & Comptabilité",
    "IT & Systèmes", "Logistique", "Direction Générale",
    "Marketing", "Juridique & Conformité"
]

POSTES = ["Assistant", "Technicien", "Analyste", "Ingénieur", "Manager", "Directeur"]

VILLES = ["Casablanca", "Rabat", "Marrakech", "Fès", "Tanger", "Agadir", "Meknès", "Oujda"]

CONTRATS = ["CDI", "CDD", "Anapec", "Intérim"]

MOTIFS_ABSENCE = [
    "Maladie", "Congé annuel", "Absence injustifiée",
    "Formation", "Congé maternité/paternité",
    "Accident de travail", "Congé sans solde"
]

# Fourchettes salariales réalistes en MAD
SALAIRES_PAR_POSTE = {
    "Assistant":  (3500,  6000),
    "Technicien": (5000,  9000),
    "Analyste":   (7000, 12000),
    "Ingénieur":  (8000, 15000),
    "Manager":    (12000, 22000),
    "Directeur":  (20000, 45000),
}


class EmployeeGenerator:
    """
    Génère un DataFrame d'employés avec des attributs RH
    réalistes dans le contexte d'une entreprise marocaine.
    """

    def __init__(self, n: int = 200):
        self.n = n

    def _generate_salary(self, poste: str) -> int:
        """Retourne un salaire aléatoire selon le poste."""
        low, high = SALAIRES_PAR_POSTE[poste]
        return random.randint(low, high)

    def generate(self) -> pd.DataFrame:
        today = date.today()
        postes = np.random.choice(POSTES, self.n)

        data = {
            "employee_id":   [f"EMP{str(i).zfill(4)}" for i in range(1, self.n + 1)],
            "nom":           [f"Employé_{i}" for i in range(1, self.n + 1)],
            "departement":   np.random.choice(DEPARTEMENTS, self.n),
            "poste":         postes,
            "ville":         np.random.choice(VILLES, self.n),
            "contrat":       np.random.choice(CONTRATS, self.n, p=[0.55, 0.25, 0.12, 0.08]),
            "salaire_mad":   [self._generate_salary(p) for p in postes],
            "date_embauche": [
                today - timedelta(days=int(np.random.exponential(scale=800)))
                for _ in range(self.n)
            ],
            "date_naissance": [
                today - timedelta(days=int(np.random.uniform(23 * 365, 55 * 365)))
                for _ in range(self.n)
            ],
            "actif": np.random.choice([1, 0], self.n, p=[0.85, 0.15]),
            "genre": np.random.choice(["M", "F"], self.n, p=[0.62, 0.38]),
        }

        df = pd.DataFrame(data)
        df["anciennete_annees"] = (
            (pd.Timestamp(today) - pd.to_datetime(df["date_embauche"])).dt.days / 365
        ).round(1)

        return df


class AbsenceGenerator:
    """
    Génère un historique d'absences sur 2 ans
    pour les employés existants.
    """

    def __init__(self, employees: pd.DataFrame, n_absences: int = 800):
        self.employees = employees
        self.n = n_absences

    def generate(self) -> pd.DataFrame:
        today = date.today()
        start = today - timedelta(days=730)
        records = []

        for i in range(self.n):
            emp = self.employees.sample(1).iloc[0]
            debut = start + timedelta(days=random.randint(0, 729))
            duree = random.randint(1, 15)

            records.append({
                "absence_id":  i + 1,
                "employee_id": emp["employee_id"],
                "departement": emp["departement"],
                "ville":       emp["ville"],
                "motif":       random.choice(MOTIFS_ABSENCE),
                "date_debut":  debut,
                "date_fin":    debut + timedelta(days=duree),
                "nb_jours":    duree,
            })

        return pd.DataFrame(records)


def save_datasets(output_dir: str = "data/raw") -> None:
    """Point d'entrée : génère et sauvegarde tous les datasets."""
    os.makedirs(output_dir, exist_ok=True)

    print("Génération des données RH...")

    emp_gen = EmployeeGenerator(n=200)
    employees = emp_gen.generate()
    employees.to_csv(f"{output_dir}/employees.csv", index=False)
    print(f"  ✓ employees.csv — {len(employees)} employés générés")

    abs_gen = AbsenceGenerator(employees=employees, n_absences=800)
    absences = abs_gen.generate()
    absences.to_csv(f"{output_dir}/absences.csv", index=False)
    print(f"  ✓ absences.csv  — {len(absences)} absences générées")

    print(f"\nDatasets disponibles dans : {output_dir}/")


if __name__ == "__main__":
    save_datasets()