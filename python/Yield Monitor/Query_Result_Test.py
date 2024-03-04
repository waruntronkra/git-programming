import pyodbc
from datetime import datetime, timedelta

class QueryResultTest():
    def Receive_Data(self, STATION_ID, day, process, fresh, TAB_Name):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        text_file = ""
        if TAB_Name == "AC100M":
            file = open("temp/CODE (Non-AC1200)(by STATION).txt", "r")
            text_file = file.read()
        elif TAB_Name == "AC200":
            file = open("temp/CODE (Non-AC1200)(by STATION).txt", "r")
            text_file = file.read()
        elif TAB_Name == "AC400":
            file = open("temp/CODE (Non-AC1200)(by STATION).txt", "r")
            text_file = file.read()          
        else:
            file = open("temp/CODE (by STATION).txt", "r")
            text_file = file.read()

        # Start query and setup data to graph
        Array_Data_Queried = []
        for i in STATION_ID:          
            SQL_Conn = pyodbc.connect(conn_str)
            cursor = SQL_Conn.cursor()
            # print(text_file + day + "\nand PROCESS in " + process + fresh + "\nand STATION_ID in ('" + i + "')\norder by START_DATE_TIME desc")
            cursor.execute(text_file + day + "\nand PROCESS in " + process + fresh + "\nand STATION_ID in ('" + i + "')\n and TPS_NAME not like ('%ATE%') order by START_DATE_TIME desc")          
            DATA_Query = cursor.fetchall()  

            # Covert format column Date_time in 3rd element (START_DATE_TIME value)      
            new_data = []
            for tup in DATA_Query:
                dt_obj = datetime.strptime(tup[2], "%d %b %Y %H:%M:%S:%f")
                new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')
                new_dt_str_for_compare = dt_obj.strftime('%d %b,%y')

                today = datetime.now()
                previous_dates = [(today - timedelta(days=i)).strftime('%d %b,%y') for i in range(int(day))]
                for data in previous_dates:
                    if data == new_dt_str_for_compare:
                        new_tup = (tup[0], tup[1], new_dt_str, tup[3], tup[4], tup[5], tup[6])
                        new_data.append(new_tup)
            Array_Data_Queried.append(new_data)
            
            SQL_Conn.close()
        file.close()
        return Array_Data_Queried
            