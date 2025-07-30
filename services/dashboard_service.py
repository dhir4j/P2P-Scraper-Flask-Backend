import re
from datetime import datetime
from config.database import DatabaseConfig

class DashboardService:
    
    @staticmethod
    def fetch_dashboard_data(exchange_name):
        """Fetch and format data for the dashboard"""
        conn = DatabaseConfig.get_db_connection(exchange_name)
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT date_time, country, fiat_currency, total_liquidity, 
                   volume_weighted_price, exchange_rate, spread, available_payment_methods 
            FROM dashboard
        """)
        rows = cursor.fetchall()
        conn.close()
        
        formatted_data = []
        for row in rows:
            raw_payment_methods = row[7]
            payment_methods_list = []
            date_time = row[0]
            formatted_date_time = datetime.strptime(date_time, "%Y-%m-%d %H:%M:%S").strftime("%Y-%m-%d %H:%M")
            
            for method in raw_payment_methods.split(','):
                method = method.strip()
                if '(' in method and ')' in method:
                    parts = method.split('(')
                    method_name = parts[0].strip()
                    liquidity = parts[1].split(')')[0].strip()
                    vwap = parts[2].split(')')[0].strip() if len(parts) > 2 else None
                    payment_methods_list.append({
                        "method": method_name, 
                        "liquidity": liquidity, 
                        "vwap": vwap
                    })
            
            formatted_data.append({
                "date_time": formatted_date_time,
                "country": row[1],
                "fiat_currency": row[2],
                "total_liquidity": row[3],
                "volume_weighted_price": row[4],
                "exchange_rate": row[5],
                "spread": row[6],
                "available_payment_methods": payment_methods_list
            })
        
        return formatted_data
    
    @staticmethod
    def calculate_metrics(exchange_name):
        """Calculate dashboard metrics for the given exchange"""
        conn = DatabaseConfig.get_db_connection(exchange_name)
        cursor = conn.cursor()
        cursor.execute("""
            SELECT country, total_liquidity, spread, available_payment_methods 
            FROM dashboard
        """)
        data = cursor.fetchall()
        conn.close()
        
        total_liquidity = 0
        total_spread = 0
        total_countries = set()
        unique_payment_methods = set()
        seen_payment_methods = set()

        for row in data:
            country, liquidity, spread, payment_methods = row
            total_liquidity += liquidity
            spread_value = float(re.sub(r'[^\d.]', '', spread))  # Remove % and other characters
            total_spread += spread_value
            total_countries.add(country)
            
            methods = re.findall(r'\b[\w\s]+(?:\(\d+\.\d+\))?', payment_methods)
            for method in methods:
                method_name = method.split('(')[0].strip()
                if method_name not in seen_payment_methods:
                    seen_payment_methods.add(method_name)
                    unique_payment_methods.add(method_name)
        
        avg_spread = total_spread / len(data) if data else 0

        return {
            'total_liquidity': total_liquidity,
            'average_spread': avg_spread,
            'total_countries': len(total_countries),
            'unique_payment_methods_count': len(unique_payment_methods)
        }