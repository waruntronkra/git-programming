import pyodbc

class QueryValueLINECHAS:
    def receive_SN(self, SN_LINECARD, SN_CHASSIS, DATA_Query_by_SN_in, TAB_Name):
        file_read = ""
        if TAB_Name == "AC100M":
            file = open("temp/CODE (Non-AC1200)(LINE_CHAS)(VALUE).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC200":
            file = open("temp/CODE (Non-AC1200)(LINE_CHAS)(VALUE).txt", "r")
            file_read = file.read()
        elif TAB_Name == "AC400":
            file = open("temp/CODE (Non-AC1200)(LINE_CHAS)(VALUE).txt", "r")
            file_read = file.read()          
        else:
            file = open("temp/CODE (LINE_CHAS)(VALUE).txt", "r")
            file_read = file.read()

        SN_Data = ""
        if SN_LINECARD == "" and SN_CHASSIS != "":
            SN_Data = "\nand UUT.FIXTURE2_ID in ('" + SN_CHASSIS + "')"
        elif SN_CHASSIS == "" and SN_LINECARD != "":
            SN_Data = "\nand UUT.FIXTURE_ID in ('" + SN_LINECARD + "')"
        else:
            SN_Data = "\n--and UUT.FIXTURE_ID in"

        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}' 

        new_data = ()
        for i in DATA_Query_by_SN_in:
            START_DATE_TIME = i[3]
            SERIAL_NUMBER = i[2]
            RESULT = i[4]

            if RESULT != "ERROR" and RESULT != "PASS" and RESULT != "FAILED" and RESULT != "TERMINATED":
                SQL_Conn = pyodbc.connect(conn_str)
                cursor = SQL_Conn.cursor()
                # print(file_read + START_DATE_TIME + "')" +  SN_Data + "\nand SR.STATUS like ('%fail%')" + "\norder by UUT.START_DATE_TIME desc, SR.ORDER_NUMBER ASC")
                cursor.execute(file_read + START_DATE_TIME + "')" +  SN_Data + "\nand SR.STATUS like ('%fail%')" + "\nand UUT.TPS_NAME not like ('%ATE%') order by UUT.START_DATE_TIME desc, SR.ORDER_NUMBER ASC")          
                DATA_Query = cursor.fetchall() 
                new_data = new_data + tuple(DATA_Query)

                SQL_Conn.close()
                file.close() 

            elif RESULT == "ERROR":
                new_data = new_data + (('ERROR', '', ''),)
            elif RESULT == "FAILED":
                new_data = new_data + (('FAILED', '', ''),)
            elif RESULT == "TERMINATED":
                new_data = new_data + (('TERMINATED', '', ''),)
            else:
                new_data = new_data + (('', '', ''),)
        return new_data