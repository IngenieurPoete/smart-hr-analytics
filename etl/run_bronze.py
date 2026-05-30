"""
Lance le chargement Bronze — CSV vers bronze.*
"""
from bronze_loader import BronzeLoader
from config import CONNECTION_STRING, DATA_RAW_DIR

if __name__ == "__main__":
    loader = BronzeLoader(
        connection_string=CONNECTION_STRING,
        data_dir=DATA_RAW_DIR
    )
    try:
        loader.connect()
        loader.run()
    finally:
        loader.disconnect()