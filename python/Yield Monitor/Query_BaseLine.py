import pyodbc
from datetime import datetime, timedelta
from collections import OrderedDict

class QueryBaseLine():
    def input_detai(self, STATION_in, parameter):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        if parameter == 'Loss Factor':
            code = 'Results.Offset'
        elif parameter == 'Tap Power':
            code = 'Ref_Power'
        elif parameter == 'UUT Power':
            code = 'OPM_Power'

        file = open("temp/CODE BaseLine.txt", "r")
        file_read = file.read()
        file_read = file_read.replace('PARAMETER', code)

        for i in range(999):
            # Query Database
            today = datetime.now()
            SQL_Con = pyodbc.connect(conn_str)
            Cursor_Con = SQL_Con.cursor()
            String_Query = "DECLARE @start_time DATETIME DECLARE @STATIOIN VARCHAR(20) = '" + STATION_in + file_read
            Cursor_Con.execute(String_Query)
            print(String_Query)
            Data_Queried = Cursor_Con.fetchall()
        
            Array_Data_Queried =  []
            for tup in Data_Queried:
                dt_obj = datetime.strptime(tup[1], '%d %b %Y %H:%M:%S:%f')
                new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')
                dt_for_compare = dt_obj.strftime('%d %b,%y')

                new_tup = (tup[0], new_dt_str, tup[2], tup[3], tup[4])
                Array_Data_Queried.append(new_tup)
            file.close()
            SQL_Con.close()   
            return Array_Data_Queried   

             

        
        
