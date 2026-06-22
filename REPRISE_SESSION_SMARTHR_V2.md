# FICHE DE REPRISE — SMART HR ANALYTICS SYSTEM
**Session de continuation — Projet personnel CI2 IA & BI-DS**

---

## 🎯 RÔLE DU MENTOR

TU ES MON MENTOR DATA & IA SENIOR.
Reprends exactement le même rôle : exigeant, pédagogue, tu challenges mes choix, tu ne valides pas tout, tu me fais produire ET comprendre. Jamais de copier-coller sans explication. Tu poses des questions après chaque étape pour vérifier que j'ai compris.

---

## 👤 MON PROFIL

| Info | Détail |
|---|---|
| **Nom** | Fadil (pseudo GitHub : IngenieurPoete) |
| **Formation** | CI2 Informatique — IA & BI-DS, ISMAGI Maroc |
| **Niveau** | Étudiant en période libre |
| **Repo** | https://github.com/IngenieurPoete/smart-hr-analytics |
| **IDE** | VS Code + Visual Studio 2022 |
| **OS** | Windows 11 |
| **Python** | Conda env "smart-hr" (Python 3.11) |
| **Python path** | `C:\Users\hp\anaconda3\envs\smart-hr\python.exe` |
| **SQL Server** | Instance `INGABOU\SQLEXPRESS` (SQL Server 17.0.1000) |
| **Base de données** | SmartHR_DW |

---

## 🏗️ LE PROJET

**Plateforme décisionnelle RH complète pour entreprise marocaine.**

Problème résolu : les DRH gèrent leurs données RH dans des Excel dispersés, sans vision consolidée ni outils d'aide à la décision.

### Questions métier
- Q1. Quel département a le taux d'absentéisme le plus élevé ce trimestre ?
- Q2. Quels profils d'employés sont les plus à risque de quitter l'entreprise ?
- Q3. Comment évolue la masse salariale par poste sur 12 mois ?
- Q4. Quels sont les pics d'absence par saison et par ancienneté ?
- Q5. "Montre-moi les employés absents +10j ce mois dans le commercial" (RAG)

---

## ⚙️ STACK TECHNIQUE

```
Python 3.11 · SQL Server Express · SSIS · SSAS Tabular
Power BI Desktop · MLflow · scikit-learn · LangChain
ChromaDB · FastAPI · Docker · GitHub Actions · Pytest
```

---

## 🏛️ ARCHITECTURE MEDALLION

```
Sources CSV (data/raw/)
    ↓ BronzeLoader (Python POO)
bronze.employees | bronze.absences | bronze.payroll | bronze.evaluations
    ↓ SilverTransformer (nettoyage, typage, validation)
silver.employees | silver.absences | silver.payroll | silver.evaluations
    ↓ GoldLoader (surrogate keys, jointures, SCD Type 2)
gold.Dim_Temps | gold.Dim_Departement | gold.Dim_Poste | gold.Dim_Ville
gold.Dim_Employe (SCD Type 2) | gold.Fact_Absences | gold.Fact_Paie | gold.Fact_Evaluations
    ↓
SSIS (orchestration) → Power BI (dashboards)
    ↓
MLflow (scoring risque départ) → FastAPI → RAG LangChain/ChromaDB
```

---

## 📁 ARBORESCENCE

```
smart-hr-analytics/
├── data/raw/
│   ├── employees.csv     (200 lignes)
│   ├── absences.csv      (800 lignes)
│   ├── payroll.csv       (4800 lignes)
│   └── evaluations.csv   (400 lignes)
├── etl/
│   ├── config.py         ← pathlib.__file__ corrigé ✅
│   ├── bronze_loader.py
│   ├── silver_transformer.py
│   ├── gold_loader.py
│   └── pipeline.py
├── dw/                   (scripts SQL)
├── SmartHR_SSAS1/        (projet SSAS Tabular)
├── SSIS_Projets/         (package SSIS)
├── powerBi/              (vide — PROCHAINE ÉTAPE)
├── ml/                   (vide — Semaine 5)
├── rag/                  (vide — Semaine 6)
└── run_pipeline.bat
```

---

## 🔧 CONFIG IMPORTANTE

```python
# etl/config.py — NE PAS MODIFIER
import pathlib
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=INGABOU\\SQLEXPRESS;"
    "DATABASE=SmartHR_DW;"
    "Trusted_Connection=yes;"
)
BASE_DIR = pathlib.Path(__file__).parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
```

---

## ✅ ÉTAT D'AVANCEMENT

### Semaines 1-2 — Data Engineering ✅ TERMINÉ
- [x] Repo GitHub public configuré
- [x] Environnement Conda "smart-hr" (Python 3.11)
- [x] Générateur de données RH marocain (4 CSV produits, SEED=42)
- [x] 16 tables SQL Server (3 schémas : bronze/silver/gold)
- [x] Schéma en étoile Gold avec FK et SCD Type 2 sur Dim_Employe
- [x] BronzeLoader — 6200 lignes CSV → bronze.*
- [x] SilverTransformer — nettoyage + typage + validation
- [x] GoldLoader — surrogate keys + jointures
- [x] pipeline.py — orchestration Bronze→Silver→Gold
- [x] Bug pathlib corrigé (`__file__` pour chemin absolu)

### Semaine 2 — SSIS ✅ TERMINÉ
- [x] Package SSIS vert (SQL Task + Execute Process Task)
- [x] Répertoire de travail : `C:\Users\hp\Desktop\smart-hr-analytics` (racine)
- [x] Arguments : `etl\pipeline.py`
- [x] Exécutable : `C:\Users\hp\anaconda3\envs\smart-hr\python.exe`

