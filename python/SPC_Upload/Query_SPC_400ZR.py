import pyodbc

class QuerySPC400ZR:
    def input_data(self, STATION, SLOT, PROCESS):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        if PROCESS == 'FCAL':
            TPS_NAME = '400ZR Calibration SPC'
            Operation = 'CAL'
            STEP_POWER_Rx = '-17.5'
            STEP_POWER_Tx = '-5'
        elif PROCESS == 'OPM':
            TPS_NAME = '400ZR OPM SPC'
            Operation = 'OPM'
            STEP_POWER_Rx = '-17.5'
            STEP_POWER_Tx = '-15'

        code = f'''
                SELECT
                    UUT.UUT_SERIAL_NUMBER
                    ,UUT.HW_PART_NUMBER
                    ,IIF(Substring(UUT.HW_PART_NUMBER, 5, 4) = '0239', 'QSFP-Bright', IIF(Substring(HW_PART_NUMBER, 5, 4) = '0195', 'QSFP-DD','')) as Model
                    ,CONCAT(RIGHT(UUT.STATION_ID, 3), ' : ', TEST_SOCKET_INDEX) as MC_Slot
                    ,UUT.MODE
                    ,convert(varchar,DATEADD(hour, 7, UUT.START_DATE_TIME),22) as START_DATE_TIME
                    ,UUT.UUT_STATUS
                    ,UUT.ID
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Tx OSNR In-Band') Order by SR.ID desc)) AS Tx_OSNR_In_Band
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Rx Power Monitor') AND SR.STEP_POWER in ('{STEP_POWER_Rx}') Order by SR.ID desc)) AS Rx_Power_Monitor
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Temperature - Laser') Order by SR.ORDER_NUMBER desc)) AS Temperature_Laser
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Temperature - ASIC') Order by SR.ID desc)) AS Temperature_ASIC
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Tx Power') AND SR.STEP_POWER in ('{STEP_POWER_Tx}') Order by SR.ID desc)) AS Tx_Power
                    ,UUT.PROCESS
                    ,CONCAT(RIGHT(UUT.PROCESS, 3), '-', '{Operation}') as Operation
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('UUT Turnup Tx Max Power Screen') Order by SR.ID desc)) AS UUT_Turnup_Tx_Max
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('Tx ITLA Frequency Offset (GHz)') Order by SR.ORDER_NUMBER asc)) AS ITLA_Frequency
                    ,(SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WITH(NOLOCK) WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_NAME in ('OSNR - FEC Threshold') Order by SR.ID desc)) AS OSNR_FEC_Threshold
                    
                FROM [ATSResults].[dbo].[UUT_RESULT] UUT WITH(NOLOCK)

                Where UUT.STATION_ID = '{STATION}'
                and UUT.TEST_SOCKET_INDEX = '{SLOT}'
                and UUT.UUT_STATUS = 'Passed'
                and UUT.TPS_NAME = '{TPS_NAME}'
                and CAST(convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) AS DATE) = CAST(GETDATE() AS DATE)
                order by UUT.START_DATE_TIME desc
                '''

        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        cursor.execute(code)
        DATA_Query = cursor.fetchall()

        SQL_Conn.close()

        return DATA_Query