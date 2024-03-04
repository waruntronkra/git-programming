import pyodbc

class QueryLastResultTestLCT:
    def input_data(self, UUT_SN_in, PROCESS_in):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        code = f'''
                SELECT TOP (1) 
                [UUT_SERIAL_NUMBER],
                [TEST_COUNT],
                [USER_LOGIN_NAME],
                [MODE],
                [STATION_ID],
                [FIXTURE_ID],
                [TEST_SOCKET_INDEX],
                [PRODUCT_CODE],
                [PRODUCT_CODE_REV],
                [HW_PART_NUMBER],
                [HW_REV],
                [SW_REV],
                convert(varchar,DATEADD(hour, 7, START_DATE_TIME), 22) as Local_START_DATE_TIME,
                [EXECUTION_TIME],
                [FAIL_MODE]
                FROM [ATSResults].[dbo].[vw_test_defect_latest]
                WHERE UUT_SERIAL_NUMBER in ('{UUT_SN_in}')
                AND PROCESS in ('{PROCESS_in}')
                order by START_DATE_TIME desc
                '''

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()

        QL_Conn.close()

        return DATA_Query[0]
