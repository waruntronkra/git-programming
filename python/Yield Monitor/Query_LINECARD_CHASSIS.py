import pyodbc

class QueryLINECARDCHASSIS:
    def SN_In(self, SN_LINECARD, SN_CHASSIS, TAB_Name, day):
        file_read = ""
        if TAB_Name == "AC100M":
            file = open("temp/CODE (Non-AC1200)(by LINE_CHAS).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC200":
            file = open("temp/CODE (Non-AC1200)(by LINE_CHAS).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC400":
            file = open("temp/CODE (Non-AC1200)(by LINE_CHAS).txt", "r")
            file_read = file.read()          
        else:
            file = open("temp/CODE (by LINE_CHAS).txt", "r")
            file_read = file.read()

        SN_Data = ""
        if SN_LINECARD == "" and SN_CHASSIS != "":
            SN_Data = "\nand UUT.FIXTURE2_ID in ('" + SN_CHASSIS + "')"
        elif SN_CHASSIS == "" and SN_LINECARD != "":
            SN_Data = "\nand VD.FIXTURE_ID in ('" + SN_LINECARD + "')"
        else:
            SN_Data = "\n--and UUT.FIXTURE_ID in"

        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
        
        SQL_Conn_by_SN = pyodbc.connect(conn_str)
        cursor_by_SN = SQL_Conn_by_SN.cursor()
        # print(file_read + day + SN_Data + "\norder by VD.START_DATE_TIME desc")
        cursor_by_SN.execute(file_read + day + SN_Data + "\norder by VD.START_DATE_TIME desc")          
        DATA_Query_by_SN = cursor_by_SN.fetchall()
        
        SQL_Conn_by_SN.close()
        file.close()

        return DATA_Query_by_SN