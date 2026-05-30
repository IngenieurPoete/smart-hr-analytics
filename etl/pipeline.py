"""
Pipeline ETL complet — Bronze → Silver → Gold
Lance les 3 couches dans l'ordre.
"""
import warnings
warnings.filterwarnings("ignore", category=UserWarning)

from bronze_loader import BronzeLoader
from silver_transformer import SilverTransformer
from gold_loader import GoldLoader
from config import CONNECTION_STRING, DATA_RAW_DIR


def run_pipeline() -> None:
    print("=" * 50)
    print("  SMART HR ANALYTICS — ETL PIPELINE")
    print("=" * 50)

    # ── Couche Bronze ─────────────────────────
    bronze = BronzeLoader(CONNECTION_STRING, DATA_RAW_DIR)
    bronze.connect()
    bronze.run()
    bronze.disconnect()

    # ── Couche Silver ─────────────────────────
    silver = SilverTransformer(CONNECTION_STRING)
    silver.connect()
    silver.run()
    silver.disconnect()

    # ── Couche Gold ───────────────────────────
    gold = GoldLoader(CONNECTION_STRING)
    gold.connect()
    gold.run()
    gold.disconnect()

    print("=" * 50)
    print("  PIPELINE TERMINÉ AVEC SUCCÈS")
    print("=" * 50)


if __name__ == "__main__":
    run_pipeline()