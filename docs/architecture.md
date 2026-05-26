# Architecture du Data Warehouse RH

## Schéma en étoile

### Tables de Dimensions
| Table | Clé | Attributs principaux |
|---|---|---|
| Dim_Employe | employe_sk | employee_id, nom, genre, ville, contrat |
| Dim_Temps | temps_sk | date, mois, trimestre, annee, semaine |
| Dim_Departement | departement_sk | nom_departement |
| Dim_Poste | poste_sk | nom_poste |

### Tables de Faits
| Table | Granularité | Mesures |
|---|---|---|
| Fact_Absences | 1 ligne = 1 absence | nb_jours |
| Fact_Paie | 1 ligne = 1 mois × 1 employé | salaire_base, salaire_verse, prime |
| Fact_Evaluations | 1 ligne = 1 évaluation annuelle | score, recommande_promotion |