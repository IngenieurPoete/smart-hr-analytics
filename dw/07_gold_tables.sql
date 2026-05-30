USE SmartHR_DW;
GO

-- ── Suppression des anciennes tables (ordre obligatoire) ──────────
-- Les faits d'abord (ils référencent les dims)
-- Les dims ensuite

IF OBJECT_ID('dbo.Fact_Evaluations', 'U') IS NOT NULL 
    DROP TABLE dbo.Fact_Evaluations;
IF OBJECT_ID('dbo.Fact_Paie', 'U') IS NOT NULL 
    DROP TABLE dbo.Fact_Paie;
IF OBJECT_ID('dbo.Fact_Absences', 'U') IS NOT NULL 
    DROP TABLE dbo.Fact_Absences;
IF OBJECT_ID('dbo.Dim_Employe', 'U') IS NOT NULL 
    DROP TABLE dbo.Dim_Employe;
IF OBJECT_ID('dbo.Dim_Ville', 'U') IS NOT NULL 
    DROP TABLE dbo.Dim_Ville;
IF OBJECT_ID('dbo.Dim_Poste', 'U') IS NOT NULL 
    DROP TABLE dbo.Dim_Poste;
IF OBJECT_ID('dbo.Dim_Departement', 'U') IS NOT NULL 
    DROP TABLE dbo.Dim_Departement;
IF OBJECT_ID('dbo.Dim_Temps', 'U') IS NOT NULL 
    DROP TABLE dbo.Dim_Temps;

PRINT 'Anciennes tables dbo supprimées.';
GO

-- ── Gold : Dimensions ─────────────────────────────────────────────

CREATE TABLE gold.Dim_Temps (
    temps_sk        INT IDENTITY(1,1) PRIMARY KEY,
    date_complete   DATE        NOT NULL UNIQUE,
    jour            INT         NOT NULL,
    mois            INT         NOT NULL,
    nom_mois        VARCHAR(20) NOT NULL,
    trimestre       INT         NOT NULL,
    annee           INT         NOT NULL,
    semaine         INT         NOT NULL,
    est_weekend     BIT         NOT NULL DEFAULT 0
);

CREATE TABLE gold.Dim_Departement (
    departement_sk  INT IDENTITY(1,1) PRIMARY KEY,
    nom_departement VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE gold.Dim_Poste (
    poste_sk    INT IDENTITY(1,1) PRIMARY KEY,
    nom_poste   VARCHAR(100) NOT NULL UNIQUE
);

CREATE TABLE gold.Dim_Ville (
    ville_sk    INT IDENTITY(1,1) PRIMARY KEY,
    nom_ville   VARCHAR(100) NOT NULL UNIQUE,
    region      VARCHAR(100)
);

CREATE TABLE gold.Dim_Employe (
    employe_sk          INT IDENTITY(1,1) PRIMARY KEY,
    employee_id         VARCHAR(10)  NOT NULL,
    nom                 VARCHAR(100) NOT NULL,
    genre               CHAR(1),
    contrat             VARCHAR(20),
    date_embauche       DATE,
    date_naissance      DATE,
    anciennete_annees   DECIMAL(5,1),
    actif               BIT          NOT NULL DEFAULT 1,
    departement_sk      INT FOREIGN KEY REFERENCES gold.Dim_Departement(departement_sk),
    poste_sk            INT FOREIGN KEY REFERENCES gold.Dim_Poste(poste_sk),
    ville_sk            INT FOREIGN KEY REFERENCES gold.Dim_Ville(ville_sk),
    date_debut          DATE NOT NULL DEFAULT GETDATE(),
    date_fin            DATE NULL,
    est_courant         BIT  NOT NULL DEFAULT 1
);

CREATE INDEX IX_Employe_Courant 
    ON gold.Dim_Employe (employee_id, est_courant);

PRINT 'Dimensions Gold créées.';
GO

-- ── Gold : Faits ──────────────────────────────────────────────────

CREATE TABLE gold.Fact_Absences (
    absence_sk      INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk      INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Employe(employe_sk),
    temps_sk_debut  INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Temps(temps_sk),
    departement_sk  INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Departement(departement_sk),
    motif           VARCHAR(100),
    nb_jours        INT NOT NULL
);

CREATE TABLE gold.Fact_Paie (
    paie_sk         INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk      INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Employe(employe_sk),
    temps_sk        INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Temps(temps_sk),
    departement_sk  INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Departement(departement_sk),
    poste_sk        INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Poste(poste_sk),
    salaire_base    DECIMAL(10,2) NOT NULL,
    salaire_verse   DECIMAL(10,2) NOT NULL,
    prime           DECIMAL(10,2) NOT NULL DEFAULT 0
);

CREATE TABLE gold.Fact_Evaluations (
    eval_sk                 INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk              INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Employe(employe_sk),
    departement_sk          INT NOT NULL FOREIGN KEY REFERENCES gold.Dim_Departement(departement_sk),
    annee                   INT NOT NULL,
    score                   INT NOT NULL CHECK (score BETWEEN 1 AND 5),
    mention                 VARCHAR(50),
    recommande_promotion    BIT NOT NULL DEFAULT 0
);

PRINT 'Faits Gold créées.';
PRINT 'Architecture Medallion complète : Bronze / Silver / Gold';
GO