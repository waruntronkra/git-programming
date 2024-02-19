from flask import Flask, request, jsonify
import win32com.client as win32
import random
import pyodbc
from datetime import datetime

app = Flask(__name__)

# Query User information
@app.route('/userinfo', methods=["GET"])
def userChecking():
    d = str(request.args['username'])

    server = 'FITS-026,14000'
    database = 'dbAcacia_Center'
    username = 'ACACIA_USER'
    password = 'User@cac1a'
    driver = '{SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'

    SQL_Conn = pyodbc.connect(conn_str)
    cursor = SQL_Conn.cursor()
    query_code = f'''
                    SELECT * FROM [dbAcacia_Center].[dbo].[tb_Employees] WITH(NOLOCK) WHERE username = '{d}'
                '''
    cursor.execute(query_code)          
    DATA_Query = cursor.fetchall() 

    if len(DATA_Query) > 0:
        # outlook = win32.Dispatch("Outlook.Application")
        # mail = outlook.CreateItem(0)
        # mail.To = f"{d}@fabrinet.co.th"
        # mail.Subject= 'Second Factor for YMA Mobile App'

        random_number = random.randint(1, 999999)

        # mail.Body = f"============== THis is Number for enter in Yield Monitor [ACACIA] mobile app ============== \n\n ==> {str(random_number)} <=="
        # mail.Send()
        
        print(random_number)

        return {
                'username' : d,
                'random_number' : str(random_number)
                }
    
    else:
        return {
                'username' : 'fail',
                'random_number' : 'NaN'
                }

# Query All Product detail 
@app.route('/queryproductname')
def query_product_name():
    server = '10.6.1.145,14000'
    database = 'ATS_Center'
    username = 'db_rw'
    password = 'Wr1te4@sta'
    driver = '{SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
 
    SQL_Conn = pyodbc.connect(conn_str)
    cursor = SQL_Conn.cursor()
    query_code = '''
                    SELECT DISTINCT Level, Model, Process, [Order], HideNPI
                    FROM ATS_Center..[71_tb_Config_Process] (NOLOCK)
                    WHERE (Level NOT LIKE ':%') AND Model <> '' AND Process <> ''
                    ORDER BY Level, Model, [Order]
                '''
    cursor.execute(query_code)          
    DATA_Query = cursor.fetchall() 
    
    product_name = [i[0] for i in DATA_Query]
    product_name = list(set(product_name))
    dict_product_name = {'Level': product_name[1:]}

    column_names = [column[0] for column in cursor.description]
    table_product_name = [
        {column: str(value) for column, value in zip(column_names, row)}
        for row in DATA_Query
    ]
    
    return {
            'product_name' : dict_product_name,
            'table_product_name': table_product_name
            }

# Query Column Name
@app.route('/querycolname', methods=["GET"])
def query_column_name():
    input_data = str(request.args['input'])
    level = input_data.split('_')[0]
    model = input_data.split('_')[1]
    process = input_data.split('_')[2]

    server = '10.6.1.145,14000'
    database = 'ATS_Center'
    username = 'db_rw'
    password = 'Wr1te4@sta'
    driver = '{SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
 
    SQL_Conn = pyodbc.connect(conn_str)
    cursor = SQL_Conn.cursor()
    query_code = f'''
                    ATS_Center..[71_sp_All_Report] 
                    @Level = '{level}', 
                    @Model = '{model}', 
                    @Process = '{process}', 
                    @DrillOn = 'YIELD', 
                    @PreTest = 1, 
                    @IncEngBld = 3
                '''
    cursor.execute(query_code)          
    DATA_Query = cursor.fetchall() 
    
    data = [i[0] for i in DATA_Query]
    dict_column_name = {'column': data[1:]}

    return {
            'col_name' : dict_column_name
            }

