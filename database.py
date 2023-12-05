import mysql.connector

class Database:
    def __init__(self):
        self.response401 = 'Authorization denied.'
        self.db_config = {
            'user': 'careintelligence',
            'password': 'XX',
            'host': 'careintelligencedev.crpv6quhydmn.sa-east-1.rds.amazonaws.com',
            'database': 'careintelligencedev'
        }

    def query_notification(self, target_id: str):
        return f"SELECT * FROM notifications WHERE target_id='{target_id}' AND notification_status=0"
    
    def query_pharmacies(self, uf: str):
        return f"SELECT * FROM farmacias WHERE uf='{uf}'"

    def close_connection(self):
        self.cursor.close()
        self.conn.close()

    def select_by_query(self, query: str, columns: list[str]):
        try:
            self.conn = mysql.connector.connect(**self.db_config)
            self.cursor = self.conn.cursor(dictionary=True, buffered=True)
            self.cursor.execute(query)

            results = self.cursor.fetchall()
            self.close_connection()
            response = {'success': False, 'data': results}

            if(len(columns) > 0 ):
                if results is not None:
                    response = {
                        'success': results is not None and len(results) > 0,
                        'data': results
                    }
            else:
                response = {
                    'success': results is not None and len(results) > 0,
                    'data': results
                }
          
            return response
        except Exception as err:
            print("Erro ao realizar query:", err)
            return {
                'success': False,
                'data': None
            }