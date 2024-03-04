import pyodbc

class QueryFITsOperation():
    def Detail_FITs_In(self, UUT_SN_in, Operation_ID, DateTime):
        file = open("temp/CODE (FITs)(Operation).txt", "r")
        file_read = file.read()
        
        server = 'FITS-026,14000'
        database = 'dbAcacia_VW'
        username = 'ACACIA_USER'
        password = 'User@cac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        SQL_Conn_by_SN = pyodbc.connect(conn_str)
        cursor_by_SN = SQL_Conn_by_SN.cursor()
        # print(file_read + str(UUT_SN_in) + "')\nand operation in ('" + str(Operation_ID) + "')\nand convert(varchar, date_time, 22) ('" + str(DateTime) + "')\norder by date_time desc")
        cursor_by_SN.execute(file_read + str(UUT_SN_in) + "')\nand operation in ('" + str(Operation_ID) + "')\nand convert(varchar, date_time, 22) in ('" + str(DateTime) + "')\norder by date_time desc")          
        DATA_Queried = cursor_by_SN.fetchall()

        SQL_Conn_by_SN.close()
        file.close()

        return DATA_Queried