# Query YIELD
@app.route('/queryyield', methods=["GET"])
def query_YIELD():
    input_data = str(request.args['input'])
    level = input_data.split('_')[0]
    model = input_data.split('_')[1]
    day = input_data.split('_')[2]
    day_num = int(day.split(' ')[0]) - 1

    day_mode = 'DATE'
    if 'Day' in day.split(' ')[1]:
        day_mode = 'DATE'
    elif 'Week' in day.split(' ')[1]:
        day_mode = 'WEEK'
    elif 'Month' in day.split(' ')[1]:
        day_mode = 'MONTH'
    elif 'Quarter' in day.split(' ')[1]:
        day_mode = 'QUARTER'

    server = '10.6.1.145,14000'
    database = 'ATS_Center'
    username = 'db_rw'
    password = 'Wr1te4@sta'
    driver = '{SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
 
    SQL_Conn = pyodbc.connect(conn_str)
    cursor = SQL_Conn.cursor()
    query_code = f'''
                    ATS_Center..[71_sp_All_Report]
                    @Level = '{level}',
                    @Model = '{model}',
                    @Backward = '{str(day_num)}',
                    @BackTo = '1',
                    @GroupBy = '{day_mode}',
                    @DrillOn = 'YIELD',
                    @IncEngBld = '3',
                    @Filter = ' AND Mode IN(''Production'', ''NPI'')',
                    @PreTest = '1',
                    @MinCumCal = '1',
                    @FirstMonth = '0'
                '''
    cursor.execute(query_code)          
    DATA_Query = cursor.fetchall() 

    column_names = [column[0] for column in cursor.description]
    data = [
        {column: str(value) for column, value in zip(column_names, row)}
        for row in DATA_Query
        ]
    
    DT = list(set([i[day_mode] for i in data]))
    if 'DATE' in column_names:
        sorted_dates = sorted(DT, key=lambda x: datetime.strptime(x, '%d %b %Y') if ' ' in x else datetime.max)
        sorted_dates = sorted_dates[::-1]
    elif 'WEEK' in column_names:
        sorted_dates = sorted(DT, key=lambda w: datetime.strptime(w.replace("WW-", ""), "%W '%y"))
        sorted_dates = sorted_dates[::-1]
    elif 'MONTH' in column_names:
        sorted_dates = sorted(DT, key=lambda x: datetime.strptime(x, '%b %Y'))
        sorted_dates = sorted_dates[::-1]
    elif 'QUARTER' in column_names:
        sorted_dates = sorted(DT, key=lambda q: datetime.strptime(q.replace('Q', ''), '%m-%Y'))    
        sorted_dates = sorted_dates[::-1]

    Grouped_Process = {}    
    for i in data:
        if i['Process'] not in Grouped_Process:
            Grouped_Process[i['Process']] = []
        Grouped_Process[i['Process']].append((i[day_mode], i['QTY'], i['FPY'], i['RTY'], i['IN'], i['Pass'], (int(i['IN'])) - int(i['OUT'])))

    Grouped_Process_with_Pareto = {}    
    for i in data:
        if i['Process'] not in Grouped_Process_with_Pareto:
            Grouped_Process_with_Pareto[i['Process']] = []
        Grouped_Process_with_Pareto[i['Process']].append((i[day_mode], i['Pareto']))

    group_data = {}
    PR = []
    for key, value in Grouped_Process.items():
        PR.append(key)
        date_form = [i[0] for i in value]
        for j in sorted_dates:
            if j in date_form:
                if key not in group_data:
                    group_data[key] = []
                group_data[key].append(value[date_form.index(j)])
            else:
                if key not in group_data:
                    group_data[key] = []
                group_data[key].append(('', '', '', '', '', '', ''))

    group_data_pareto_sorting = {}
    for key, value in Grouped_Process_with_Pareto.items():
        arrDT = list(set([i[0] for i in value]))
        arrAll = []
        for j in arrDT:
            arr = []
            arr.append(j)
            for item in value:
                if j in item:
                    arr.append(item[1])
            arrAll.append(arr)
        if key not in group_data_pareto_sorting:
            group_data_pareto_sorting[key] = []
        group_data_pareto_sorting[key].append(arrAll)
    # ==========================================================
    group_data_pareto_sorting = {key: [item for sublist in value for item in sublist] for key, value in group_data_pareto_sorting.items()} # Reduce array inside
    group_data_pareto_sorting = {key: [sublist + [''] * (6 - len(sublist)) for sublist in value] for key, value in group_data_pareto_sorting.items()}  # Fill empty string if len not equl 6
    
    group_data_pareto = {}
    for key, value in group_data_pareto_sorting.items():
        date_form = [i[0] for i in value]
        for j in sorted_dates:
            if j in date_form:
                if key not in group_data_pareto:
                    group_data_pareto[key] = []
                group_data_pareto[key].append(value[date_form.index(j)])
            else:
                if key not in group_data_pareto:
                    group_data_pareto[key] = []
                group_data_pareto[key].append(['', '', '', '', '', '', ''])
    # ==========================================================

    return {
            'yield_data' : group_data,
            'col_head' : sorted_dates,
            'row_head' : PR,
            'pareto' : group_data_pareto
            }

