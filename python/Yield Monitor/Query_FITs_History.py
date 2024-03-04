import pyodbc

class QueryFITsHistory():
    def SN_FITs_In(self, UUT_SN_in):
        file = open("temp/CODE (FITs)(History).txt", "r")
        file_read = file.read()

        server = 'FITS-026,14000'
        database = 'dbAcacia_VW'
        username = 'ACACIA_USER'
        password = 'User@cac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        SQL_Conn_by_SN = pyodbc.connect(conn_str)
        cursor_by_SN = SQL_Conn_by_SN.cursor()
        # print(file_read + UUT_SN_in + "')" + "\nand sn_attr_code in ('410001')" + "\norder by VW.date_time desc")
        cursor_by_SN.execute(file_read + UUT_SN_in + "')" + "\nand sn_attr_code in ('410001','810001','30001','9800','710001')" + "\norder by VW.date_time desc")          
        DATA_Queried = cursor_by_SN.fetchall()

        SQL_Conn_by_SN.close()
        file.close()

        return DATA_Queried