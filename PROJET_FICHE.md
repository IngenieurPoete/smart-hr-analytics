# Smart HR Analytics System
### Fiche de Projet — CI2 IA & BI-DS | ISMAGI Maroc

---

## 1. Contexte & Importance

Les départements RH des entreprises marocaines — PME comme grandes structures — gèrent encore aujourd'hui une masse considérable d'informations dans des fichiers Excel dispersés, sans vision consolidée ni outils d'aide à la décision. Le résultat est systématiquement le même : des décisions prises trop tard, sur intuition, sans données fiables.

Les conséquences sont mesurables et coûteuses :
- Un taux de turnover élevé détecté *après* que les départs ont eu lieu
- Des pics d'absentéisme récurrents jamais anticipés
- Une masse salariale mal maîtrisée par faute de vision transversale
- Des DRH qui passent plus de temps à consolider des tableaux qu'à analyser et décider

Ce projet répond à un besoin réel, documenté, et croissant sur le marché marocain : **donner aux équipes RH les outils qu'elles méritent.**

---

## 2. Mission du Projet

Concevoir et déployer une plateforme décisionnelle RH complète combinant :
- Un **Data Warehouse structuré** alimenté automatiquement
- Des **dashboards Power BI** actionnables pour les DRH
- Un **modèle prédictif** de risque de départ (turnover)
- Un **assistant IA conversationnel** (RAG) permettant d'interroger les données RH en langage naturel

Le tout déployé avec des pratiques MLOps professionnelles : versioning, CI/CD, tests automatisés, containerisation Docker.

---

## 3. Problème Résolu

| Problème actuel | Solution apportée |
|---|---|
| Données RH éparpillées dans des Excel | Data Warehouse centralisé (SQL Server) |
| Aucune vision du taux d'absentéisme | Dashboard Power BI avec alertes par département |
| Départs d'employés non anticipés | Modèle ML de scoring de risque de départ |
| DRH incapable d'interroger ses données sans technicien | Chatbot RAG en langage naturel |
| Aucune traçabilité des analyses | MLflow + DVC + GitHub Actions |

**La valeur ajoutée en une phrase :**
> Un DRH sans compétence technique peut désormais poser la question *"Quels employés risquent de partir ce trimestre dans le département commercial ?"* et obtenir une réponse immédiate, fiable, et traçable.

---

## 4. Stack Technique Mobilisée

```
Données          → Python (POO), Faker, Pandas, NumPy
Qualité données  → Great Expectations
ETL & DW         → SSIS, SQL Server Express, SSAS (cubes OLAP)
Machine Learning → scikit-learn, MLflow
BI & Reporting   → Power BI Desktop (DAX, modèle en étoile)
IA & RAG         → LangChain, ChromaDB, FastAPI
DevOps           → Docker, GitHub Actions, DVC, Pytest
IDE & Versioning → VS Code, Git, GitHub
```

---

## 5. Architecture Globale

```
[Sources CSV] 
      ↓ Python ETL (POO) + SSIS
[Data Warehouse SQL Server]
   ├── Dim_Employe
   ├── Dim_Temps
   ├── Dim_Departement
   ├── Dim_Poste
   ├── Fact_Absences
   ├── Fact_Paie
   └── Fact_Evaluations
      ↓
[SSAS — Cubes OLAP] ──→ [Power BI Dashboards]
      ↓
[MLflow — Modèle Scoring Turnover] ──→ [FastAPI]
      ↓
[LangChain + ChromaDB — RAG] ──→ [Chatbot DRH]
      ↓
[Docker + GitHub Actions — Déploiement CI/CD]
```

---

## 6. Questions Métier Auxquelles le Projet Répond

| # | Question | Réponse apportée par |
|---|---|---|
| Q1 | Quel département a le taux d'absentéisme le plus élevé ce trimestre ? | Power BI |
| Q2 | Quels profils d'employés sont les plus à risque de quitter l'entreprise ? | Modèle MLflow |
| Q3 | Comment évolue la masse salariale par poste sur 12 mois ? | Power BI + DW |
| Q4 | Quels sont les pics d'absence par saison et par ancienneté ? | Power BI + SSAS |
| Q5 | "Montre-moi les employés absents +10j ce mois dans le commercial" | Chatbot RAG |

---

## 7. Roadmap — Cheminement Semaine par Semaine

### ✅ SEMAINE 1 — Setup & Données (EN COURS)

**Objectif :** Poser les fondations solides du projet.

**Déjà accompli :**
- [x] Choix et validation de l'idée projet
- [x] Définition des 5 questions métier
- [x] Création de l'arborescence du projet (`data/`, `etl/`, `dw/`, `ml/`, `rag/`, `powerBi/`, `tests/`, `docker/`, `docs/`, `.github/`)
- [x] Initialisation Git + push GitHub
- [x] Création et activation environnement Conda `smart-hr` (Python 3.11)
- [x] Installation des dépendances (`requirements.txt`)
- [x] Création du générateur de données RH marocain (`data/generate_hr_data.py`)
  - Classes POO : `EmployeeGenerator`, `AbsenceGenerator`
  - 200 employés générés (`employees.csv`)
  - 800 absences générées (`absences.csv`)
  - Données contextualisées Maroc (villes, salaires MAD, contrats)

**À faire cette semaine :**
- [ ] Exploration des datasets générés (statistiques descriptives)
- [ ] Génération du dataset `payroll.csv` (historique paie mensuelle)
- [ ] Génération du dataset `evaluations.csv` (évaluations annuelles)
- [ ] Création `docs/architecture.md` avec schéma du DW
- [ ] Commit & push de tout sur GitHub