# Query PARETO
@app.route('/querypareto', methods=["GET"])
def query_PARETO():
    input_data = str(request.args['input'])
    level = input_data.split('_')[0]
    model = input_data.split('_')[1]
    day = input_data.split('_')[2]
    day_num = int(day.split(' ')[0]) - 1

    day_mode = 'DATE'
    if 'Day' in day.split(' ')[1]:
        day_mode = 'DATE'
    elif 'Week' in day.split(' ')[1]:
        day_mode = 'WEEK'
    elif 'Month' in day.split(' ')[1]:
        day_mode = 'MONTH'
    elif 'Quarter' in day.split(' ')[1]:
        day_mode = 'QUARTER'

    server = '10.6.1.145,14000'
    database = 'ATS_Center'
    username = 'db_rw'
    password = 'Wr1te4@sta'
    driver = '{SQL Server}'
    conn_str = f'DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}'
 
    SQL_Conn = pyodbc.connect(conn_str)
    cursor = SQL_Conn.cursor()
    query_code = f'''
                    ATS_Center..[71_sp_All_Report]
                    @Level = '{level}',
                    @Model = '{model}',
                    @Backward = '{str(day_num)}',
                    @BackTo = '1',
                    @GroupBy = '{day_mode}',
                    @DrillOn = 'PARETO',
                    @IncEngBld = '3',
                    @Filter = ' AND Mode IN(''Production'', ''NPI'')',
                    @PreTest = '1',
                    @MinCumCal = '1',
                    @FirstMonth = '0'
                '''
    cursor.execute(query_code)          
    DATA_Query = cursor.fetchall() 

    column_names = [column[0] for column in cursor.description]
    data = [
        {column: str(value) for column, value in zip(column_names, row)}
        for row in DATA_Query
    ]


    result_test = list(set([i['Result'] for i in data]))
    
    # Sort DATE
    DT = list(set([i[day_mode] for i in data]))
    if 'DATE' in column_names:
        sorted_dates = sorted(DT, key=lambda x: datetime.strptime(x, '%d %b %Y') if ' ' in x else datetime.max)
        sorted_dates = sorted_dates[::-1]
    elif 'WEEK' in column_names:
        sorted_dates = sorted(DT, key=lambda w: datetime.strptime(w.replace("WW-", ""), "%W '%y"))
        sorted_dates = sorted_dates[::-1]
    elif 'MONTH' in column_names:
        sorted_dates = sorted(DT, key=lambda x: datetime.strptime(x, '%b %Y'))
        sorted_dates = sorted_dates[::-1]
    elif 'QUARTER' in column_names:
        sorted_dates = sorted(DT, key=lambda q: datetime.strptime(q.replace('Q', ''), '%m-%Y'))    
        sorted_dates = sorted_dates[::-1]

    Grouped = {}    
    for i in data:
        if i['Result'] not in Grouped:
            Grouped[i['Result']] = []
        Grouped[i['Result']].append((i['Result'], i[day_mode], i['QTY'], i['R']))


    group_data = {}
    RT = []
    for key, value in Grouped.items():
        RT.append(key)
        date_form = [i[1] for i in value]
        for j in sorted_dates:
            if j in date_form:
                if key not in group_data:
                    group_data[key] = []
                group_data[key].append(value[date_form.index(j)])
            else:
                if key not in group_data:
                    group_data[key] = []
                group_data[key].append(('', '', '', ''))
    
    return {
            'pareto_data' : group_data,
            'col_head' : sorted_dates,
            'row_head' : result_test,
            }

if __name__ == '__main__':
    app.run(debug=True, port=8000)

