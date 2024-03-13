async function startRun()  {
    document.getElementById('loader').style.display = 'block';

    var data =  await queryData('7');
    var data_last =  await queryDataLast();
    
    var data_table = [];
    for (let i = 0; i < data['data'].length; i++) {
        console.log(data['data'][i])
        data_table.push([
            data['data'][i]['UUT_SERIAL_NUMBER'],
            data['data'][i]['START_DATE_TIME'],
            data['data'][i]['HW_PART_NUMBER'],
            data['data'][i]['MC_Slot'],
            data['data'][i]['ACR1_Avg'],
            data['data'][i]['Max_ACR1_Dev'],
        ])
    }
    console.log(data_table)
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