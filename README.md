# smart-hr-analytics
# Smart HR Analytics System 🇲🇦

> Plateforme décisionnelle RH complète — Data Warehouse SQL Server,
> pipeline ETL Medallion (Bronze/Silver/Gold), dashboards Power BI
> et assistant IA RAG pour DRH.

## Stack
![Python](https://img.shields.io/badge/Python-3.11-blue)
![SQL Server](https://img.shields.io/badge/SQL_Server-2019-red)
![Power BI](https://img.shields.io/badge/Power_BI-Dashboard-yellow)
![MLflow](https://img.shields.io/badge/MLflow-Tracking-blue)

## Architecture
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
