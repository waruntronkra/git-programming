$(document).ready(async function() {
	var model = 'All Module';
    var revision = '1'; // Check-in = 0, Check-in = 1
    var value_FITS_text_array = [];
    var initial_check = [];
    var parameter_FITS_text = '';
    var parameter_FITS_array = [];
    var result_check_out_FITs = [];
    var button_id_for_revise = '';
    var last_button_id = '';
    var edit_active = false;
    var listSN = [];
    var listSN_ID = [];
    var duplicate_index = {};
    var index_bad_SN = [];
    var handshake_for_hover = [];
    var data_handshake = [];
	var data_handshake_all = [];

    $(`#input-dev-effective-date`).text('-');
    $(`#input-dev-end-date`).text('-');
    $(`#input-dev-model`).text('-');
    $(`#input-dev-pn`).text('-');

    $("#error-pop-up").css({
        'scale' : '0'
    });

    $(document).on('mouseenter', '.sn-indicator', function () {

        if (handshake_for_hover.length > 0) {
			if (handshake_for_hover[$(this).index()] != 'True') {
				$('#tooltip-new').text(handshake_for_hover[$(this).index()]);
				$("#tooltip-new").css({
										'top': $(this).offset()['top'] + 40, 
										'left': $(this).offset()['left'],
										'scale' : '1'
									});
			}
            
        }  
    });
    
    $(document).on('mouseleave', '.sn-indicator', function () {
        $("#tooltip-new").css({
            'scale' : '0'
        });
    });

    // Initial per Local Storage data ****************************************************
    if (localStorage.getItem('text_process') != null) {
        try {
            process = localStorage.getItem('text_process').split(' : ')[0];
            operation = localStorage.getItem('text_process').split(' : ')[1];
            document.getElementById('text-process').textContent = localStorage.getItem('text_process');

            if (
                process == 'FCAL' ||
                process == 'OPM' ||
                process == 'OPMP' ||
                process == 'OPMT' ||
                process == 'EXP' ||
                process == 'LCT1' ||
                process == 'LCT2' ||
                process == 'LCTT'
                ) 
                {
                model = 'All Module';
            }

            else if (process == 'DEV01') {
                model = '*';
            }
			
            var data = await getParamFITs();

            parameter_FITS_array = [];
            for (let i = 0; i < data['data'].length; i++) {
                if (data['data'][i]['PARAMETER'] != 'Lid RT & SN') {
                    parameter_FITS_array.push(data['data'][i]['PARAMETER']);
                }
                else {
                    parameter_FITS_array.push('Lid RT _SN');
                }
            }

            parameter_FITS_text = '';
            for (let i = 0; i < parameter_FITS_array.length; i++) {
                parameter_FITS_text += `,${parameter_FITS_array[i]}`;
            }
            parameter_FITS_text = parameter_FITS_text.slice(1);

            // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            const result_data_table = document.getElementById('table-parameter-fits');
            result_data_table.innerHTML = '';

            const theader = document.createElement('thead');
            const headerRow = document.createElement('tr');

            const th = document.createElement('th');
            th.textContent = 'Parameter';
            
            headerRow.appendChild(th);
            theader.appendChild(headerRow);
            result_data_table.appendChild(theader);

            const tbody = document.createElement('tbody');
            parameter_FITS_array.forEach(rowData => {
                const row = document.createElement('tr');
            
                const cell = document.createElement('td');
                cell.textContent = rowData;

                row.appendChild(cell);
                tbody.appendChild(row);
            });  

            result_data_table.appendChild(tbody);

            const tableData = document.getElementById('container-table-parameter-fits');
            tableData.appendChild(result_data_table);
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    }
    else {
        document.getElementById('text-process').innerHTML = 'Select<br>Process';
    }

    // Input Serial Number ****************************************************
    $('#input-sn').on('input', function() {
        try {
            if ($(this).val().length == 9 && edit_active == false) {
                // Create Button SN Indicator >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                handshake_for_hover= [];
                $("#tooltip-new").css({
                    'scale' : '0'
                });
                if (Object.keys(duplicate_index).length == 0) {
                    try {
                        last_button_id = document.querySelectorAll('.sn-indicator')[document.querySelectorAll('.sn-indicator').length - 1].id;
                        last_button_id = `sn-indicator-${(parseInt(last_button_id.split('-')[2]) + 1)}`
                    }
                    catch (e) {
                        last_button_id = 'sn-indicator-0';
                        document.getElementById('container-delete-sn-indicator').style.display = 'block';
                        document.getElementById('container-sn-indicator').style.display = 'flex';
                        document.getElementById('container-initial-button').style.display = 'flex';
                        document.getElementById('button-save').style.display = 'flex';
                        
                        if (operation == 'DEV01') {
                            setTimeout(function() {
                                document.querySelector('.user-container').style.top = '50px';
                            }, 100);
                        }
                    }

                    var button = $('<button>').addClass('sn-indicator').attr({
                        id: last_button_id
                    })
                    
                    $('<p>').text($(this).val()).appendTo(button);

                    $(`<svg class ="svg-button" id="${last_button_id}" width="30px" height="30px" viewBox="0 0 48 48" fill="none" xmlns="http://www.w3.org/2000/svg">` +
                    `<rect width="48" height="48" fill="white" fill-opacity="0.01"/>` +
                    `<path d="M5.32497 43.4998L13.81 43.5L44.9227 12.3873L36.4374 3.90204L5.32471 35.0147L5.32497 43.4998Z" fill="#2F88FF" stroke="#000000" stroke-width="4" stroke-linejoin="round"/>` +
                    `<path d="M27.9521 12.3873L36.4374 20.8726" stroke="#000000" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/>` +
                    `</svg>`).appendTo(button);

                    $('#container-sn-indicator').append(button);

                    $(this).val('');
                    
                    var container_sn_indicator = document.getElementById('container-sn-indicator');
                    container_sn_indicator.scrollTop = container_sn_indicator.scrollHeight - container_sn_indicator.clientHeight;

                    // Check duplicate SN input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    listSN = []
                    listSN_ID = []
                    document.querySelectorAll('.sn-indicator').forEach(function(item) {
                        listSN.push(item.querySelector('p').textContent);
                        listSN_ID.push(item.id)
                        item.style.backgroundColor = 'white'
                        item.querySelector('p').style.color = 'black'
                    });

                    duplicate_index = {}
                    listSN.forEach(function(item, index) {
                        if (listSN.indexOf(item) !== index) {
                            if (!duplicate_index[item]) {
                                duplicate_index[item] = [];
                            } 
                            duplicate_index[item].push(index);
                        }
                    });

                    if (Object.keys(duplicate_index).length > 0) {
                        document.getElementById('tag-fail-duplicate').style.display = 'flex';
                        Object.values(duplicate_index).forEach(val => {
                            val.forEach(idx => {
                                document.getElementById(listSN_ID[idx]).style.background = 'yellow';
                            })
                        })
                    }
                    else{
                        document.getElementById('tag-fail-duplicate').style.display = 'none';
                    }
                }
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }   
    });

    // CLick icon edit at Button SN Indicator to edit ****************************************************
    $(document).on('click', '.svg-button', function() {
        try {
        document.getElementById('revise-button').style.display = 'block';
		
        button_id_for_revise = $(this).attr('id');
		sn_indicator_id_for_delete = button_id_for_revise;
        edit_active = true;
        $('#input-sn').val($(`#${button_id_for_revise} p`).text());

        document.querySelectorAll('.sn-indicator').forEach(function(item) {
            item.style.border = '2px solid black'
          
        })

        document.getElementById(button_id_for_revise).style.border = '4px solid rgb(37 37 160)';
     
        document.getElementById('container-revise-button').style.display = 'block';
        document.getElementById('container-delete-sn-indicator').style.display = 'block';
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    // Confirm editing ****************************************************
    $('#revise-button').click(function () { 
        try {
            handshake_for_hover = [];
            $("#tooltip-new").css({
                'scale' : '0'
            });
            if (button_id_for_revise != null && document.getElementById('input-sn').value.length == 9) {
                edit_active = false;
                $(`#${button_id_for_revise} p`).text($('#input-sn').val());

                document.getElementById('input-sn').style.border = '2px solid #ccc';
                
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    item.style.border = '2px solid black'
                })

                document.getElementById('container-revise-button').style.display = 'none';
                document.getElementById('container-delete-sn-indicator').style.display = 'block';

                $('#input-sn').val('');
                // Check duplicate SN input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                listSN = [];
                listSN_ID = [];
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    listSN.push(item.querySelector('p').textContent);
                    listSN_ID.push(item.id)
                });

                duplicate_index = {}
                listSN.forEach(function(item, index) {
                    if (listSN.indexOf(item) !== index) {
                        if (!duplicate_index[item]) {
                            duplicate_index[item] = [];
                        } 
                        duplicate_index[item].push(index);
                    }
                });
                
                if (Object.keys(duplicate_index).length > 0) {
                    document.getElementById('tag-fail-duplicate').style.display = 'flex';
                    Object.values(duplicate_index).forEach(val => {
                        val.forEach(idx => {
                            document.getElementById(listSN_ID[idx]).style.background = 'yellow';
                        })
                    })
                }
                else{
                    document.getElementById('tag-fail-duplicate').style.display = 'none';
                    document.querySelectorAll('.sn-indicator').forEach(function(item) {
                        item.style.border = '2px solid black';
                        item.style.backgroundColor = 'white'
                        item.querySelector('p').style.color = 'black'
                    })
                }
            }
            else {
                alert('SN lenght is not equal 9')
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    // Delete Button SN Indicator ****************************************************
    $('#delete-sn-indicator').click(function () { 
        try {
			console.log($(this).attr('id'))
			var last_button_id_NEW;
			if (edit_active == true) {
				last_button_id_NEW = button_id_for_revise;
				edit_active = false;
				document.getElementById('container-revise-button').style.display = 'none';
				document.getElementById('container-delete-sn-indicator').style.display = 'block';
				$('#input-sn').val('');
			}
			else {
				last_button_id_NEW = document.querySelectorAll('.sn-indicator')[document.querySelectorAll('.sn-indicator').length - 1].id;
			}
			
            handshake_for_hover= [];
            $("#tooltip-new").css({
                'scale' : '0'
            });
            // *********** Disable the button to prevent multiple clicks ***********
            $('#delete-sn-indicator').prop('disabled', true);
            $(`#${last_button_id_NEW}`).prop('disabled', true);
            
            document.getElementById(last_button_id_NEW).remove();
            // Enable the button
            $('#delete-sn-indicator').prop('disabled', false);

            try {
                last_button_id = document.querySelectorAll('.sn-indicator')[document.querySelectorAll('.sn-indicator').length - 1].id;
            }
            catch (e) {
                document.getElementById('container-delete-sn-indicator').style.display = 'none';
                document.getElementById('container-sn-indicator').style.display = 'none';
                document.getElementById('container-initial-button').style.display = 'none';
                document.getElementById('tag-fail-duplicate').style.display = 'none';
                document.getElementById('tag-fail-badword').style.display = 'none';
                document.getElementById('button-save').style.display = 'none';

                if (operation == 'DEV01') {
                    setTimeout(function() {
                        document.querySelector('.user-container').style.top = '-900px';
                    }, 100);
                }
            }

            // Check duplicate SN input >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            listSN = [];
            listSN_ID = [];
            document.querySelectorAll('.sn-indicator').forEach(function(item) {
                listSN.push(item.querySelector('p').textContent);
                listSN_ID.push(item.id);
                item.style.backgroundColor = 'white'
                item.querySelector('p').style.color = 'black'
            });

            duplicate_index = {}
            listSN.forEach(function(item, index) {
                if (listSN.indexOf(item) !== index) {
                    if (!duplicate_index[item]) {
                        duplicate_index[item] = [];
                    } 
                    duplicate_index[item].push(index);
                }
            });
            
            if (Object.keys(duplicate_index).length > 0) {
                document.getElementById('tag-fail-duplicate').style.display = 'flex';
                Object.values(duplicate_index).forEach(val => {
                    val.forEach(idx => {
                        document.getElementById(listSN_ID[idx]).style.background = 'yellow';
                    })
                })
            }
            else{
                document.getElementById('tag-fail-duplicate').style.display = 'none';
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    item.style.color = 'black';
                    item.style.border = '2px solid black';
                    item.style.background = 'white';
                })
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });
    
    // CLick for initial SN entererd ****************************************************
    $('#initial-button').click(async function () {
        try {
            document.getElementById('loader').style.display = 'block';
            document.getElementById('container-delete-sn-indicator').style.display = 'none';
            document.getElementById('revise-button').style.display = 'none';
            document.getElementById('input-sn').value = '';
            button_id_for_revise = '';
            edit_active = false
            
            // If everything OK, let query data >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            data_handshake = [];
			data_handshake_all = [];
            var value_FITS_array = [];
            value_FITS_text_array = [];
            var map_work_flow = [];
            if (Object.keys(duplicate_index).length == 0 && index_bad_SN.length == 0) {
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    item.style.background = 'white'
                    let span_tooltip = item.querySelector(`#tooltip-sn-indicator-${item.id.split('-')[2]}`);
                    if (span_tooltip) {
                        item.querySelector('p').style.color = 'black';
                        item.removeChild(span_tooltip);
                    }
                })
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    item.style.backgroundColor = 'white'
                    item.style.border = '2px solid black'
                })

                // Query Handshake >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                listSN = []
                listSN_ID = [];
                document.querySelectorAll('.sn-indicator').forEach(function(item) {
                    listSN.push(item.querySelector('p').textContent);
                    listSN_ID.push(item.id)
                });
                
                for (const sn of listSN) {
                    const val = await WebServiceFIts(sn, 'fn_Handshake', '', '', '1', operation);
                    data_handshake.push(val)
                }
                
                // Validate Handshake >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                handshake_for_hover = [];
                for (let i = 0; i < data_handshake.length; i++) {
                    if (data_handshake[i] != 'True') {
                        let span = document.createElement('div');
                        span.className = 'tooltip-sn-indicator';
                        span.id = `tooltip-sn-indicator-${i}`;
                        span.style.backgroundColor = 'yellow';
                        span.style.color = 'black';
                        span.appendChild(document.createTextNode(data_handshake[i]));

                        handshake_for_hover.push(data_handshake[i])
                        
                        document.getElementById(listSN_ID[i]).appendChild(span);
                        document.getElementById(listSN_ID[i]).style.background = 'red';
                        document.getElementById(listSN_ID[i]).querySelector('p').style.color = 'white';
                    }
                    else {
						handshake_for_hover.push('True');
                        let span_tooltip = document.getElementById(listSN_ID[i]).querySelector(`#tooltip-sn-indicator-${i}`);
                        if (span_tooltip) {
                            document.getElementById(listSN_ID[i]).querySelector('p').style.color = 'black';
                            document.getElementById(listSN_ID[i]).removeChild(span_tooltip);
                        }
                        document.getElementById(listSN_ID[i]).style.background = '#00FF17';
                    }
                } 
				data_handshake_all = data_handshake;
                data_handshake = [...new Set(data_handshake)];
                // Preapare value for map with Parameters >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                if (data_handshake.length == 1 && data_handshake[0] == 'True') {
                    // Query dat to FITs and Work Flow of each unit >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    for (let i = 0; i < listSN.length; i++) {
                        let value = (await getWorkFlow(listSN[i]))['data'];
                        for (let j = 0; j < value.length; j++) {
                            if (value[j]['attribute_value'].includes(operation)) {
                                map_work_flow.push(value[j + 1]['attribute_value']);
                            }
                        }

                        let array = [];
                        for (let j = 0; j < parameter_FITS_array.length; j++) {
                            if (parameter_FITS_array[j] == 'FBN Serial No') {
                                array.push(listSN[i]);
                            }
                            else if (parameter_FITS_array[j] == 'send to') {
                                array.push(map_work_flow[i]);
                            }  
							else if (parameter_FITS_array[j] == 'Error Code') {
                                array.push('-');
                            }
                            
                            else {
                                try {
									
									if (process == 'EXP' && parameter_FITS_array[j] == 'Tester Fiber Tx SN') {
										array.push('');					
									}
									else if (process == 'EXP' && parameter_FITS_array[j] == 'Tester Fiber Rx SN') {
										array.push('');	
									}
									else if (process == 'EXS' && parameter_FITS_array[j] == 'Tester Fiber Tx SN') {
										array.push('');	
									}
									else if (process == 'EXS' && parameter_FITS_array[j] == 'Tester Fiber Rx SN') {
										array.push('');	
									}
									else {
										array.push((await getLastTest(parameter_FITS_array[j], listSN[i]))['data'][0]['OUTPUT']);
									}
									
                                }
                                catch {
                                    array.push('');
                                }
                            }
                        }
                        value_FITS_array.push(array);
                    }
					
					
                    // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    const history_data_table = document.getElementById('history_data_table');
                    history_data_table.innerHTML = '';

                    const theader = document.createElement('thead');
                    const headerRow = document.createElement('tr');
                    for (let i = 0; i < value_FITS_array[0].length; i++) {
                        const th = document.createElement('th');
                        th.textContent = parameter_FITS_array[i];
                        headerRow.appendChild(th);
                    }
                    theader.appendChild(headerRow);
                    history_data_table.appendChild(theader);

                    const tbody = document.createElement('tbody');
                    value_FITS_array.forEach(rowData => {
                        const row = document.createElement('tr');
                        rowData.forEach(cellData => {
                            const cell = document.createElement('td');
                            cell.textContent = cellData;
                            row.appendChild(cell);
                        });
                        tbody.appendChild(row);
                    });
                    history_data_table.appendChild(tbody);

                    const tableData = document.getElementById('table-data');
                    tableData.appendChild(history_data_table);

                    setTimeout(function() {
                        document.getElementById('table-data').style.top = '120px';
                    }, 400);

                    // Validate last test queried and Test count >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
                    initial_check = [];
					handshake_for_hover = [];
                    for (let i = 0; i < value_FITS_array.length; i++) {
                        let span_tooltip = document.getElementById(listSN_ID[i]).querySelector(`#tooltip-sn-indicator-${i}`)
                        if (span_tooltip) {
                            document.getElementById(listSN_ID[i]).removeChild(span_tooltip);
                            document.getElementById(listSN_ID[i]).querySelector('p').style.color = 'black';
                        }
                        document.getElementById(listSN_ID[i]).style.background = '#00FF17';
		
                        if (value_FITS_array[i][parameter_FITS_array.indexOf('Result')] == 'PASS') {
                            var value_FITS_text = '';
                            for (let j = 0; j < value_FITS_array[i].length; j++) {
                                value_FITS_text += `,${value_FITS_array[i][j]}`;
                            }

                            value_FITS_text = value_FITS_text.slice(1);
                            value_FITS_text_array.push(value_FITS_text);
							
							handshake_for_hover.push(value_FITS_array[i][parameter_FITS_array.indexOf('Result')])
                            initial_check.push(true);
							
                        }
                        else {
							handshake_for_hover.push(value_FITS_array[i][parameter_FITS_array.indexOf('Result')])

                            let span = document.createElement('div');
                            span.className = 'tooltip-sn-indicator';
                            span.id = `tooltip-sn-indicator-${i}`;
                            span.style.backgroundColor = 'yellow';
                            span.style.color = 'black';
                            span.appendChild(document.createTextNode(value_FITS_array[i][parameter_FITS_array.indexOf('Result')]));
                        
                            document.getElementById(listSN_ID[i]).querySelector('p').style.color = 'black';
                            document.getElementById(listSN_ID[i]).style.background = 'red';
                            document.getElementById(listSN_ID[i]).appendChild(span);
                            initial_check.push(false);
                        }	
                    }
					
                }
            }
            document.getElementById('loader').style.display = 'none';
            document.getElementById('container-delete-sn-indicator').style.display = 'block';
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    // CLick for save data to FITs ****************************************************
    $('#button-save').click(async function() {
        try {
            handshake_for_hover= [];
            $("#tooltip-new").css({
                'scale' : '0'
            });
            // *********** Disable the button to prevent multiple clicks ***********
            $('#button-save').prop('disabled', true);
            // Check out FITs >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
			
            if (initial_check.length > 0 && initial_check.length == data_handshake_all.length) {
                document.getElementById('loader').style.display = 'block';
                result_check_out_FITs = [];
               
				for (let i = 0; i < initial_check.length; i++) {
					if (data_handshake_all[i] == 'True') {
						const result = await WebServiceFIts('', 'fn_Log', parameter_FITS_text, value_FITS_text_array[i], '1', operation);
						result_check_out_FITs.push([listSN[i], result]);
						if (result == 'True') {
							document.getElementById(listSN_ID[i]).style.transition = 'all 0.5s ease';
							document.getElementById(listSN_ID[i]).style.width = '0';
							document.getElementById(listSN_ID[i]).style.height = '0';
							document.getElementById(listSN_ID[i]).style.border = '1px solid black';
							document.getElementById(listSN_ID[i]).querySelector('p').textContent = '';
							setTimeout(function() {
								document.getElementById(listSN_ID[i]).remove();
							}, 350);
						}
					}
				}
			
				// Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
				const result_data_table = document.getElementById('result_data_table');
				result_data_table.innerHTML = '';

				const theader = document.createElement('thead');
				const headerRow = document.createElement('tr');
				var col_th = ['SERIAL_NUMBER', 'RESULT']
				for (let i = 0; i < result_check_out_FITs[0].length; i++) {
					const th = document.createElement('th');
					th.textContent = col_th[i];
					headerRow.appendChild(th);
				}
				theader.appendChild(headerRow);
				result_data_table.appendChild(theader);

				const tbody = document.createElement('tbody');
				result_check_out_FITs.forEach(rowData => {
					const row = document.createElement('tr');
					rowData.forEach(cellData => {
						const cell = document.createElement('td');
						cell.textContent = cellData;
						row.appendChild(cell);
					});
					tbody.appendChild(row);
				});
				result_data_table.appendChild(tbody);

				const tableData = document.getElementById('table-result-data');
				tableData.appendChild(result_data_table);

				setTimeout(function() {
					document.getElementById('table-result-data').style.top = '500px';
				}, 400);	
                
                document.getElementById('loader').style.display = 'none';
            }
            else {
                alert('There is some UNIT not found data in Database yet !')
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });
    // Process selection ****************************************************
    $(".card-process").click(async function() {
        try {
            process = $(this).text();
            if (process == 'FCAL') {
                operation = '2251';
            }
            else if (process == 'OPM') {
                operation = '3105';
            }
            else if (process == 'OPMP') {
                operation = '3106';
            }
            else if (process == 'OPMT') {
                operation = '3107';
            }
            else if (process == 'EXP') {
                operation = '3500';
            }
            else if (process == 'EXS') {
                operation = '3600';
            }
            else if (process == 'LCT1') {
                operation = '2253';
            }
            else if (process == 'LCT2') {
                operation = '2254';
            }
            else if (process == 'LCTT') {
                operation = '2257';
            }
            else if (process == 'DEV01') {
                operation = 'DEV01';
            }

            if (
                process == 'FCAL' ||
                process == 'OPM' ||
                process == 'OPMP' ||
                process == 'OPMT' ||
                process == 'EXP' ||
                process == 'LCT1' ||
                process == 'LCT2' ||
                process == 'LCTT'
                ) 
                {
                model = 'All Module';
            }
    
            else if (process == 'DEV01') {
                model = '*';
            }

            document.getElementById('text-process').textContent = `${process} : ${operation}`;

            // Set local memmory
            localStorage.setItem("text_process", `${process} : ${operation}`)

            var data = await getParamFITs();

            parameter_FITS_array = [];
            for (let i = 0; i < data['data'].length; i++) {
                if (data['data'][i]['PARAMETER'] != 'Lid RT & SN') {
                    parameter_FITS_array.push(data['data'][i]['PARAMETER']);
                }
                else {
                    parameter_FITS_array.push('Lid RT _SN');
                }
            }

            parameter_FITS_text = '';
            for (let i = 0; i < parameter_FITS_array.length; i++) {
                parameter_FITS_text += `,${parameter_FITS_array[i]}`;
            }
            parameter_FITS_text = parameter_FITS_text.slice(1);

            // Insert data to Table >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>
            const result_data_table = document.getElementById('table-parameter-fits');
            result_data_table.innerHTML = '';

            const theader = document.createElement('thead');
            const headerRow = document.createElement('tr');
    
            const th = document.createElement('th');
            th.textContent = 'Parameter';
            
            headerRow.appendChild(th);
            theader.appendChild(headerRow);
            result_data_table.appendChild(theader);

            const tbody = document.createElement('tbody');
            parameter_FITS_array.forEach(rowData => {
                const row = document.createElement('tr');
            
                const cell = document.createElement('td');
                cell.textContent = rowData;

                row.appendChild(cell);
                tbody.appendChild(row);
            });  
    
            result_data_table.appendChild(tbody);

            const tableData = document.getElementById('container-table-parameter-fits');
            tableData.appendChild(result_data_table);
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    // Menu Setting ****************************************************
    $('.menu-1').click(async function() {
        setTimeout(function() {
            document.getElementById('container-table-parameter-fits').style.top = '100px';
            document.getElementById('container-table-parameter-fits').style.left = '520px';
            document.getElementById('container-table-parameter-fits').style.width = 'auto';
            document.getElementById('container-table-parameter-fits').style.height = '600px';
        }, 200);
    })
    
    $('.menu-2').click(async function() {
        
        document.getElementById('container-LC-fits').style.opacity = '1';
    });

    // Get date from day selected
    $('.calendar-body').click(function() {
        try {
            var days = document.querySelectorAll('.calendar-body .calendar-days div');
            days.forEach(function(day) {
                day.addEventListener('click', function() {
                    // Remove any existing 'selected' class
                    document.querySelectorAll('.calendar-body .calendar-days div').forEach(function(day) {
                        day.classList.remove('selected');
                    });

                    // Add 'selected' class to the clicked day
                    day.classList.add('selected');

                    // Get the selected day, month, and year
                    var selectedDay = day.textContent.trim();
                    var selectedMonth = document.getElementById('month-picker').textContent.trim();
                    var selectedYear = document.getElementById('year').textContent.trim();

                    // Format the selected date as MM/DD/YY
                    var formattedDate = formatDate(selectedMonth, selectedDay, selectedYear);

                    var calendar = $('.calendar');
                    if (calendar.offset().top == 390) {
                        $(`#input-dev-effective-date`).text(formattedDate);
                    }
                    else if (calendar.offset().top == 450) {
                        $(`#input-dev-end-date`).text(formattedDate);
                    }

                    if (formattedDate.length > 0) {
                        document.querySelector('.calendar').style.width = '0';
                        document.querySelector('.calendar').style.height = '0';
                        document.querySelector('.calendar').style.background = 'transparent';
                        document.querySelector('.calendar').style.boxShadow = 'none';
                    }
                });
            });

            function formatDate(month, day, year) {
                var monthIndex = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'].indexOf(month);
                var formattedMonth = ('0' + (monthIndex + 1)).slice(-2);
                var formattedDay = ('0' + day).slice(-2);
                var formattedYear = ('' + year).slice(-2);
                return formattedMonth + '/' + formattedDay + '/' + formattedYear;
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });
    
    $('#effective-date_bt').click(async function() {
        document.querySelector('.calendar').style.width = '0';
        document.querySelector('.calendar').style.height = '0';
        setTimeout(function() {
            document.querySelector('.calendar').style.top = '390px';
            document.querySelector('.calendar').style.left = '750px';
            document.querySelector('.calendar').style.width = '290px';
            document.querySelector('.calendar').style.height = '25rem';
            document.querySelector('.calendar').style.background = 'white';
            document.querySelector('.calendar').style.boxShadow = 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px';
        }, 300);
    });

    $('#end-date_bt').click(async function() {
        document.querySelector('.calendar').style.width = '0';
        document.querySelector('.calendar').style.height = '0';
        setTimeout(function() {
            document.querySelector('.calendar').style.top = '450px';
            document.querySelector('.calendar').style.left = '750px';
            document.querySelector('.calendar').style.width = '290px';
            document.querySelector('.calendar').style.height = '25rem';
            document.querySelector('.calendar').style.background = 'white';
            document.querySelector('.calendar').style.boxShadow = 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px';
        }, 300);
    });

    $('#model_bt').click(async function() {
        try {
            const data = (await getModel())['data']
            const array = [];
            for (let i = 0; i < data.length; i++) {
                array.push(data[i]['buildtype']);
            }
            array.sort()

            const container = document.getElementById('dropdown-model');

            document.querySelectorAll('.model-bt-class').forEach(function(element) {
                element.remove();
            });

            container.style.height = '150px';
            container.style.zIndex = '2';
            container.style.boxShadow = 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px';

            for (let i = 0; i < array.length; i++) {
                let button = document.createElement('button');
                button.id = `model-bt-${i}`;
                button.className = 'model-bt-class';
                button.style.height = '30px';
                button.textContent = array[i];

                container.appendChild(button);
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    $(document).on('click', '.model-bt-class', function() {
        document.querySelectorAll('.model-bt-class').forEach(function(element) {
            element.remove();
        });
        document.getElementById('dropdown-model').style.height = '0';
        $(`#input-dev-model`).text($(this).text());
    }); 

    $('#pn_bt').click(async function() {
        try {
            const data = (await getPN())['data']
            const array = [];
            for (let i = 0; i < data.length; i++) {
                array.push(data[i]['part_no']);
            }
            array.sort()

            const container = document.getElementById('dropdown-pn');

            document.querySelectorAll('.pn-bt-class').forEach(function(element) {
                element.remove();
            });

            container.style.height = '150px';
            container.style.boxShadow = 'rgba(100, 100, 111, 0.2) 0px 7px 29px 0px';

            for (let i = 0; i < array.length; i++) {
                let button = document.createElement('button');
                button.id = `pn-bt-${i}`;
                button.className = 'pn-bt-class';
                button.style.height = '30px';
                button.textContent = array[i];

                container.appendChild(button);
            }
        }
        catch (e) {
            $('#error-pop-up').html(`! ${e.message} ! <br> ${e.lineNumber || e.line}`);
            $("#error-pop-up").css({
                'scale' : '1'
            });
            console.warn(e) 
        }
    });

    $(document).on('click', '.pn-bt-class', function() {
        document.querySelectorAll('.pn-bt-class').forEach(function(element) {
            element.remove();
        });
        document.getElementById('dropdown-pn').style.height = '0';
        $(`#input-dev-pn`).text($(this).text());
    });

    $(document).on('click', '#bt-LC-1-time', function() {
        document.querySelector('.page-for-LC-1-time').style.height = '200px';
        document.getElementById('check-in-LC-1-time').style.display = 'block';
    });

    $(document).on('click', '#bt-LC-3-times', function() {
        document.querySelector('.page-for-LC-3-times').style.height = '200px';
        document.getElementById('container-input-LC-SN-3-times').style.display = 'flex';
    });

    $(document).on('click', '#check-in-LC-1-time', async function() {
        if ($('#input-LC-SN-1-time').val() != '' && $('#input-EN-1-time').val() != '') {
            const result_check_in = await WebServiceFIts('', 'fn_Log', 'Fixture ID', $('#input-LC-SN-1-time').val(), '0', '9965');
            const result_check_out = await WebServiceFIts('', 'fn_Log', 'Fixture ID,EN,Result,Remark', `${$('#input-LC-SN-1-time').val()},${$('#input-EN-1-time').val()},PASS,GOOD`, '1', '9965');
            const result_check_release = await WebServiceFIts('', 'fn_Log', 'Fixture ID,EN,Result,Reason for release', `${$('#input-LC-SN-1-time').val()},${$('#input-EN-1-time').val()},PASS,GOOD`, '1', '9967');

            console.log(result_check_in)
            console.log(result_check_out)
            console.log(result_check_release)
        }
    });

    // Click another area to close widget
    $(document).mouseup(function (e) { 
        var table = $('#table-parameter-fits');
        var menu_process = $('.card-process');
        var calendar = $('.calendar');
        var dropdown_model = $('#dropdown-model');
        var dropdown_pn = $('#dropdown-pn');
        var LC_fits = $('#container-LC-fits');

        var LC_fits_button_1 = $('#bt-LC-1-time');
        var LC_fits_button_3 = $('#bt-LC-3-times');
        
        if (!table.is(e.target) && table.has(e.target).length == 0 && !menu_process.is(e.target)) {
            document.getElementById('container-table-parameter-fits').style.top = '260px';
            document.getElementById('container-table-parameter-fits').style.left = '370px';
            document.getElementById('container-table-parameter-fits').style.width = '0';
            document.getElementById('container-table-parameter-fits').style.height = '0';
            document.getElementById('container-table-parameter-fits').style.transition = '0.5s ease';
        }
        
        if (calendar.width() == 290) {
            if (!calendar.is(e.target) && calendar.has(e.target).length == 0) {
                document.querySelector('.calendar').style.width = '0';
                document.querySelector('.calendar').style.height = '0';
                document.querySelector('.calendar').style.background = 'transparent';
                document.querySelector('.calendar').style.boxShadow = 'none';
            }
        }

        if (!dropdown_model.is(e.target) && dropdown_model.has(e.target).length == 0) {
            document.querySelectorAll('.model-bt-class').forEach(function(element) {
                element.remove();
            });
            document.getElementById('dropdown-model').style.height = '0';
        }

        if (!dropdown_pn.is(e.target) && dropdown_pn.has(e.target).length == 0) {
            document.querySelectorAll('.pn-bt-class').forEach(function(element) {
                element.remove();
            });
            document.getElementById('dropdown-pn').style.height = '0';
        }

        if (!LC_fits.is(e.target) && LC_fits.has(e.target).length == 0) {
            document.getElementById('container-LC-fits').style.opacity = '0';
            document.querySelector('.page-for-LC-1-time').style.height = '0';
            document.getElementById('check-in-LC-1-time').style.display = 'none';
            document.querySelector('.page-for-LC-3-times').style.height = '0';
            document.getElementById('container-input-LC-SN-3-times').style.display = 'none';
        }

        if (LC_fits_button_3.is(e.target)) {
            document.querySelector('.page-for-LC-1-time').style.height = '0';
            document.getElementById('check-in-LC-1-time').style.display = 'none';
        }

        if (LC_fits_button_1.is(e.target)) {
            document.querySelector('.page-for-LC-3-times').style.height = '0';
            document.getElementById('container-input-LC-SN-3-times').style.display = 'none';
        }
    });

    // ******************************************** Query Zone ********************************************
    async function getParamFITs() {
        try {
            // !!! use "<NAME_OF_YOUR_SITE>/get-param-fits?"
            const response = await fetch(`/get-param-fits?operation=${operation}`);
            const dataJSON = await response.json();
            return dataJSON;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async function getLastTest(parameter, sn) {
        try {
            // !!! use "<NAME_OF_YOUR_SITE>/get-last-test?"
            const response = await fetch(`/get-last-test?parameter=${parameter}&sn=${sn}&process=${process}`);
            const dataJSON = await response.json();
            return dataJSON;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async function getWorkFlow(sn) {
        try {
            // !!! use "<NAME_OF_YOUR_SITE>/get-workflow?"
            const response = await fetch(`/get-workflow?serialnumber=${sn}`);
            const dataJSON = await response.json();
            return dataJSON;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async function getModel() {
        try {
            // !!! use "<NAME_OF_YOUR_SITE>/get-model?"
            const response = await fetch(`/get-model`);
            const dataJSON = await response.json();
            return dataJSON;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async function getPN() {
        try {
            // !!! use "<NAME_OF_YOUR_SITE>/get-pn?"
            const response = await fetch(`/get-pn`);
            const dataJSON = await response.json();
            return dataJSON;
        } catch (error) {
            console.error('Error:', error);
            throw error;
        }
    }

    async function WebServiceFIts(sn, type, parameter, value, rev, oper) {
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

    const isLeapYear = (year) => {
        return (
            (year % 4 === 0 && year % 100 !== 0 && year % 400 !== 0) ||
            (year % 100 === 0 && year % 400 === 0)
        );
    };

    const getFebDays = (year) => {
        return isLeapYear(year) ? 29 : 28;
    };

    let calendar = document.querySelector('.calendar');
    const month_names = [
        'January',
        'February',
        'March',
        'April',
        'May',
        'June',
        'July',
        'August',
        'September',
        'October',
        'November',
        'December',
    ];

    let month_picker = document.querySelector('#month-picker');
    const dayTextFormate = document.querySelector('.day-text-formate');
    const timeFormate = document.querySelector('.time-formate');
    const dateFormate = document.querySelector('.date-formate');
        
    month_picker.onclick = () => {
        month_list.classList.remove('hideonce');
        month_list.classList.remove('hide');
        month_list.classList.add('show');
        dayTextFormate.classList.remove('showtime');
        dayTextFormate.classList.add('hidetime');
        timeFormate.classList.remove('showtime');
        timeFormate.classList.add('hideTime');
        dateFormate.classList.remove('showtime');
        dateFormate.classList.add('hideTime');
    };
        
    const generateCalendar = (month, year) => {
        let calendar_days = document.querySelector('.calendar-days');
        calendar_days.innerHTML = '';
        let calendar_header_year = document.querySelector('#year');
        let days_of_month = [
            31,
            getFebDays(year),
            31,
            30,
            31,
            30,
            31,
            31,
            30,
            31,
            30,
            31,
        ];
        
        let currentDate = new Date();
        
        month_picker.innerHTML = month_names[month];
        
        calendar_header_year.innerHTML = year;
        
        let first_day = new Date(year, month);
        
        
        for (let i = 0; i <= days_of_month[month] + first_day.getDay() - 1; i++) {
        
            let day = document.createElement('div');
        
            if (i >= first_day.getDay()) {
            day.innerHTML = i - first_day.getDay() + 1;
        
            if (i - first_day.getDay() + 1 === currentDate.getDate() &&
                year === currentDate.getFullYear() &&
                month === currentDate.getMonth()
            ) {
                day.classList.add('current-date');
            }
            }
            calendar_days.appendChild(day);
        }
    };
        
    let month_list = calendar.querySelector('.month-list');
    month_names.forEach((e, index) => {
        let month = document.createElement('div');
        month.innerHTML = `<div>${e}</div>`;
        
        month_list.append(month);
        month.onclick = () => {
            currentMonth.value = index;
            generateCalendar(currentMonth.value, currentYear.value);
            month_list.classList.replace('show', 'hide');
            dayTextFormate.classList.remove('hideTime');
            dayTextFormate.classList.add('showtime');
            timeFormate.classList.remove('hideTime');
            timeFormate.classList.add('showtime');
            dateFormate.classList.remove('hideTime');
            dateFormate.classList.add('showtime');
        };
    });
        
    (function() {
    month_list.classList.add('hideonce');
    })();

    document.querySelector('#pre-year').onclick = () => {
        --currentYear.value;
        generateCalendar(currentMonth.value, currentYear.value);
    };

    document.querySelector('#next-year').onclick = () => {
        ++currentYear.value;
        generateCalendar(currentMonth.value, currentYear.value);
    };
        
    let currentDate = new Date();
    let currentMonth = { value: currentDate.getMonth() };
    let currentYear = { value: currentDate.getFullYear() };
    generateCalendar(currentMonth.value, currentYear.value);
    
    const todayShowTime = document.querySelector('.time-formate');
    const todayShowDate = document.querySelector('.date-formate');
    
    const currshowDate = new Date();
    const showCurrentDateOption = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        weekday: 'long',
    };

    const currentDateFormate = new Intl.DateTimeFormat(
        'en-US',
        showCurrentDateOption
    ).format(currshowDate);

    todayShowDate.textContent = currentDateFormate;
    setInterval(() => {
        const timer = new Date();
        const option = {
            hour: 'numeric',
            minute: 'numeric',
            second: 'numeric',
        };
        const formateTimer = new Intl.DateTimeFormat('en-us', option).format(timer);
        let time = `${`${timer.getHours()}`.padStart(
            2,
            '0'
            )}:${`${timer.getMinutes()}`.padStart(
            2,
            '0'
            )}: ${`${timer.getSeconds()}`.padStart(2, '0')}`;
        todayShowTime.textContent = formateTimer;
    }, 1000);
})

