import sqlite3
import json
import os

class DatabaseConfig:
    DATABASE_PATH = "database"
    
    @staticmethod
    def get_db_connection(exchange_name):
        """Get database connection for specified exchange"""
        db_path = os.path.join(DatabaseConfig.DATABASE_PATH, f"{exchange_name}_data.db")
        if not os.path.exists(db_path):
            raise FileNotFoundError(f"Database file not found: {db_path}")
        return sqlite3.connect(db_path)
    
    @staticmethod
    def load_country_fiat_mapping(exchange_name):
        """Load country-to-fiat mapping from the exchange-specific JSON file"""
        fiat_mapping_file = os.path.join(DatabaseConfig.DATABASE_PATH, exchange_name, "fiat2country.json")
        try:
            with open(fiat_mapping_file, "r") as f:
                return json.load(f)
        except FileNotFoundError:
            raise FileNotFoundError(f"Fiat mapping file not found: {fiat_mapping_file}")
        except json.JSONDecodeError:
            raise ValueError("Invalid JSON format in fiat mapping file")
    
    @staticmethod
    def get_supported_exchanges():
        """Get list of supported exchanges based on available database files"""
        exchanges = []
        if os.path.exists(DatabaseConfig.DATABASE_PATH):
            for file in os.listdir(DatabaseConfig.DATABASE_PATH):
                if file.endswith("_data.db"):
                    exchange_name = file.replace("_data.db", "")
                    exchanges.append(exchange_name)
        return exchanges