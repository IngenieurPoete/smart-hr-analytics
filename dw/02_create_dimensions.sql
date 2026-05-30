USE SmartHR_DW;
GO

-- ── Dim_Temps ─────────────────────────────────────────────────────
CREATE TABLE Dim_Temps (
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

-- ── Dim_Departement ───────────────────────────────────────────────
CREATE TABLE Dim_Departement (
    departement_sk  INT IDENTITY(1,1) PRIMARY KEY,
    nom_departement VARCHAR(100) NOT NULL UNIQUE
);

-- ── Dim_Poste ─────────────────────────────────────────────────────
CREATE TABLE Dim_Poste (
    poste_sk    INT IDENTITY(1,1) PRIMARY KEY,
    nom_poste   VARCHAR(100) NOT NULL UNIQUE
);

-- ── Dim_Ville ─────────────────────────────────────────────────────
CREATE TABLE Dim_Ville (
    ville_sk    INT IDENTITY(1,1) PRIMARY KEY,
    nom_ville   VARCHAR(100) NOT NULL UNIQUE,
    region      VARCHAR(100)
);

-- ── Dim_Employe — SCD Type 2 ──────────────────────────────────────
-- Principe : on ne modifie jamais une ligne existante.
-- Quand un attribut change (département, poste...) :
--   1. On ferme l'ancienne ligne  (date_fin = aujourd'hui, est_courant = 0)
--   2. On insère une nouvelle ligne (date_fin = NULL, est_courant = 1)
-- Résultat : l'historique complet est préservé dans le DW.
CREATE TABLE Dim_Employe (
    employe_sk          INT IDENTITY(1,1) PRIMARY KEY,
    employee_id         VARCHAR(10)  NOT NULL,   -- clé source (peut se répéter)
    nom                 VARCHAR(100) NOT NULL,
    genre               CHAR(1),
    contrat             VARCHAR(20),
    date_embauche       DATE,
    date_naissance      DATE,
    anciennete_annees   DECIMAL(5,1),
    actif               BIT          NOT NULL DEFAULT 1,
    departement_sk      INT FOREIGN KEY REFERENCES Dim_Departement(departement_sk),
    poste_sk            INT FOREIGN KEY REFERENCES Dim_Poste(poste_sk),
    ville_sk            INT FOREIGN KEY REFERENCES Dim_Ville(ville_sk),

    -- Colonnes SCD Type 2
    date_debut          DATE NOT NULL DEFAULT GETDATE(),
    date_fin            DATE NULL,        -- NULL = version actuellement active
    est_courant         BIT  NOT NULL DEFAULT 1
);

-- Index pour accélérer les recherches sur la version courante
CREATE INDEX IX_Employe_Courant
    ON Dim_Employe (employee_id, est_courant);

PRINT 'Tables de dimensions créées avec SCD Type 2 sur Dim_Employe.';
GO