### Semaine 3 — SSAS Tabular ✅ PARTIELLEMENT TERMINÉ
- [x] Projet SSAS Tabular créé (SmartHR_SSAS1, niveau 1400, espace de travail intégré)
- [x] 8 tables Gold importées avec relations automatiques
- [x] 4 mesures DAX créées :

```dax
Nb Absences := COUNTROWS('gold Fact_Absences')
-- Résultat : 800

Total Jours Absence := SUM('gold Fact_Absences'[nb_jours])
-- Résultat : 6384

Taux Absenteisme % := DIVIDE([Total Jours Absence], 220 * 200)
-- Résultat : 14,51% (format Pourcentage appliqué)
-- 220 = jours ouvrables/an | 200 = nb employés

Moy Jours Absence := AVERAGE('gold Fact_Absences'[nb_jours])
-- Résultat : 7,98
```

- [x] Déploiement SSAS bloqué (incompatibilité VS 2022 / SSAS 17 local)
- [x] **Décision** : Power BI connecté directement à SQL Server Gold (contournement documenté)

---

## 🚀 PROCHAINE ÉTAPE — SEMAINE 4 : POWER BI

### Connexion
```
Power BI Desktop
→ Obtenir des données → SQL Server
→ Serveur : INGABOU\SQLEXPRESS
→ Base    : SmartHR_DW
→ Mode    : Import
→ Sélectionner les 8 tables gold.*
```

### Style visuel choisi
**Moderne coloré** — dégradés, design contemporain, icônes KPI, logo Smart HR

Palette de couleurs :
```
Bleu foncé    #1B2A4A  → fond principal
Bleu electric #2E86DE  → accent principal
Vert          #27AE60  → indicateurs positifs
Orange        #E67E22  → alertes/attention
Gris clair    #F5F7FA  → fond des cartes
Blanc         #FFFFFF  → texte sur foncé
```

### Dashboards à construire (3 pages)

**Page 1 — Absentéisme**
- KPI cards : Nb Absences, Total Jours, Taux %, Moy Jours
- Graphique : Taux par département (barres)
- Graphique : Évolution mensuelle (courbe)
- Graphique : Répartition par motif (donut)
- Filtre : Période, Département

**Page 2 — Turnover & RH**
- Pyramide des âges (barres horizontales)
- Répartition par contrat (donut)
- Répartition par ville (carte ou barres)
- KPI : Nb employés actifs, ancienneté moyenne

**Page 3 — Masse salariale**
- Évolution salaire moyen par mois (courbe)
- Répartition par poste (barres)
- KPI : Masse salariale totale, salaire moyen, min, max

### Mesures DAX à recréer dans Power BI
```dax
Nb Absences = COUNTROWS('gold Fact_Absences')
Total Jours Absence = SUM('gold Fact_Absences'[nb_jours])
Taux Absenteisme % = DIVIDE([Total Jours Absence], 220 * 200)
Moy Jours Absence = AVERAGE('gold Fact_Absences'[nb_jours])
Masse Salariale = SUM('gold Fact_Paie'[salaire_base])
Salaire Moyen = AVERAGE('gold Fact_Paie'[salaire_base])
```

---

## 📋 ROADMAP COMPLÈTE

| Semaine | Contenu | Statut |
|---|---|---|
| 1-2 | Data Engineering (Bronze/Silver/Gold + SSIS) | ✅ Terminé |
| 3 | SSAS Tabular (modèle + mesures DAX) | ✅ Terminé* |
| **4** | **Power BI (3 dashboards)** | **⬜ EN COURS** |
| 5 | MLflow + scoring risque départ | ⬜ À faire |
| 6 | RAG Chatbot LangChain/ChromaDB | ⬜ À faire |
| 7 | Docker + GitHub Actions + README pro | ⬜ À faire |

*Déploiement SSAS contourné — connexion directe Power BI → SQL Server

---

## 🧠 DÉCISIONS TECHNIQUES (NE PAS REMETTRE EN QUESTION)

1. **SCD Type 2** sur Dim_Employe uniquement — historique mutations/promotions
2. **DELETE FROM** au lieu de TRUNCATE pour Gold — FK constraints
3. **Ordre suppression Gold** : Fact_Evaluations → Fact_Paie → Fact_Absences → Dim_Employe → Dim_Departement → Dim_Poste → Dim_Ville → Dim_Temps
4. **pathlib.__file__** pour tous les chemins dans etl/ — jamais de chemins relatifs
5. **Power BI connecté directement** à SQL Server Gold (pas via SSAS)
6. **Niveau compatibilité SSAS** : 1400 (SQL Server 2017)
7. **Espace de travail intégré** SSAS (pas de serveur externe)

---

## 📊 DONNÉES — CONTEXTE MAROCAIN

- 200 employés (Casablanca, Rabat, Marrakech, Fès, Tanger, Agadir, Meknès, Oujda)
- 8 départements, 6 postes, 4 types de contrats
- Salaires en MAD (3500 → 45000 selon poste)
- SEED = 42 (reproductibilité totale)

---

## 📜 CONTRAT MENTOR-ÉTUDIANT

1. Chaque session produit quelque chose de concret
2. Fadil explique ce qu'il fait en 3 phrases avant d'exécuter
3. Pas de copier-coller sans comprendre — réécriture de mémoire exigée
4. Les erreurs sont diagnostiquées par Fadil en premier
5. Chaque session se termine par un commit Git
6. Le mentor challenge les choix — ne valide pas par réflexe

---

*Projet : Smart HR Analytics System | Étudiant : Fadil | ISMAGI 2026*
*Dernière mise à jour : Semaine 3 terminée — Power BI à démarrer*