---

### ⬜ SEMAINE 2 — ETL Python (POO) + SSIS + Data Warehouse

**Objectif :** Alimenter le Data Warehouse avec des données propres et validées.

**Tâches :**
- [ ] Concevoir le schéma en étoile complet (tables de dimensions et de faits)
  - `Dim_Employe`, `Dim_Temps`, `Dim_Departement`, `Dim_Poste`, `Dim_Ville`
  - `Fact_Absences`, `Fact_Paie`, `Fact_Evaluations`
- [ ] Créer la base SQL Server et les tables (scripts SQL dans `dw/`)
- [ ] Écrire les classes ETL Python propres (`etl/`)
  - `DataLoader` — chargement et lecture des CSV
  - `DataTransformer` — nettoyage, typage, encodage
  - `DWLoader` — insertion dans SQL Server via pyodbc
- [ ] Configurer les pipelines SSIS (chargement incrémental)
- [ ] Great Expectations — suite de validation qualité données
- [ ] Commit & push

---

### ⬜ SEMAINE 3 — SSAS + Premières Analyses SQL

**Objectif :** Rendre les données interrogeables depuis plusieurs angles d'analyse.

**Tâches :**
- [ ] Créer les cubes OLAP SSAS (absentéisme, paie, turnover)
- [ ] Écrire les premières requêtes MDX/DAX de validation
- [ ] Vérifier la cohérence des mesures (taux absentéisme, masse salariale)
- [ ] Documenter le modèle de données dans `docs/`
- [ ] Commit & push

---

### ⬜ SEMAINE 4 — Power BI Dashboards

**Objectif :** Produire 3 rapports Power BI professionnels et actionnables.

**Tâches :**
- [ ] Connexion Power BI → SQL Server DW
- [ ] Rapport 1 : Absentéisme (taux par département, motifs, évolution)
- [ ] Rapport 2 : Turnover & Pyramide des âges / ancienneté
- [ ] Rapport 3 : Masse salariale (évolution, répartition par poste)
- [ ] Mesures DAX avancées (taux, moyennes mobiles, comparaisons N-1)
- [ ] Mise en page professionnelle, slicers, alertes visuelles
- [ ] Export `.pbix` dans `powerBi/`
- [ ] Commit & push

---

### ⬜ SEMAINE 5 — Machine Learning + MLflow

**Objectif :** Construire et tracker un modèle de prédiction de risque de départ.

**Tâches :**
- [ ] Feature engineering (ancienneté, taux absence, salaire relatif, évaluation)
- [ ] Entraîner plusieurs modèles (RandomForest, LogisticRegression, XGBoost)
- [ ] Tracker toutes les expériences dans MLflow (paramètres, métriques, artefacts)
- [ ] Sélectionner et enregistrer le meilleur modèle
- [ ] Exposer le scoring via FastAPI (`/predict`)
- [ ] Tests Pytest sur les fonctions de feature engineering
- [ ] Commit & push

---

### ⬜ SEMAINE 6 — Pipeline RAG + Chatbot DRH

**Objectif :** Permettre à un DRH d'interroger ses données en langage naturel.

**Tâches :**
- [ ] Préparer les documents de contexte RH pour ChromaDB
- [ ] Configurer le pipeline LangChain (retriever + LLM)
- [ ] Développer l'API FastAPI du chatbot (`rag/`)
- [ ] Tester les 5 questions métier via le chatbot
- [ ] Dockeriser l'application (`docker/`)
- [ ] Commit & push

---

### ⬜ SEMAINE 7 — CI/CD + Finitions + Présentation

**Objectif :** Rendre le projet présentable à un recruteur ou jury.

**Tâches :**
- [ ] Configurer GitHub Actions (tests auto à chaque push)
- [ ] DVC — versioning des datasets et modèles
- [ ] README.md professionnel avec badges, screenshots, instructions
- [ ] `docs/architecture.md` complet avec diagrammes
- [ ] Vidéo de démo (3 min : DW → Power BI → Chatbot RAG)
- [ ] Slides de présentation recruteur (10 slides max)
- [ ] Commit final & tag `v1.0.0`

---

## 8. Livrables Finaux

| Livrable | Description |
|---|---|
| Repo GitHub public | Code complet, documenté, avec historique Git propre |
| Data Warehouse | SQL Server, schéma en étoile, scripts reproductibles |
| Dashboards Power BI | 3 rapports `.pbix` connectés au DW |
| Modèle MLflow | Expériences trackées, modèle versionné, API scoring |
| Chatbot RAG | Interface FastAPI, réponses en langage naturel |
| Docker | Application containerisée, déployable en une commande |
| Documentation | Architecture, README, guide d'utilisation |
| Vidéo démo | Présentation end-to-end de 3 minutes |

---

## 9. Ce que ce Projet Démontre à un Recruteur

- **Pensée système :** capacité à concevoir une architecture bout en bout
- **Rigueur data :** validation, versioning, tests — pas juste un notebook
- **Compétences BI :** modélisation dimensionnelle + DAX + Power BI
- **MLOps :** MLflow, CI/CD, Docker — pratiques professionnelles
- **IA appliquée :** RAG sur données métier réelles — compétence rare
- **Sens métier :** le projet répond à un vrai problème RH, mesurable

---

*Document vivant — mis à jour à chaque fin de sprint.*  
*Auteur : [Ton Nom] | ISMAGI CI2 IA & BI-DS | 2026*
