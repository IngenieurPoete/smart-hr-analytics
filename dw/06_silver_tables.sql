USE SmartHR_DW;
GO

-- ── Silver : données nettoyées, typées, validées ──────────────────
-- Ici les types sont stricts. Si une valeur arrive ici, 
-- c'est qu'elle a passé la validation Great Expectations.

CREATE TABLE silver.employees (
    employee_id         VARCHAR(10)     NOT NULL,
    nom                 VARCHAR(100)    NOT NULL,
    departement         VARCHAR(100)    NOT NULL,
    poste               VARCHAR(100)    NOT NULL,
    ville               VARCHAR(100)    NOT NULL,
    contrat             VARCHAR(20)     NOT NULL,
    salaire_mad         DECIMAL(10,2)   NOT NULL,
    date_embauche       DATE            NOT NULL,
    date_naissance      DATE            NOT NULL,
    actif               BIT             NOT NULL,
    genre               CHAR(1)         NOT NULL,
    anciennete_annees   DECIMAL(5,1)    NOT NULL,
    charge_date         DATETIME        NOT NULL DEFAULT GETDATE()
);

CREATE TABLE silver.absences (
    absence_id      INT             NOT NULL,
    employee_id     VARCHAR(10)     NOT NULL,
    departement     VARCHAR(100)    NOT NULL,
    ville           VARCHAR(100)    NOT NULL,
    motif           VARCHAR(100)    NOT NULL,
    date_debut      DATE            NOT NULL,
    date_fin        DATE            NOT NULL,
    nb_jours        INT             NOT NULL,
    charge_date     DATETIME        NOT NULL DEFAULT GETDATE()
);

CREATE TABLE silver.payroll (
    payroll_id      INT             NOT NULL,
    employee_id     VARCHAR(10)     NOT NULL,
    departement     VARCHAR(100)    NOT NULL,
    poste           VARCHAR(100)    NOT NULL,
    mois            VARCHAR(7)      NOT NULL,
    salaire_base    DECIMAL(10,2)   NOT NULL,
    salaire_verse   DECIMAL(10,2)   NOT NULL,
    prime           DECIMAL(10,2)   NOT NULL,
    charge_date     DATETIME        NOT NULL DEFAULT GETDATE()
);

CREATE TABLE silver.evaluations (
    eval_id                 INT             NOT NULL,
    employee_id             VARCHAR(10)     NOT NULL,
    departement             VARCHAR(100)    NOT NULL,
    annee                   INT             NOT NULL,
    score                   INT             NOT NULL,
    mention                 VARCHAR(50)     NOT NULL,
    recommande_promotion    BIT             NOT NULL,
    charge_date             DATETIME        NOT NULL DEFAULT GETDATE()
);

PRINT 'Tables Silver créées.';
GO