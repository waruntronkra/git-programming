import pyodbc
from datetime import datetime, timedelta

class QueryLastResultTest():
    def Input_Data(self, day, process, fresh, TAB_Name, Product):
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

        fresh = "\nand TEST_COUNT in ('1')"
        
        text_file = ""
        if TAB_Name == "AC100M":
            file = open("temp/CODE (Non-AC1200)(LAST)(by PROCESS).txt", "r")
            text_file = file.read()
        elif TAB_Name == "AC200":
            file = open("temp/CODE (Non-AC1200)(LAST)(by PROCESS).txt", "r")
            text_file = file.read()
        elif TAB_Name == "AC400":
            file = open("temp/CODE (Non-AC1200)(LAST)(by PROCESS).txt", "r")
            text_file = file.read()          
        else:
            file = open("temp/CODE (LAST)(by PROCESS).txt", "r")
            text_file = file.read()

        # Start query and setup data to graph
        SQL_Conn = pyodbc.connect(conn_str)
        cursor = SQL_Conn.cursor()
        code_for_query = text_file + day + "\nand PROCESS in ('" + process + "')" + fresh + "\nand MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')" + "\nand STATION_ID like ('%" + Product + "%')\nand TPS_NAME not like ('%ATE%')" + "\norder by START_DATE_TIME desc"
        # print(code_for_query)
        cursor.execute(code_for_query)          
        DATA_Query = cursor.fetchall()  

        # Covert format column Date_time in 2rd element (START_DATE_TIME value) 
        results = []   
        for tup in DATA_Query:
            dt_obj = datetime.strptime(tup[1], "%d %b %Y %H:%M:%S:%f")
            new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')
            new_dt_str_for_compare = dt_obj.strftime('%d %b,%y')
                 
            today = datetime.now()
            previous_dates = [(today - timedelta(days=i)).strftime('%d %b,%y') for i in range(int(day))]
            for data in previous_dates:
                if data == new_dt_str_for_compare:
                    new_tup = (tup[0],new_dt_str)
                    results.append(new_tup)
        
        SQL_Conn.close()
        file.close()
        return results
            