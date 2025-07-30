from datetime import datetime
from config.database import DatabaseConfig

class LogsService:
    
    @staticmethod
    def get_logs(exchange_name):
        """Fetch logs data for the specified exchange"""
        conn = DatabaseConfig.get_db_connection(exchange_name)
        cursor = conn.cursor()

        try:
            # Fetch column names dynamically
            cursor.execute("PRAGMA table_info(logs)")
            columns = [column[1] for column in cursor.fetchall()]

            # Validate required columns
            if 'timestamp' not in columns:
                raise ValueError("'timestamp' column is missing in the logs table")

            # Query all logs data in descending order
            query = "SELECT * FROM logs ORDER BY timestamp DESC"
            cursor.execute(query)
            rows = cursor.fetchall()

            if not rows:
                return []

            # Format the response
            response_data = []
            for row in rows:
                log_entry = {}
                for idx, column in enumerate(columns):
                    if column == 'timestamp':
                        # Format timestamp to "YYYY-MM-DD HH:MM"
                        log_entry[column] = datetime.strptime(
                            row[idx], "%Y-%m-%d %H:%M:%S"
                        ).strftime("%Y-%m-%d %H:%M")
                    else:
                        log_entry[column] = row[idx]
                response_data.append(log_entry)

            return response_data

        finally:
            conn.close()