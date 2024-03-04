import pyodbc

class FITsLINECARDCount:
    def input_data(self, LINECARD_SN):
        server = 'FITS-026,14000'
        database = 'dbAcacia_VW'
        username = 'ACACIA_USER'
        password = 'User@cac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        SQL_Conn_by_SN = pyodbc.connect(conn_str)
        cursor_by_SN = SQL_Conn_by_SN.cursor()
        code_query = f"SELECT [Line Card Serial Number],[Usage Counts],[Remaining Usage],[Rework Counts] \nFROM [dbAcacia].[dbo].[tb_line_card_usage_module]\n  Where [Line Card Serial Number] = '{LINECARD_SN}'"
        cursor_by_SN.execute(code_query)          
        DATA_Queried = cursor_by_SN.fetchall()

        SQL_Conn_by_SN.close()

        return DATA_Queried[0]
        