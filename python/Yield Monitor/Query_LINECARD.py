import pyodbc
from datetime import datetime, timedelta

class QueryLINECARD:
    def input_data(self, day, station, process, LINECARD_SN, CHASSIS_SN, mode):
        product_type = station.split('_')
        if mode == "By Date":
            if product_type[1] == 'AC100M' or product_type[1] == 'AC200' or product_type[1] == 'AC400':
                with open('temp/CODE Query LINECARD (Non_AC1200).txt', 'r') as f:
                    file_read = f.read()
            else:
                with open('temp/CODE Query LINECARD.txt', 'r') as f:
                    file_read = f.read()

            if LINECARD_SN == '' and CHASSIS_SN == '':
                query_code = file_read + day + "\nand VD.STATION_ID in ('" + station + "')\n--and VD.PROCESS in ('" + process + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"
            elif LINECARD_SN != '' and CHASSIS_SN == '':
                query_code = file_read + day + "\nand VD.STATION_ID in ('" + station + "')\n--and VD.PROCESS in ('" + process + "')\nand VD.FIXTURE_ID in ('" + LINECARD_SN + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"
            elif LINECARD_SN == '' and CHASSIS_SN != '':
                query_code = file_read + day + "\nand VD.STATION_ID in ('" + station + "')\n--and VD.PROCESS in ('" + process + "')\nand UUT.FIXTURE2_ID in ('" + CHASSIS_SN + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"

        elif mode == "By UUT":
            if product_type[1] == 'AC100M' or product_type[1] == 'AC200' or product_type[1] == 'AC400':
                with open('temp/CODE Query LINECARD (Non_AC1200)(By UUT).txt', 'r') as f:
                    file_read = f.read()
                file_read = file_read.replace("number", day) # day in this state is UUT amount (Top number)
                with open('temp/CODE Query LINECARD (Non_AC1200)(By UUT).txt', 'w') as f:
                    f.write(file_read)
                with open('temp/CODE Query LINECARD (Non_AC1200)(By UUT).txt', 'r') as f:
                    new_file_read = f.read()
            else:
                with open('temp/CODE Query LINECARD (By UUT).txt', 'r') as f:
                    file_read = f.read()
                file_read = file_read.replace("number", day) # day in this state is UUT amount (Top number)
                with open('temp/CODE Query LINECARD (By UUT).txt', 'w') as f:
                    f.write(file_read)
                with open('temp/CODE Query LINECARD (By UUT).txt', 'r') as f:
                    new_file_read = f.read()
            
            if LINECARD_SN == '' and CHASSIS_SN == '':
                query_code = file_read + "\nwhere VD.STATION_ID like ('%" + "ATE" + "%')\n--and VD.PROCESS in ('" + process + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"
            elif LINECARD_SN != '' and CHASSIS_SN == '':
                query_code = file_read + "\nwhere VD.STATION_ID like ('%" + "ATE" + "%')\n--and VD.PROCESS in ('" + process + "')\nand VD.FIXTURE_ID in ('" + LINECARD_SN + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"
            elif LINECARD_SN == '' and CHASSIS_SN != '':
                query_code = file_read + "\nwhere VD.STATION_ID like ('%" + "ATE" + "%')\n--and VD.PROCESS in ('" + process + "')\nand UUT.FIXTURE2_ID in ('" + CHASSIS_SN + "')\nand UUT.MODE not in ('RMA','ORM','SPC','KGB','EXPERIMENT','DEVELOPER')\nand UUT.TPS_NAME not like ('%ATE CAL%')\nand VD.TEST_COUNT in ('1')\norder by VD.START_DATE_TIME desc"
        
            if product_type[1] == 'AC100M' or product_type[1] == 'AC200' or product_type[1] == 'AC400':
                with open('temp/CODE Query LINECARD (Non_AC1200)(By UUT).txt', 'r') as f:
                    file_read = f.read()
                file_read = file_read.replace("Top " + str(day), "Top number") # day in this state is UUT amount (Top number)
                with open('temp/CODE Query LINECARD (Non_AC1200)(By UUT).txt', 'w') as f:
                    f.write(file_read)

            else:
                with open('temp/CODE Query LINECARD (By UUT).txt', 'r') as f:
                    file_read = f.read()
                file_read = file_read.replace("Top " + str(day), "Top number") # day in this state is UUT amount (Top number)
                with open('temp/CODE Query LINECARD (By UUT).txt', 'w') as f:
                    f.write(file_read)
     
        server = '10.6.1.145,14000'
        database = 'ATS_Results'
        username = 'ats_read'
        password = 'R6ad4r#Acac1a'
        driver = '{SQL Server}'
        conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
    
        SQL_conn = pyodbc.connect(conn_str)
        cursor_conn = SQL_conn.cursor()
        cursor_conn.execute(query_code)
        DATA_Queried = cursor_conn.fetchall()
        
        new_data = []
        for tup in DATA_Queried:
            dt_obj = datetime.strptime(tup[3], "%d %b %Y %H:%M:%S:%f")
            new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')
            new_dt_str_for_compare = dt_obj.strftime('%d %b,%y')

            today = datetime.now()
            previous_dates = [(today - timedelta(days=i)).strftime('%d %b,%y') for i in range(int(day))]
            for data in previous_dates:
                if data == new_dt_str_for_compare:
                    new_tup = (tup[0], tup[1], tup[2], new_dt_str, tup[4], tup[5], tup[6], tup[7], tup[8])
                    new_data.append(new_tup)

            if product_type[1] == 'AC100M' or product_type[1] == 'AC200' or product_type[1] == 'AC400':
                new_data = [(t[0], t[1], t[2], t[3], t[4], t[5], '', t[7], t[8]) for t in new_data]

        SQL_conn.close()
        if mode == "By Date":
            return new_data
        elif mode == "By UUT":
            new_data = []
            for tup in DATA_Queried:
                dt_obj = datetime.strptime(tup[3], "%d %b %Y %H:%M:%S:%f")
                new_dt_str = dt_obj.strftime('%d %b,%y %H:%M')

                new_tup = (tup[0], tup[1], tup[2], new_dt_str, tup[4], tup[5], tup[6], tup[7], tup[8])
                new_data.append(new_tup)

            return new_data


    