import pyodbc

class QueryResultTestSN():
    def SN_In(self, UUT_SN_in, TAB_Name, day_mode, day):
        file_read = ""
        if TAB_Name == "AC100M":
            file = open("temp/CODE (Non-AC1200)(by SN).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC200":
            file = open("temp/CODE (Non-AC1200)(by SN).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC400":
            file = open("temp/CODE (Non-AC1200)(by SN).txt", "r")
            file_read = file.read()          
        else:
            file = open("temp/CODE (by SN).txt", "r")
            file_read = file.read()
        
        if day_mode == True:
            code_date = f"')\nand VD.START_DATE_TIME > getdate() - {day}"
        else:
            code_date = f"')\n--and VD.START_DATE_TIME > getdate() - {day}"

        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        SQL_Conn_by_SN = pyodbc.connect(conn_str)
        cursor_by_SN = SQL_Conn_by_SN.cursor()
        cursor_by_SN.execute(file_read + UUT_SN_in + code_date + "\nand VD.STATION_ID not like ('%fb%') \nand VD.STATION_ID not like ('%siph%')" + "\nand VD.TPS_NAME not like ('%ATE%') order by VD.START_DATE_TIME desc")          
        DATA_Query_by_SN = cursor_by_SN.fetchall()
        
        SQL_Conn_by_SN.close()
        file.close()

        return DATA_Query_by_SN