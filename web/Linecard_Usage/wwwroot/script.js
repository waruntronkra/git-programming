// window.onload = function() {
//     var image = document.getElementById('background-1');
//     image.style.opacity = '1'; // Set opacity to 0 to start fading
// };
$(document).ready(async function () {
    var table_new;
    $('#bt').click(async function () { 
        // setTimeout(function() {
        //     document.getElementById('background-1').style.opacity = '0';
        // }, 400);

        // var input_sn = (document.getElementById('sn-input').value).split(',')
        // input_sn = input_sn.map(str => str.replace(/\n/g, ''));

        // var sn_text_query = '';
        // for (let i = 0; i < input_sn.length; i++) {
        //     sn_text_query += `,'${input_sn[i]}'`;
        // }

        // const data = (await getLinecardUsage(sn_text_query.slice(1)))['data'];
        const data_linecard_today = (await getLinecardToday())['data'].map(data => data['FIXTURE_ID']);
        var sn_text_query = '';
        for (let i = 0; i < data_linecard_today.length; i++) {
            sn_text_query += `,'${data_linecard_today[i]}'`;
        }
        const data = (await getLinecardUsage(sn_text_query.slice(1)))['data'];
        
        console.log(data)
        console.log(data_linecard_today)

        // Destroy exist table
        if (table_new) {
            table_new.destroy();
            $('#table-data').empty();
        }

        if (data.length > 0) {
            const column_head = Object.keys(data[0])

            var array_raw_data = [];
            for (let i = 0; i < data.length; i++) {
                const raw_data = Object.values(data[i]);

                let array = [];
                for (let j = 0; j < raw_data.length; j++) {
                    if (typeof raw_data[j] === 'object') {
                        array.push('')
                    }
                    else {
                        array.push(raw_data[j])
                    }
                }
                array_raw_data.push(array)
            }
            
            const table_container = document.getElementById('container-table');

            const table = document.getElementById('table-data');
            table.innerHTML = '';

            const thead = document.createElement('thead');
            const headRow = document.createElement('tr');
            for (let i = 0; i < column_head.length; i++) {
                const th = document.createElement('th');
                th.style.backgroundColor = 'rgb(3, 141, 93)';
                th.style.color = 'white';
                th.style.width = 'auto';
                th.style.border = '1px solid rgb(175, 175, 175)';

                th.textContent = column_head[i];
                headRow.appendChild(th);
            }
            thead.appendChild(headRow);
            table.appendChild(thead);

            const body = document.createElement('tbody');
            array_raw_data.forEach(rowData => {
                const row = document.createElement('tr');
                rowData.forEach(cellData => {
                    const cell = document.createElement('td');
                    cell.style.width = '200px';
                    cell.style.border = '1px solid rgb(175, 175, 175)';
                    cell.style.verticalAlign = 'middle';

                    cell.textContent = cellData;
                    row.appendChild(cell);
                })
                body.appendChild(row);
            })

            table.appendChild(body);
            table_container.appendChild(table);

            
            
            table_new =  new DataTable('#table-data', {
                scrollX: true,
                scrollY: true
            });
            
        }
        else {
            setTimeout(function() {
                document.getElementById('table-data').style.top = '-9999px';
                // document.getElementById('background-1').style.opacity = '1';
            }, 400);
            const table = document.getElementById('table-data');
            table.innerHTML = '';
        }
    });

    async function getLinecardUsage(sn) {
        try {
            const response = await fetch('/get-linecard-usage', {
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

    async function getLinecardToday() {
        try {
            const response = await fetch('/get-linecard-today', {
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
});