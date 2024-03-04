import pyodbc
from datetime import datetime, timedelta

class QueryValueATECAL():
    def input_detai(self, day_in, STATION_in, parameter):
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

        Product_Type = STATION_in.split('_')
        file_read = ''
        if Product_Type[1] == 'AC100M' or Product_Type[1] == 'AC200' or Product_Type[1] == 'AC400':
            file = open("temp/CODE Query_ATE_CAL (Non-AC1200).txt", "r")
            file_read = file.read()
        else:
            file = open("temp/CODE Query_ATE_CAL.txt", "r")
            file_read = file.read()
        # Query Database
        SQL_Con = pyodbc.connect(conn_str)
        Cursor_Con = SQL_Con.cursor()
        String_Query = file_read + day_in + "\nand STATION_ID in ('" + STATION_in + "')\nand TPS_NAME like ('%ATE CAL%')\nand UUT.UUT_STATUS like ('%pass%')\nand DT.PATH like N'%" + code + "%'\nORDER by UUT.START_DATE_TIME asc ,SR.ORDER_NUMBER ASC"
        Cursor_Con.execute(String_Query)
        Data_Queried = Cursor_Con.fetchall()
     
        Array_Data_Queried =  []
        for tup in Data_Queried:
            dt_obj = datetime.strptime(tup[1], '%d %b %Y %H:%M:%S:%f')
            new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')
            dt_for_compare = dt_obj.strftime('%d %b,%y')

            today = datetime.now()
            previous_days = [(today-timedelta(days=i)).strftime('%d %b,%y') for i in range(int(day_in))]
            for data in previous_days:
                if data == dt_for_compare:
                    new_tup = (tup[0], new_dt_str, tup[2], tup[3], tup[4])
                    Array_Data_Queried.append(new_tup)
        file.close()
        SQL_Con.close()
            
        return Array_Data_Queried

        
        
