import pyodbc

class QueryATS:
    def input_data(self, SERIAL_NUMBER):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        code = f'''
                SELECT TOP 1
                    STATION_ID
                    ,UUT_SERIAL_NUMBER
                    ,TEST_COUNT
                    ,PRODUCT_CODE
                    ,FIXTURE_ID
                    ,convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) as START_DATE_TIME
                    ,EXECUTION_TIME
                    ,MODE
                    ,USER_LOGIN_NAME
                    ,TEST_SOCKET_INDEX
                    ,TPS_REV
                    ,HW_PART_NUMBER
                    ,HW_REV
                    ,FW_REV
                    ,FAIL_MODE

                FROM [ATSResults].[dbo].[vw_test_defect_latest] WITH(NOLOCK)

                Where UUT_SERIAL_NUMBER = '{SERIAL_NUMBER}'
                order by START_DATE_TIME desc
                '''

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()

        SQL_Conn.close()

        return DATA_Query