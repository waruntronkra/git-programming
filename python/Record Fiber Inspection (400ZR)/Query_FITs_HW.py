import pyodbc

class QueryFITsHW:
    def input_data(self, UUT_SERIAL_NUMBER):
        server = 'FITS-026,14000'
        database = 'dbAcacia_VW'
        username = 'ACACIA_USER'
        password = 'User@cac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        code = f"SELECT [part_no] FROM [dbAcacia_VW].[dbo].[vw_event] WITH(NOLOCK) WHERE serial_no = '{UUT_SERIAL_NUMBER}' order by [date_time] desc"

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()
        for i in DATA_Query:
            if i[0] != 'n/a':
                HW = i[0]
                break

        SQL_Conn.close()

        return HW


      