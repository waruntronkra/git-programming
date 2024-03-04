import pyodbc

class QueryLineCardCount():
    def input_detail(self, SN_LC):
        server = 'FITS-026,14000'
        database = 'dbAcacia_VW'
        username = 'ACACIA_USER'
        password = 'User@cac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        code = f'''
                SELECT TOP 1 [Usage Counts]

                FROM [dbAcacia].[dbo].[tb_line_card_usage_module]
                WHERE [Line Card Serial Number] = '{SN_LC}'
                '''

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()

        SQL_Conn.close()

        return DATA_Query