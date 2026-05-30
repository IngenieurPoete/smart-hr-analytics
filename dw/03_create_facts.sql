USE SmartHR_DW;
GO

-- ── Fact_Absences ─────────────────────────────────────────────────
-- Granularité : 1 ligne = 1 absence d'un employé
CREATE TABLE Fact_Absences (
    absence_sk      INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk      INT NOT NULL FOREIGN KEY REFERENCES Dim_Employe(employe_sk),
    temps_sk_debut  INT NOT NULL FOREIGN KEY REFERENCES Dim_Temps(temps_sk),
    departement_sk  INT NOT NULL FOREIGN KEY REFERENCES Dim_Departement(departement_sk),
    motif           VARCHAR(100),
    nb_jours        INT NOT NULL
);

-- ── Fact_Paie ─────────────────────────────────────────────────────
-- Granularité : 1 ligne = 1 mois de paie pour 1 employé
CREATE TABLE Fact_Paie (
    paie_sk         INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk      INT NOT NULL FOREIGN KEY REFERENCES Dim_Employe(employe_sk),
    temps_sk        INT NOT NULL FOREIGN KEY REFERENCES Dim_Temps(temps_sk),
    departement_sk  INT NOT NULL FOREIGN KEY REFERENCES Dim_Departement(departement_sk),
    poste_sk        INT NOT NULL FOREIGN KEY REFERENCES Dim_Poste(poste_sk),
    salaire_base    DECIMAL(10,2) NOT NULL,
    salaire_verse   DECIMAL(10,2) NOT NULL,
    prime           DECIMAL(10,2) NOT NULL DEFAULT 0
);

-- ── Fact_Evaluations ──────────────────────────────────────────────
-- Granularité : 1 ligne = 1 évaluation annuelle pour 1 employé
CREATE TABLE Fact_Evaluations (
    eval_sk                 INT IDENTITY(1,1) PRIMARY KEY,
    employe_sk              INT NOT NULL FOREIGN KEY REFERENCES Dim_Employe(employe_sk),
    departement_sk          INT NOT NULL FOREIGN KEY REFERENCES Dim_Departement(departement_sk),
    annee                   INT NOT NULL,
    score                   INT NOT NULL CHECK (score BETWEEN 1 AND 5),
    mention                 VARCHAR(50),
    recommande_promotion    BIT NOT NULL DEFAULT 0
);

PRINT 'Tables de faits créées.';
GO