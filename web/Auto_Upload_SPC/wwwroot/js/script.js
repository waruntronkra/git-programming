async function startRun()  {
    document.getElementById('loader').style.display = 'block';

    var data =  await queryData('7');
    var data_last =  await queryDataLast();

    var data_table = [];
    for (let i = 0; i < data['data'].length; i++) {
        data_table.push([
            data['data'][i]['UUT_SERIAL_NUMBER'],
            data['data'][i]['START_DATE_TIME'],
            data['data'][i]['HW_PART_NUMBER'],
            data['data'][i]['MC_Slot'],
            data['data'][i]['ACR1_Avg'],
            data['data'][i]['Max_ACR1_Dev'],
        ])
    }
    var array_ACR1_Avg = [];
    var array_Max_ACR1_Dev = [];
    for (let i = 0; i < data_last['data'].length; i++) {
        if (data_last['data'][i]['UUT_SERIAL_NUMBER'] != '2135540068') {
            array_ACR1_Avg.push(data_last['data'][i]['ACR1_Avg']);
            array_Max_ACR1_Dev.push(data_last['data'][i]['Max_ACR1_Dev']);
        }
    }

    // ******************** Do Mean ********************
    const avg_array_ACR1_Avg = array_ACR1_Avg.reduce((acc, val) => acc + parseFloat(val), 0) / array_ACR1_Avg.length;
    const avg_array_Max_ACR1_Dev = array_Max_ACR1_Dev.reduce((acc, val) => acc + parseFloat(val), 0) / array_Max_ACR1_Dev.length;

    // ******************** Do Stdev ********************
    const sqr_array_ACR1_Avg = array_ACR1_Avg.map(num => Math.pow(parseFloat(num) - avg_array_ACR1_Avg, 2));
    const varience_array_ACR1_Avg = sqr_array_ACR1_Avg.reduce((acc, val) => acc + val, 0) / array_ACR1_Avg.length;
    const stdev_array_ACR1_Avg = Math.sqrt(varience_array_ACR1_Avg);

    const sqr_array_Max_ACR1_Dev = array_Max_ACR1_Dev.map(num => Math.pow(parseFloat(num) - avg_array_Max_ACR1_Dev, 2));
    const varience_array_Max_ACR1_Dev = sqr_array_Max_ACR1_Dev.reduce((acc, val) => acc + val, 0) / array_Max_ACR1_Dev.length;
    const stdev_array_Max_ACR1_Dev = Math.sqrt(varience_array_Max_ACR1_Dev);

    console.log(array_ACR1_Avg);
    console.log(array_Max_ACR1_Dev);

    console.log(`[AVG] ACR1_Avg : ${avg_array_ACR1_Avg}`);
    console.log(`[Stdev] ACR1_Avg : ${stdev_array_ACR1_Avg}`);

    console.log(`[AVG] Max_ACR1_Dev : ${avg_array_Max_ACR1_Dev}`);
    console.log(`[Stdev] Max_ACR1_Dev : ${stdev_array_Max_ACR1_Dev}`);

    // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
    const table = document.getElementById('table-data');
    table.innerHTML = '';

    const theader = document.createElement('thead');
    const headerRow = document.createElement('tr');
    var column_head = ['UUT_SERIAL_NUMBER', 'START_DATE_TIME', 'HW_PART_NUMBER', 'MC_Slot', 'ACR1_Avg', 'Max_ACR1_Dev']
    for (let i = 0; i < column_head.length; i++) {
        const th = document.createElement('th');
        th.textContent = column_head[i];
        headerRow.appendChild(th);
    }
    theader.appendChild(headerRow);
    table.appendChild(theader);

    const tbody = document.createElement('tbody');
    data_table.forEach(rowData => {
        const row = document.createElement('tr');
        rowData.forEach(cellData => {
            const cell = document.createElement('td');
            cell.textContent = cellData;
            row.appendChild(cell);
        });
        tbody.appendChild(row);
    });
    table.appendChild(tbody);

    const tableData = document.getElementById('container-table-data');
    tableData.appendChild(table);

    tableData.style.top = '110px';

    document.getElementById('loader').style.display = 'none';
}

async function queryData(daySelected) {
    try {
        const response = await fetch('/query-data', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ day: daySelected })
        });
        const data = await response.json();
        return data;
    } 
    catch (error) {
        console.log(`Error : ${error}`);
        return error;
    }
}

async function queryDataLast() {
    try {
        const response = await fetch('/query-data-last', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
        });
        const data = await response.json();
        return data;
    } 
    catch (error) {
        console.log(`Error : ${error}`);
        return error;
    }
}