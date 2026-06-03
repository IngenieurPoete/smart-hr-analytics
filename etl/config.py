import pathlib
# ── Connexion SQL Server ──────────────────────────────────────────
CONNECTION_STRING = (
    "DRIVER={ODBC Driver 17 for SQL Server};"
    "SERVER=INGABOU\\SQLEXPRESS;"
    "DATABASE=SmartHR_DW;"
    "Trusted_Connection=yes;"
)

# ── Répertoires ─────────────────────────────────────────────────────
BASE_DIR = pathlib.Path(__file__).parent.parent
#chemin absolu du dossier data/raw
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
