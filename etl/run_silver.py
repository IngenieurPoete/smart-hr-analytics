"""Lance la transformation Silver."""
from silver_transformer import SilverTransformer

if __name__ == "__main__":
    transformer = SilverTransformer()
    try:
        transformer.connect()
        transformer.run()
    finally:
        transformer.disconnect()