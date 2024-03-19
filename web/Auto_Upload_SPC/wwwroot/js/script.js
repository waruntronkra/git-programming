async function startRun() {
    try {
        intervalId = setInterval(async function() {
            var date_today = (new Date()).toLocaleString('en-US', { month: '2-digit', day: '2-digit', year: '2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true });
            document.getElementById('text-date-refresh').innerText = `Date Time : ${date_today}`;
            if (date_today.split(' ')[1] == '8:01:05') {
                document.getElementById('loader').style.display = 'block';
    
                var data_last = await queryDataLast();
    
                var data_table = [];
                var result_fits = [];
                for (let i = 0; i < data_last['data'].length; i++) {
                    if (data_last['data'][i]['UUT_SERIAL_NUMBER'] != '2135540068') {
                        var date_latest = await queryDateLatest(data_last['data'][i]['UUT_SERIAL_NUMBER']);
                        data_table.push([
                            data_last['data'][i]['UUT_SERIAL_NUMBER'],
                            data_last['data'][i]['START_DATE_TIME'],
                            data_last['data'][i]['HW_PART_NUMBER'],
                            data_last['data'][i]['MC_Slot'],
                            data_last['data'][i]['ACR1_Avg'],
                            data_last['data'][i]['Max_ACR1_Dev'],
                        ]);
                        if (date_today.split(',')[0] != date_latest['data'][0]['Local_Date_Time'].split(' ')[0]) {
                            // result_fits.push(await WebServiceFIts('', 'fn_Log', parameter_FITS_text, value_FITS_text_array[i], '1', operation));
                            result_fits.push([data_last['data'][i]['UUT_SERIAL_NUMBER'], await WebServiceFIts(
                                data_last['data'][i]['UUT_SERIAL_NUMBER'], 
                                'fn_Handshake', 
                                'TOSA',
                                'SPC270', 
                                '1', 
                                'EN,TOSA SN,Part Number,Machine ID,ACR1_Avg,Max_ACR1_Dev', 
                                `${document.getElementById('input-en').value},${data_last['data'][i]['UUT_SERIAL_NUMBER']},${data_last['data'][i]['HW_PART_NUMBER']},${data_last['data'][i]['MC_Slot']},${data_last['data'][i]['ACR1_Avg']},${data_last['data'][i]['Max_ACR1_Dev']}`
                            )]);
                        }
                        else {
                            result_fits.push([data_last['data'][i]['UUT_SERIAL_NUMBER'], 'Added']);
                        }
                    }
                }
    
                // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                for (let i = 0; i < 2; i++) {
                    if (i == 0) {
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
    
                        const tableContainer = document.getElementById('container-table-data');
                        tableContainer.appendChild(table);
    
                        tableContainer.style.top = '150px';
    
                        document.getElementById('loader').style.display = 'none';
                    }
                    else {
                        const table = document.getElementById('table-result-fits');
                        table.innerHTML = '';
    
                        const theader = document.createElement('thead');
                        const headerRow = document.createElement('tr');
                        var column_head = ['UUT_SERIAL_NUMBER', 'Result']
                        for (let i = 0; i < column_head.length; i++) {
                            const th = document.createElement('th');
                            th.textContent = column_head[i];
                            headerRow.appendChild(th);
                        }
                        theader.appendChild(headerRow);
                        table.appendChild(theader);
    
                        const tbody = document.createElement('tbody');
                        result_fits.forEach(rowData => {
                            const row = document.createElement('tr');
                            rowData.forEach(cellData => {
                                const cell = document.createElement('td');
                                cell.textContent = cellData;
                                row.appendChild(cell);
                            });
                            tbody.appendChild(row);
                        });
                        table.appendChild(tbody);
    
                        const tableContainer = document.getElementById('container-table-result-fits');
                        tableContainer.appendChild(table);
    
                        tableContainer.style.top = '370px';
    
                        document.getElementById('loader').style.display = 'none';
                    }
                }
            }
        }, 1000);

        
        // intervalId = setInterval(async function() {
        //     document.getElementById('loader').style.display = 'block';

        //     var data_last =  await queryDataLast();

        //     var date_today = (new Date()).toLocaleString('en-US', { month: '2-digit', day: '2-digit', year: '2-digit', hour: 'numeric', minute: 'numeric', second: 'numeric', hour12: true });

        //     document.getElementById('text-date-refresh').innerText = `Last refreshed : ${date_today}`;

        //     var data_table = [];
        //     var result_fits = [];
        //     for (let i = 0; i < data_last['data'].length; i++) {
        //         if (data_last['data'][i]['UUT_SERIAL_NUMBER'] != '2135540068') {
        //             var date_latest = await queryDateLatest(data_last['data'][i]['UUT_SERIAL_NUMBER']);
        //             data_table.push([
        //                 data_last['data'][i]['UUT_SERIAL_NUMBER'],
        //                 data_last['data'][i]['START_DATE_TIME'],
        //                 data_last['data'][i]['HW_PART_NUMBER'],
        //                 data_last['data'][i]['MC_Slot'],
        //                 data_last['data'][i]['ACR1_Avg'],
        //                 data_last['data'][i]['Max_ACR1_Dev'],
        //             ]);
        //             if (date_today.split(',')[0] != date_latest['data'][0]['Local_Date_Time'].split(' ')[0]) {
        //                 // result_fits.push(await WebServiceFIts('', 'fn_Log', parameter_FITS_text, value_FITS_text_array[i], '1', operation));
        //                 result_fits.push([data_last['data'][i]['UUT_SERIAL_NUMBER'], await WebServiceFIts(
        //                     data_last['data'][i]['UUT_SERIAL_NUMBER'], 
        //                     'fn_Handshake', 
        //                     'TOSA',
        //                     'SPC270', 
        //                     '1', 
        //                     'EN,TOSA SN,Part Number,Machine ID,ACR1_Avg,Max_ACR1_Dev', 
        //                     `${document.getElementById('input-en').value},${data_last['data'][i]['UUT_SERIAL_NUMBER']},${data_last['data'][i]['HW_PART_NUMBER']},${data_last['data'][i]['MC_Slot']},${data_last['data'][i]['ACR1_Avg']},${data_last['data'][i]['Max_ACR1_Dev']}`
        //                 )]);
        //             }
        //             else {
        //                 result_fits.push([data_last['data'][i]['UUT_SERIAL_NUMBER'], 'Added']);
        //             }
        //         }
        //     }

        //     // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
        //     for (let i = 0; i < 2; i++) {
        //         if (i == 0) {
        //             const table = document.getElementById('table-data');
        //             table.innerHTML = '';

        //             const theader = document.createElement('thead');
        //             const headerRow = document.createElement('tr');
        //             var column_head = ['UUT_SERIAL_NUMBER', 'START_DATE_TIME', 'HW_PART_NUMBER', 'MC_Slot', 'ACR1_Avg', 'Max_ACR1_Dev']
        //             for (let i = 0; i < column_head.length; i++) {
        //                 const th = document.createElement('th');
        //                 th.textContent = column_head[i];
        //                 headerRow.appendChild(th);
        //             }
        //             theader.appendChild(headerRow);
        //             table.appendChild(theader);

        //             const tbody = document.createElement('tbody');
        //             data_table.forEach(rowData => {
        //                 const row = document.createElement('tr');
        //                 rowData.forEach(cellData => {
        //                     const cell = document.createElement('td');
        //                     cell.textContent = cellData;
        //                     row.appendChild(cell);
        //                 });
        //                 tbody.appendChild(row);
        //             });
        //             table.appendChild(tbody);

        //             const tableContainer = document.getElementById('container-table-data');
        //             tableContainer.appendChild(table);

        //             document.getElementById('loader').style.display = 'none';
        //         }
        //         else {
        //             const table = document.getElementById('table-result-fits');
        //             table.innerHTML = '';

        //             const theader = document.createElement('thead');
        //             const headerRow = document.createElement('tr');
        //             var column_head = ['UUT_SERIAL_NUMBER', 'Result']
        //             for (let i = 0; i < column_head.length; i++) {
        //                 const th = document.createElement('th');
        //                 th.textContent = column_head[i];
        //                 headerRow.appendChild(th);
        //             }
        //             theader.appendChild(headerRow);
        //             table.appendChild(theader);

        //             const tbody = document.createElement('tbody');
        //             result_fits.forEach(rowData => {
        //                 const row = document.createElement('tr');
        //                 rowData.forEach(cellData => {
        //                     const cell = document.createElement('td');
        //                     cell.textContent = cellData;
        //                     row.appendChild(cell);
        //                 });
        //                 tbody.appendChild(row);
        //             });
        //             table.appendChild(tbody);

        //             const tableContainer = document.getElementById('container-table-result-fits');
        //             tableContainer.appendChild(table);

        //             document.getElementById('loader').style.display = 'none';
        //         }
        //     }
        // }, 180000);
    }
    catch (e) {
        console.warn(e);
        alert(e)
    }
}

function stopRun() {
    clearInterval(intervalId);
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

async function queryDateLatest(sn) {
    try {
        const response = await fetch('/query-date-latest', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ sn: sn })
        });
        const data = await response.json();
        return data;
    } 
    catch (error) {
        console.log(`Error : ${error}`);
        return error;
    }
}

