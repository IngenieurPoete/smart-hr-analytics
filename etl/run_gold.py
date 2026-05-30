"""Lance le chargement Gold."""
from gold_loader import GoldLoader

if __name__ == "__main__":
    loader = GoldLoader()
    try:
        loader.connect()
        loader.run()
    finally:
        loader.disconnect()