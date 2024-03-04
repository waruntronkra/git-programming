import pyodbc

class QueryLastResultTest:
    def input_data(self, UUT_SN_in, PROCESS_in):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        code = f"SELECT TOP (1) [FAIL_MODE],[TEST_SOCKET_INDEX],[STATION_ID],[TEST_COUNT],[USER_LOGIN_NAME],[MODE],[FIXTURE_ID],[PRODUCT_CODE],[PRODUCT_CODE_REV],[HW_PART_NUMBER],[HW_REV],[SW_REV],convert(varchar,DATEADD(hour, 7, START_DATE_TIME), 113) as Local_START_DATE_TIME,[EXECUTION_TIME],[FAIL_MODE] \nFROM [ATSResults].[dbo].[vw_test_defect_latest]\nWHERE UUT_SERIAL_NUMBER in ('{UUT_SN_in}')\nAND PROCESS in ('{PROCESS_in}')\norder by START_DATE_TIME desc"

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()

        SQL_Conn.close()

        if DATA_Query:
            return DATA_Query[0]
        else:
            return 0