async function WebServiceFIts(sn, type, model, oper, rev, parameter, value) {
    try {
        // !!! use "<NAME_OF_YOUR_SITE>/webservice-fits?"
        const response = await fetch(`/webservice-fits?serialnumber=${sn}&operation=${oper}&type=${type}&parameter=${parameter}&value=${value}&model=${model}&revision=${rev}`);
        const dataXML = await response.text();
        if (dataXML.split('<a:Message/><a:Result>').length > 1) {
            return dataXML.split('<a:Message/><a:Result>')[1].split('</a:Result>')[0];
        }
        else {
            return dataXML.split('<a:Message>')[1].split('</a:Message>')[0];
        }
        
    } catch (error) {
        console.error('Error:', error);
        throw error;
    }
}

// var array_ACR1_Avg = [];
        // var array_Max_ACR1_Dev = [];
        // for (let i = 0; i < data_last['data'].length; i++) {
        //     if (data_last['data'][i]['UUT_SERIAL_NUMBER'] != '2135540068') {
        //         array_ACR1_Avg.push(data_last['data'][i]['ACR1_Avg']);
        //         array_Max_ACR1_Dev.push(data_last['data'][i]['Max_ACR1_Dev']);
        //     }
        // }

        // ******************** Do Mean ********************
        // const avg_array_ACR1_Avg = array_ACR1_Avg.reduce((acc, val) => acc + parseFloat(val), 0) / array_ACR1_Avg.length;
        // const avg_array_Max_ACR1_Dev = array_Max_ACR1_Dev.reduce((acc, val) => acc + parseFloat(val), 0) / array_Max_ACR1_Dev.length;

        // ******************** Do Stdev ********************
        // const sqr_array_ACR1_Avg = array_ACR1_Avg.map(num => Math.pow(parseFloat(num) - avg_array_ACR1_Avg, 2));
        // const varience_array_ACR1_Avg = sqr_array_ACR1_Avg.reduce((acc, val) => acc + val, 0) / array_ACR1_Avg.length;
        // const stdev_array_ACR1_Avg = Math.sqrt(varience_array_ACR1_Avg);

        // const sqr_array_Max_ACR1_Dev = array_Max_ACR1_Dev.map(num => Math.pow(parseFloat(num) - avg_array_Max_ACR1_Dev, 2));
        // const varience_array_Max_ACR1_Dev = sqr_array_Max_ACR1_Dev.reduce((acc, val) => acc + val, 0) / array_Max_ACR1_Dev.length;
        // const stdev_array_Max_ACR1_Dev = Math.sqrt(varience_array_Max_ACR1_Dev);