USE SmartHR_DW;
GO

-- ── Bronze : copie exacte des CSV, aucune transformation ──────────
CREATE TABLE bronze.employees (
    employee_id         VARCHAR(20),
    nom                 VARCHAR(100),
    departement         VARCHAR(100),
    poste               VARCHAR(100),
    ville               VARCHAR(100),
    contrat             VARCHAR(50),
    salaire_mad         VARCHAR(20),   -- VARCHAR volontaire : on ne fait
    date_embauche       VARCHAR(20),   -- confiance à rien en Bronze.
    date_naissance      VARCHAR(20),   -- Les types seront validés en Silver.
    actif               VARCHAR(5),
    genre               VARCHAR(5),
    anciennete_annees   VARCHAR(10)
);

CREATE TABLE bronze.absences (
    absence_id      VARCHAR(20),
    employee_id     VARCHAR(20),
    departement     VARCHAR(100),
    ville           VARCHAR(100),
    motif           VARCHAR(100),
    date_debut      VARCHAR(20),
    date_fin        VARCHAR(20),
    nb_jours        VARCHAR(10)
);

CREATE TABLE bronze.payroll (
    payroll_id      VARCHAR(20),
    employee_id     VARCHAR(20),
    departement     VARCHAR(100),
    poste           VARCHAR(100),
    mois            VARCHAR(10),
    salaire_base    VARCHAR(20),
    salaire_verse   VARCHAR(20),
    prime           VARCHAR(20)
);

CREATE TABLE bronze.evaluations (
    eval_id                 VARCHAR(20),
    employee_id             VARCHAR(20),
    departement             VARCHAR(100),
    annee                   VARCHAR(10),
    score                   VARCHAR(5),
    mention                 VARCHAR(50),
    recommande_promotion    VARCHAR(5)
);

PRINT 'Tables Bronze créées.';
GO