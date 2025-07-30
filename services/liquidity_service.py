import sqlite3
from config.database import DatabaseConfig

class LiquidityService:
    
    @staticmethod
    def calculate_liquidity(fiat_table, payment_methods, exchange_name):
        """Calculate liquidity for given payment methods and fiat table"""
        conn = DatabaseConfig.get_db_connection(exchange_name)
        cursor = conn.cursor()
        
        # Query to fetch relevant data from the exchange's database
        query = f"""
        SELECT price, available_amount, payment_methods
        FROM {fiat_table}
        """
        
        try:
            cursor.execute(query)
            rows = cursor.fetchall()
        except sqlite3.OperationalError as e:
            conn.close()
            raise ValueError(f"Table '{fiat_table}' does not exist in the database.")
        finally:
            conn.close()
        
        total_liquidity = 0
        weighted_price_sum = 0
        
        for row in rows:
            price, available_amount, methods = row
            methods_set = set(method.strip() for method in methods.split(","))
            
            processed = False
            
            # Check if 'Bank Transfer' is in payment methods
            if "Bank Transfer" in payment_methods:
                if any("bank" in method.lower() for method in methods_set):
                    if not processed:
                        total_liquidity += available_amount
                        weighted_price_sum += price * available_amount
                        processed = True
            
            # Handle other payment methods independently
            if not processed and methods_set.intersection(payment_methods):
                total_liquidity += available_amount
                weighted_price_sum += price * available_amount
                processed = True

        vwap = weighted_price_sum / total_liquidity if total_liquidity > 0 else 0

        return {
            "specific_liquidity": f"{total_liquidity:.2f}", 
            "specific_vwap": f"{vwap:.2f}"
        }
    
    @staticmethod
    def get_fiat_table_by_country(country):
        """Get fiat table name from country name"""
        COUNTRY_TO_FIAT = DatabaseConfig.load_country_fiat_mapping()
        
        for fiat, mapped_country in COUNTRY_TO_FIAT.items():
            if mapped_country.lower() == country.lower():
                return fiat
        
        return None