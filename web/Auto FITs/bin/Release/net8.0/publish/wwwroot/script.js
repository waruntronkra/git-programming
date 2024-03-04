var byProcess = '';
var runByProcess_Activate = false;
var doubleClickProcess = false;
var selectedProduct = '';
var selectedModel = '';
$(document).ready(function() {
    // ================================== Tab Click ==================================
    $('.tabLinks').click(function () {
        document.querySelectorAll('.tabLinks').forEach(element => {
            element.style.backgroundColor = 'white';
        })
        this.style.backgroundColor = '#08cc77';

        document.getElementById('myLineChart').style.display = 'none';
        document.getElementById('myMixChart').style.display = 'none';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        document.getElementById('matrix_table').style.display = 'none';
        document.getElementById('raw_data_table').style.display = 'none';
        document.getElementById('history_data_table').style.display = 'none';
        document.getElementById('pareto_data_table').style.display = 'none';

        if (this.id === 'button_1') {
            $('#myLineChart').css({'display': 'block'})
            $('#matrix_table').css({'display': 'block'})
        }
        else if (this.id === 'button_2') {
            $('#myParetoChart').css({'display': 'block'})
            $('#pareto_data_table').css({'display': 'block'})
        }
        else if (this.id === 'button_3') {
            $('#myMixChart').css({'display': 'block'})
            $('#raw_data_table').css({'display': 'block'})
        }
        else if (this.id === 'button_4') {
            $('#history_data_table').css({'display': 'block'})
        }
    });

    // ================================== Clik for run [All Process] ==================================
    $('.btn--huge').click(function () {
        runByProcess_Activate = false;
        doubleClickProcess = false;
        byProcess = '';

        selectedProduct = this.id.split(':')[0];
        selectedModel = this.id.split(':')[1];

        document.querySelectorAll('.sub-menu-zephyr').forEach(element => {
            element.style.display = 'none';
        })
        document.querySelectorAll('.sub-menu-process').forEach(element => {
            element.style.display = 'none';
        });

        document.querySelectorAll('.sub-menu-non-ac1200').forEach(element => {
            element.style.display = 'none';
        })
        document.querySelectorAll('.sub-menu-ac1200').forEach(element => {
            element.style.display = 'none';
        })
        document.querySelectorAll('.sub-menu-jannu').forEach(element => {
            element.style.display = 'none';
        })

        document.querySelectorAll('.tabLinks').forEach(element => {
            element.style.backgroundColor = 'white';
        })
        document.getElementById('button_1').style.backgroundColor = '#08cc77';

        document.getElementById('myLineChart').style.display = 'block';
        document.getElementById('myMixChart').style.display = 'none';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        document.getElementById('matrix_table').style.display = 'block';
        document.getElementById('raw_data_table').style.display = 'none';
        document.getElementById('history_data_table').style.display = 'none';
        document.getElementById('pareto_data_table').style.display = 'none';
 
        $('#productName_label').text('Product: ' + selectedProduct + ' [' + selectedModel + ']');
        $('#' + this.id.split(':')[2] + '-submenu').toggle();

        // Clear Line Chart
        if (lineChart) {
            lineChart.data.labels = [];
            lineChart.data.datasets = [];
            lineChart.update();
        }
        fetchData();
    });

    // ================================== Clik for run [By Process] [Button] ==================================
    $('.BT_process').click(function() {
        runByProcess_Activate = true;
        doubleClickProcess = false;

        byProcess = $(this).text().split(' ')[1];

        document.querySelectorAll('.sub-menu-process').forEach(element => {
            element.style.display = 'none';
        });
        document.getElementById(this.id.split('_')[1]).style.display = 'block';

        document.querySelectorAll('.tabLinks').forEach(element => {
            element.style.backgroundColor = 'white';
        });
        document.getElementById('button_1').style.backgroundColor = '#08cc77';

        document.getElementById('myLineChart').style.display = 'none';
        document.getElementById('myMixChart').style.display = 'block';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        document.getElementById('matrix_table').style.display = 'block';
        document.getElementById('raw_data_table').style.display = 'none';
        document.getElementById('history_data_table').style.display = 'none';
        document.getElementById('pareto_data_table').style.display = 'none';
 
        // Clear Mix Chart
        if (mixChart) {
            mixChart.data.labels = [];
            mixChart.data.datasets[0].data = [];
            mixChart.data.datasets[1].data = [];
            mixChart.data.datasets[2].data = [];
            mixChart.data.datasets[2].qty = [];
            mixChart.update();
        }
        fetchData();
    });
    // ================================== Clik for run [By Column Name] [Button] ==================================
    $('.BT_sub_menu_process').click(function() {
        fetchValueByColName($(this).text());
    })

    // ================================== Clik for run [By Process] [Double CLick] ==================================
    // $(document) in case that widget doesn't create and has been created after Javascript
    $(document).on('dblclick', '#matrix_table td', function() {
        if ($(this).text() !== '') {
            document.querySelectorAll('.tabLinks').forEach(element => {
                element.style.backgroundColor = 'white';
            })
            document.getElementById('button_3').style.backgroundColor = '#08cc77';
            
            document.getElementById('myLineChart').style.display = 'none';
            document.getElementById('myMixChart').style.display = 'block';
            document.getElementById('myParetoChart').style.display = 'none';
            document.getElementById('myParetoFailChart').style.display = 'none';
            document.getElementById('myMixChartSecond').style.display = 'none';
            
            document.getElementById('matrix_table').style.display = 'none';
            document.getElementById('raw_data_table').style.display = 'block';
            document.getElementById('history_data_table').style.display = 'none';
            document.getElementById('pareto_data_table').style.display = 'none';

            doubleClickProcess = true;

            byProcess = $(this).closest('tr').find('th:first').text(); // Row Header

            var aboveRow;
            if (byProcess === '') {
                var rowIndex = $(this).closest('tr').index();
                for (let i = 1; i < 5; i++) {
                    aboveRow = $(this).closest('tr').parent().find('tr').eq(rowIndex - i);
                    if (aboveRow.find('th:first').text() !== '') {
                        break;
                    }
                }
                byProcess = aboveRow.find('th:first').text();
            }
            
            if (this.className === "for_pareto") {
                Pareto_Chart();
            }
            else {
                var colIndex = parseInt($(this).index() / 6) + 1; 
                // Clear Mix Chart
                if (mixChart) {
                    mixChart.data.labels = [];
                    mixChart.data.datasets[0].data = [];
                    mixChart.data.datasets[1].data = [];
                    mixChart.data.datasets[2].data = [];
                    mixChart.data.datasets[2].qty = [];
                    mixChart.update();
                }
                
                fetchData();
                queryHistorybyLegend($('#matrix_table thead tr:first th').eq(colIndex).text()); // Column Header
            }
        }
    });
    
    $(document).on('click', '#pareto_data_table tr:first th', function() {
        paretoSelectCell('', '', $('#pareto_data_table tr:first th').eq($(this).index()).text())
    });
})

selectedDays = '1';
modeDayOption = 'DATE';
function day_selected(value, mode_day) {
    if (runByProcess_Activate === true) {
        document.getElementById('myLineChart').style.display = 'none';
        document.getElementById('myMixChart').style.display = 'block';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        document.getElementById('matrix_table').style.display = 'block';
        document.getElementById('raw_data_table').style.display = 'none';
        document.getElementById('history_data_table').style.display = 'none';
        document.getElementById('pareto_data_table').style.display = 'none';
    }
    else {
        document.getElementById('myLineChart').style.display = 'block';
        document.getElementById('myMixChart').style.display = 'none';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        document.getElementById('matrix_table').style.display = 'block';
        document.getElementById('raw_data_table').style.display = 'none';
        document.getElementById('history_data_table').style.display = 'none';
        document.getElementById('pareto_data_table').style.display = 'none';
    }

    document.querySelectorAll('.tabLinks').forEach(element => {
        element.style.backgroundColor = 'white';
    })
    document.getElementById('button_1').style.backgroundColor = '#08cc77';

    if (mode_day === 'DATE') {
        mode_show = ' Days'
    }
    else if (mode_day === 'WEEK') {
        mode_show = ' Weeks'
    }
    else if (mode_day === 'MONTH') {
        mode_show = ' Months'
    }
    else if (mode_day === 'QUARTER') {
        mode_show = ' Quarters'
    }

    selectedDay_Label = parseInt(value) + 1;
    document.getElementById('label_day_selected').textContent = String(selectedDay_Label) + mode_show;

    selectedDays = value;
    modeDayOption = mode_day;
    doubleClickProcess = false
    
    if (runByProcess_Activate === false) {
        byProcess = '';
    } 
    fetchData();
}

// Function to fetch data
var lineChart;
var mixChart;
function fetchData() {
    if (modeDayOption === 'DATE') {
        mode_show = ' Days'
    }
    else if (modeDayOption === 'WEEK') {
        mode_show = ' Weeks'
    }
    else if (modeDayOption === 'MONTH') {
        mode_show = ' Months'
    }
    else if (modeDayOption === 'QUARTER') {
        mode_show = ' Quarters'
    }
    selectedDay_Label = parseInt(selectedDays) + 1;
    document.getElementById('label_day_selected').textContent = String(selectedDay_Label) + mode_show;
    $('#loader').css({'display': 'block'});

    fetch(
        `/fetch_data?` +
        `days=${selectedDays}` +
        `&selected_Product=${selectedProduct}` +
        `&selected_Model=${selectedModel}` +
        `&mode_day_option=${modeDayOption}` + 
        `&by_Process=${byProcess}`
        )
        .then(response => response.json())
        .then(dataJSON => {
            console.log("DATA", dataJSON)
            const dataAll = dataJSON.data;
            if (dataAll.length > 0) {
                const data = [];
                for (var i = 0; i < dataAll.length; i++) {
                    var val = dataAll[i];
                    data.push([
                        val.Process, 
                        val[modeDayOption],
                        val.FPY,
                        val.QTY,
                        val.RTY,
                        val.Pareto,
                        val.Fail,
                        val.Pass,
                        parseInt(val.QTY) - parseInt(val.Pass),
                        val.Model,
                        val['%']
                    ]);
                }
                
                // ======================== Plot Line Chart ========================
                var dates = [...new Set(data.map(item => item[1]))];
                if (modeDayOption === 'D'|| modeDayOption === 'M') {
                    dates.sort(function(a, b) { // Sort data aecending
                        // Convert the date strings to JavaScript Date objects for comparison
                        var dateA = new Date(a);
                        var dateB = new Date(b);
                    
                        // Compare the dates
                        return dateA - dateB;
                    });
                }
                var datasets = [];
                data.forEach(processData => {
                    var legendName;
                    if (modeRunAll_HW === true) {
                        legendName = processData[9]; // legend name
                    }
                    else {
                        legendName = processData[0]; // legend name
                    }
                    var date = processData[1]; // x
                    var value = parseFloat(processData[2]); // y
                    var quantity = parseInt(processData[3]); // other data
                    var passed_units = parseInt(processData[7]);
                    var failed_units = parseInt(processData[8]);

                    // Find or create dataset for the process
                    var dataset = datasets.find(ds => ds.label === legendName);
                    if (!dataset) {
                        dataset = {
                            label: legendName,
                            data: [],
                            quantity: [],
                            passed: [],
                            failed: [],
                            fill: false,
                            borderColor: getRandomColor(),
                            borderWidth: 2,
                            lineTension: 0,
                        };
                        datasets.push(dataset);
                    } 

                    var dateIndex = dates.indexOf(date);

                    if (dateIndex === -1) {
                        dates.push(date);
                        dateIndex = dates.indexOf(date);
                    }
                    dataset.data[dateIndex] = value;
                    dataset.quantity[dateIndex] = quantity;
                    dataset.passed[dateIndex] = passed_units;
                    dataset.failed[dateIndex] = failed_units;
                });

                function getRandomColor() {
                    var letters = '0123456789ABCDEF';
                    var color = '#';
                    for (var i = 0; i < 6; i++) {
                        color += letters[Math.floor(Math.random() * 16)];
                    }
                    return color;
                }
        
                if (runByProcess_Activate === false && doubleClickProcess === false) {
                    if (!lineChart) {
                        var ctx = document.getElementById('myLineChart').getContext('2d');
                        lineChart = new Chart(ctx, {
                            type: 'line',
                            data: {
                                labels: dates,
                                datasets: datasets.map(dataset => ({
                                    ...dataset,
                                    pointStyle: 'circle',
                                    pointRadius: 5
                                })),
                            },
                            options: {
                                responsive: true,
                                maintainAspectRatio: false,
                                
                                title: {
                                    display: true,
                                    text: 'Line Chart'
                                },
                                scales: {
                                    x: {
                                        offset: true,
                                        title: {
                                            display: true,
                                            text: 'DATE',
                                            color: '#FFFFFF',
                                            font: {
                                                size: 15,
                                                family: 'Century Gothic',
                                                weight: 'bold'
                                            }
                                        },
                                        ticks: {
                                            color: '#FFFFFF'
                                        }
                                    },
                                    y: {
                                        title: {
                                            display: true,
                                            text: 'Yield (%)',
                                            color: '#FFFFFF',
                                            font: {
                                                size: 15,
                                                family: 'Century Gothic',
                                                weight: 'bold'
                                            }
                                        },
                                        ticks: {
                                            color: '#FFFFFF'
                                        }
                                    }
                                },
                                plugins: {
                                    legend: {
                                        position: 'right',
                                        labels: {
                                            boxWidth: 30,
                                            boxHeight: 2,
                                            color: '#FFFFFF'
                                        },
                                        onClick: function (e, legendItem) {
                                            document.getElementById('myLineChart').style.display = 'none';
                                            document.getElementById('myMixChart').style.display = 'none';
                                            document.getElementById('myParetoChart').style.display = 'none';
                                            document.getElementById('myParetoFailChart').style.display = 'none';
                                            document.getElementById('myMixChartSecond').style.display = 'block';
                                    
                                            // Clear Mix Chart
                                            if (myMixChartSecond) {
                                                myMixChartSecond.data.labels = [];
                                                myMixChartSecond.data.datasets[0].data = [];
                                                myMixChartSecond.data.datasets[1].data = [];
                                                myMixChartSecond.data.datasets[2].data = [];
                                                myMixChartSecond.data.datasets[2].qty = [];
                                                myMixChartSecond.update();
                                            }
                                            fetchData_Second(legendItem.text);
                                          },
                                    },
                                    title: {
                                        display: true,
                                        text: `ATS YIELD : ${selectedModel}`,
                                        color: '#FFFFFF',
                                        font: {
                                            size: 15,
                                            family: 'Century Gothic',
                                            weight: 'bold'
                                        }
                                    },
                                    tooltip: {
                                        mode: 'index',
                                        intersect: false,
                                        callbacks: {
                                            title: function (context) {
                                                return context[0].label;
                                            },
                                            label: function (context) {
                                                var dataLabel = context.dataset.label;
                                                var val = context.raw;
                                                var qty = context.dataset.quantity[context.dataIndex];
                                                var qty_passed = context.dataset.passed[context.dataIndex];
                                                var qty_failed = context.dataset.failed[context.dataIndex];
                                                return `${dataLabel} : ${val} % | Qty : ${qty} | PASS : ${qty_passed} | FAIL : ${qty_failed}`
                                            }
                                        }
                                    }
                                }
                            }
                        });
                    } 

                    else {
                        lineChart.data.labels = dates;
                        lineChart.data.datasets = datasets;
                        lineChart.options.plugins.title.text = `ATS YIELD : ${selectedModel}`;
                        lineChart.update();
                    }
                }
                // ======================== Plot Mix Chart ========================
                if (runByProcess_Activate === true || doubleClickProcess === true) {
                    const data_all_mix = {labels: [], quantity: []} 
                    var datasets_line_chart = [];
                    data.forEach(processData => {
                        var legendName;
                        if (modeRunAll_HW === true) {
                            legendName = processData[9]; // legend name
                        }
                        else {
                            legendName = processData[0]; // legend name
                        }
                        var date = processData[1]; // x
                        var value = parseFloat(processData[2]); // y
                        var quantity = parseInt(processData[3]); // other data
                        var passed_units = parseInt(processData[7]);
                        var failed_units = parseInt(processData[8]);
                        
                        // Find or create dataset for the process
                        var dataset_line = datasets_line_chart.find(ds => ds.label === legendName);
                        if (!dataset_line) {
                            dataset_line = {
                                type: 'line',
                                label: legendName,
                                data: [],
                                passed: [],
                                failed: [],
                                quantity: [],
                                fill: false,
                                borderColor: getRandomColor(),
                                borderWidth: 2,
                                lineTension: 0,
                            };
                            datasets_line_chart.push(dataset_line);
                        } 

                        var dateIndex = dates.indexOf(date);
                        if (dateIndex === -1) {
                            dates.push(date);
                            dateIndex = dates.indexOf(date);
                        }

                        dataset_line.data[dateIndex] = value;
                        dataset_line.quantity[dateIndex] = quantity;
                        dataset_line.passed[dateIndex] = passed_units;
                        dataset_line.failed[dateIndex] = failed_units;

                        data_all_mix.labels[dateIndex] = date;
                    });

                    const arr_data = [];
                    const arr_data_passed = [];
                    const arr_data_failed = [];

                    datasets_line_chart.forEach(val => {
                        arr_data.push(val.data);
                        arr_data_passed.push(val.passed);
                        arr_data_failed.push(val.failed);
                    });
                    var new_arr_data = arr_data.pop();
                    var new_arr_data_passed = arr_data_passed.pop();
                    var new_arr_data_failed = arr_data_failed.pop();
                    
                    var merge_chart = {
                        labels: data_all_mix.labels,
                        datasets: [
                            {
                                label: 'PASS',
                                backgroundColor: 'rgba(39, 255, 0, 0.5)',
                                data: new_arr_data_passed
                            },
                            {
                                label: 'FAIL',
                                backgroundColor: 'rgba(255, 0, 0, 0.5)',
                                data: new_arr_data_failed
                            },
                            {
                                label: byProcess,
                                type: 'line',
                                fill: false,
                                backgroundColor: '#AE00FF',
                                borderColor: '#AE00FF',
                                yAxisID: 'line-axis',
                                data: new_arr_data,
                                qty: datasets_line_chart[0].quantity
                            }
                        ]
                    };
                    
                    if (!mixChart) {
                        var ctx_mix = document.getElementById('myMixChart').getContext('2d');
                        mixChart = new Chart(ctx_mix, {
                            type: 'bar',
                            data: merge_chart,
                            options: {
                                responsive: true,
                                scales: {
                                    x: {
                                        stacked: true,
                                        offset: true,
                                        title: {
                                            display: true,
                                            text: 'DATE',
                                            color: '#FFFFFF',
                                            font: {
                                                size: 15,
                                                family: 'Century Gothic',
                                                weight: 'bold'
                                            }
                                        },
                                        ticks: {
                                            color: '#FFFFFF'
                                        }
                                    },
                                    y: {
                                        stacked: true,
                                        title: {
                                            display: false,
                                            color: '#FFFFFF',
                                            font: {
                                                size: 15,
                                                family: 'Century Gothic',
                                                weight: 'bold'
                                            }
                                        },
                                        ticks: {
                                            color: '#FFFFFF'
                                        }
                                    },
                                    'line-axis': {
                                        type: 'linear',
                                        position: 'right',
                                        display: true,
                                        color: '#FFFFFF',
                                        font: {
                                            size: 15,
                                            family: 'Century Gothic',
                                            weight: 'bold'
                                        },
                                        ticks: {
                                            color: '#FFFFFF'
                                        }
                                    }
                                },
                                plugins: {
                                    tooltip: {
                                        mode: 'index', // Display multiple tooltips at once
                                        intersect: false,
                                        callbacks: {
                                            label: function (context) {
                                                if (context.datasetIndex === 2) {
                                                    var name = context.dataset.label.split('\n')[0];
                                                    var Percent = context.dataset.data[context.dataIndex];
                                                    var QTY_Unit = context.dataset.qty[context.dataIndex];
                                                    return `${name} : ${Percent} % | Qty : ${QTY_Unit}`
                                                }
                                            }
                                        }
                                    },
                                    legend: {
                                        position: 'right',
                                        labels: {
                                            boxWidth: 30,
                                            boxHeight: 2,
                                            color: '#FFFFFF'
                                        }
                                    },
                                    title: {
                                        display: true,
                                        text: `ATS YIELD : ${selectedModel} / ${byProcess}`,
                                        color: '#FFFFFF',
                                        font: {
                                            size: 15,
                                            family: 'Century Gothic',
                                            weight: 'bold'
                                        }
                                    }
                                }
                            }
                        });
                    } 
                    else {
                        mixChart.data.labels = data_all_mix.labels;
                        mixChart.data.datasets[0].data = new_arr_data_passed;
                        mixChart.data.datasets[1].data = new_arr_data_failed;
                        mixChart.data.datasets[2].data = new_arr_data;
                        mixChart.data.datasets[2].label = byProcess;
                        mixChart.data.datasets[2].qty = datasets_line_chart[0].quantity;
                        mixChart.options.plugins.title.text = `ATS YIELD : ${selectedModel} / ${byProcess}`;
                        mixChart.update(); // Update the chart to reflect the changes
                    }
                }
                // Create matrix table
                if (doubleClickProcess === false) {
                    if (runByProcess_Activate === false || runByProcess_Activate === true) {
                        create_matrix_table(dataAll, modeDayOption);
                    }
                }
                else if (runByProcess_Activate === true) {
                    create_matrix_table(dataAll, modeDayOption);
                }
            }
            
            else {
                // Clear Line Chart
                if (lineChart) {
                    lineChart.data.labels = [];
                    lineChart.data.datasets = [];
                    lineChart.update();
                }
                // Clear Mix Chart
                if (mixChart) {
                    mixChart.data.labels = [];
                    mixChart.data.datasets[0].data = [];
                    mixChart.data.datasets[1].data = [];
                    mixChart.data.datasets[2].data = [];
                    mixChart.data.datasets[2].qty = [];
                    mixChart.update();
                }
                // Clear Matrix Data Table Chart
                const matrix_table = document.getElementById('matrix_table');
                matrix_table.innerHTML = '';
                const dataRow_matrix = document.createElement('tr');
                matrix_table.appendChild(dataRow_matrix);
                document.body.appendChild(matrix_table);

                // Clear Raw Data Table Chart
                const raw_data_table = document.getElementById('raw_data_table');
                raw_data_table.innerHTML = '';
                const dataRow_raw = document.createElement('tr');
                raw_data_table.appendChild(dataRow_raw);
                document.body.appendChild(raw_data_table);
            }
            if (doubleClickProcess === false) {
                $('#loader').css({'display': 'none'});
            }
        })
}

var myMixChartSecond;
function fetchData_Second(process_cliked) {
    if (modeDayOption === 'DATE') {
        mode_show = ' Days'
    }
    else if (modeDayOption === 'WEEK') {
        mode_show = ' Weeks'
    }
    else if (modeDayOption === 'MONTH') {
        mode_show = ' Months'
    }
    else if (modeDayOption === 'QUARTER') {
        mode_show = ' Quarters'
    }
    selectedDay_Label = parseInt(selectedDays) + 1;
    document.getElementById('label_day_selected').textContent = String(selectedDay_Label) + mode_show;
    $('#loader').css({'display': 'block'});

    fetch(
        `/fetch_data?` +
        `days=${selectedDays}` +
        `&selected_Product=${selectedProduct}` +
        `&selected_Model=${selectedModel}` +
        `&mode_day_option=${modeDayOption}` + 
        `&by_Process=${process_cliked}`
        )
        .then(response => response.json())
        .then(dataJSON => {
            const dataAll = dataJSON.data;
            if (dataAll.length > 0) {
                const data = [];
                for (var i = 0; i < dataAll.length; i++) {
                    var val = dataAll[i];
                    data.push([
                        val.Process, 
                        val[modeDayOption],
                        val.FPY,
                        val.QTY,
                        val.RTY,
                        val.Pareto,
                        val.Fail,
                        val.Pass,
                        parseInt(val.QTY) - parseInt(val.Pass),
                        val.Model,
                        val['%']
                    ]);
                }
                var dates = [...new Set(data.map(item => item[1]))];
                if (modeDayOption === 'D'|| modeDayOption === 'M') {
                    dates.sort(function(a, b) { // Sort data aecending
                        // Convert the date strings to JavaScript Date objects for comparison
                        var dateA = new Date(a);
                        var dateB = new Date(b);
                    
                        // Compare the dates
                        return dateA - dateB;
                    });
                }
                const data_all_mix = {labels: [], quantity: []} 
                var datasets_line_chart = [];
                data.forEach(processData => {
                    var legendName;
                    if (modeRunAll_HW === true) {
                        legendName = processData[9]; // legend name
                    }
                    else {
                        legendName = processData[0]; // legend name
                    }
                    var date = processData[1]; // x
                    var value = parseFloat(processData[2]); // y
                    var quantity = parseInt(processData[3]); // other data
                    var passed_units = parseInt(processData[7]);
                    var failed_units = parseInt(processData[8]);
                    
                    // Find or create dataset for the process
                    var dataset_line = datasets_line_chart.find(ds => ds.label === legendName);
                    if (!dataset_line) {
                        dataset_line = {
                            type: 'line',
                            label: legendName,
                            data: [],
                            passed: [],
                            failed: [],
                            quantity: [],
                            fill: false,
                            borderWidth: 2,
                            lineTension: 0,
                        };
                        datasets_line_chart.push(dataset_line);
                    } 

                    var dateIndex = dates.indexOf(date);
                    if (dateIndex === -1) {
                        dates.push(date);
                        dateIndex = dates.indexOf(date);
                    }

                    dataset_line.data[dateIndex] = value;
                    dataset_line.quantity[dateIndex] = quantity;
                    dataset_line.passed[dateIndex] = passed_units;
                    dataset_line.failed[dateIndex] = failed_units;

                    data_all_mix.labels[dateIndex] = date;
                });

                const arr_data = [];
                const arr_data_passed = [];
                const arr_data_failed = [];

                datasets_line_chart.forEach(val => {
                    arr_data.push(val.data);
                    arr_data_passed.push(val.passed);
                    arr_data_failed.push(val.failed);
                });
                var new_arr_data = arr_data.pop();
                var new_arr_data_passed = arr_data_passed.pop();
                var new_arr_data_failed = arr_data_failed.pop();
                
                var merge_chart = {
                    labels: data_all_mix.labels,
                    datasets: [
                        {
                            label: 'PASS',
                            backgroundColor: 'rgba(39, 255, 0, 0.5)',
                            data: new_arr_data_passed
                        },
                        {
                            label: 'FAIL',
                            backgroundColor: 'rgba(255, 0, 0, 0.5)',
                            data: new_arr_data_failed
                        },
                        {
                            label: process_cliked,
                            type: 'line',
                            fill: false,
                            backgroundColor: '#AE00FF',
                            borderColor: '#AE00FF',
                            yAxisID: 'line-axis',
                            data: new_arr_data,
                            qty: datasets_line_chart[0].quantity
                        }
                    ]
                };
                
                if (!myMixChartSecond) {
                    var ctx_mix_second = document.getElementById('myMixChartSecond').getContext('2d');
                    myMixChartSecond = new Chart(ctx_mix_second, {
                        type: 'bar',
                        data: merge_chart,
                        options: {
                            responsive: true,
                            scales: {
                                x: {
                                    stacked: true,
                                    offset: true,
                                    title: {
                                        display: true,
                                        text: 'DATE',
                                        color: '#FFFFFF',
                                        font: {
                                            size: 15,
                                            family: 'Century Gothic',
                                            weight: 'bold'
                                        }
                                    },
                                    ticks: {
                                        color: '#FFFFFF'
                                    }
                                },
                                y: {
                                    stacked: true,
                                    title: {
                                        display: false,
                                        color: '#FFFFFF',
                                        font: {
                                            size: 15,
                                            family: 'Century Gothic',
                                            weight: 'bold'
                                        }
                                    },
                                    ticks: {
                                        color: '#FFFFFF'
                                    }
                                },
                                'line-axis': {
                                    type: 'linear',
                                    position: 'right',
                                    display: true,
                                    color: '#FFFFFF',
                                    font: {
                                        size: 15,
                                        family: 'Century Gothic',
                                        weight: 'bold'
                                    },
                                    ticks: {
                                        color: '#FFFFFF'
                                    }
                                }
                            },
                            plugins: {
                                tooltip: {
                                    mode: 'index', // Display multiple tooltips at once
                                    intersect: false,
                                    callbacks: {
                                        label: function (context) {
                                            if (context.datasetIndex === 2) {
                                                var name = context.dataset.label.split('\n')[0];
                                                var Percent = context.dataset.data[context.dataIndex];
                                                var QTY_Unit = context.dataset.qty[context.dataIndex];
                                                return `${name} : ${Percent} % | Qty : ${QTY_Unit}`
                                            }
                                        }
                                    }
                                },
                                legend: {
                                    position: 'right',
                                    labels: {
                                        boxWidth: 30,
                                        boxHeight: 2,
                                        color: '#FFFFFF'
                                    }
                                },
                                title: {
                                    display: true,
                                    text: `ATS YIELD : ${selectedModel} / ${process_cliked}`,
                                    color: '#FFFFFF',
                                    font: {
                                        size: 15,
                                        family: 'Century Gothic',
                                        weight: 'bold'
                                    }
                                }
                            }
                        }
                    });
                } 
                else {
                    myMixChartSecond.data.labels = data_all_mix.labels;
                    myMixChartSecond.data.datasets[0].data = new_arr_data_passed;
                    myMixChartSecond.data.datasets[1].data = new_arr_data_failed;
                    myMixChartSecond.data.datasets[2].data = new_arr_data;
                    myMixChartSecond.data.datasets[2].label = process_cliked;
                    myMixChartSecond.data.datasets[2].qty = datasets_line_chart[0].quantity;
                    myMixChartSecond.options.plugins.title.text = `ATS YIELD : ${selectedModel} / ${process_cliked}`;
                    myMixChartSecond.update(); // Update the chart to reflect the changes
                }
                $('#loader').css({'display': 'none'});
            }
        })
}

function fetchValueByColName(col_name) {
    fetch(
        `/fetch_value_by_colName?` +
        `days=${selectedDays}` +
        `&selected_Product=${selectedProduct}` +
        `&selected_Model=${selectedModel}` +
        `&mode_day_option=${modeDayOption}` + 
        `&by_Process=${byProcess}` +
        `&column_name=${col_name}`
        )
        .then(response => response.json())
        .then(dataJSON => {
            dataJSON.data.forEach(val => {
                var BT_colName = document.createElement('button');
                BT_colName.innerText = val.ColValue;
                document.getElementById('div_Dash').appendChild(BT_colName);
            });
        })
}
        
// toggleTab
modeRunAll_HW = false;
function toggleTab_NON_AC1200(tabName, productName) {
    var emptyPage = document.getElementById('empty_page_non_ac1200');

    // Hide all sub-menus
    document.querySelectorAll('.sub-menu-non-ac1200').forEach(function (submenu) {
        submenu.style.display = 'none';
    });
    
    if (document.getElementById(tabName + '-content').style.display === 'none') {
        document.querySelectorAll('.tab-content').forEach(function (allTab) {
            allTab.style.display = 'none';
        }); 
        document.querySelectorAll('.empty_page').forEach(function (emptyPage) {
            emptyPage.style.display = 'none';
        }); 
        document.getElementById(tabName + '-content').style.display = 'block';
        emptyPage.style.display = 'block';  
         
    } else {
        document.getElementById(tabName + '-content').style.display = 'none';
        emptyPage.style.display = 'none'; 
    }
}

function toggleTab_JANNU(tabName, productName) {
    var emptyPage = document.getElementById('empty_page_jannu');

    // Hide all sub-menus
    document.querySelectorAll('.sub-menu-jannu').forEach(function (submenu) {
        submenu.style.display = 'none';
    });
    
    if (document.getElementById(tabName + '-content').style.display === 'none') {
        document.querySelectorAll('.tab-content').forEach(function (allTab) {
            allTab.style.display = 'none';
        }); 
        document.querySelectorAll('.empty_page').forEach(emptyPage => {
            emptyPage.style.display = 'none';
        }); 
        document.getElementById(tabName + '-content').style.display = 'block';
        emptyPage.style.display = 'block';  
         
    } else {
        document.getElementById(tabName + '-content').style.display = 'none';
        emptyPage.style.display = 'none'; 
    }
}
function toggleTab_AC1200(tabName, productName) {
    var emptyPage = document.getElementById('empty_page_ac1200');

    // Hide all sub-menus
    document.querySelectorAll('.sub-menu-ac1200').forEach(function (submenu) {
        submenu.style.display = 'none';
    });

    if (document.getElementById(tabName + '-content').style.display === 'none') {
        document.querySelectorAll('.tab-content').forEach(function (allTab) {
            allTab.style.display = 'none';
        }); 
        document.querySelectorAll('.empty_page').forEach(function (emptyPage) {
            emptyPage.style.display = 'none';
        }); 
        document.getElementById(tabName + '-content').style.display = 'block';
        emptyPage.style.display = 'block';  

    } else {
        document.getElementById(tabName + '-content').style.display = 'none';
        emptyPage.style.display = 'none';  
    }
}
function toggleTab_ZEPHYR(tabName, productName) {
    var emptyPage = document.getElementById('empty_page_zephyr');

    // Hide all sub-menus
    document.querySelectorAll('.sub-menu-zephyr').forEach(function (submenu) {
        submenu.style.display = 'none';
    });

    if (document.getElementById(tabName + '-content').style.display === 'none') {
        document.querySelectorAll('.tab-content').forEach(function (allTab) {
            allTab.style.display = 'none';
        }); 
        document.querySelectorAll('.empty_page').forEach(function (emptyPage) {
            emptyPage.style.display = 'none';
        }); 
        document.getElementById(tabName + '-content').style.display = 'block';
        emptyPage.style.display = 'block';  

    } else {
        document.getElementById(tabName + '-content').style.display = 'none';
        emptyPage.style.display = 'none';  
    }
}

// toggle sub menu
// function toggleSubMenu_NON_AC1200(menuName, labelId, Product, Model) {
//     var subMenu = document.getElementById(menuName + '-submenu');

//     document.querySelectorAll('.tabLinks').forEach(element => {
//         element.style.backgroundColor = 'white';
//     })
//     document.getElementById('button_1').style.backgroundColor = '#08cc77';

//     document.getElementById('matrix_table').style.display = 'block';
//     document.getElementById('raw_data_table').style.display = 'none';
//     document.getElementById('history_data_table').style.display = 'none';
//     document.getElementById('pareto_data_table').style.display = 'none';

//     document.getElementById('myLineChart').style.display = 'block';
//     document.getElementById('myMixChart').style.display = 'none';
//     document.getElementById('myParetoChart').style.display = 'none';
//     document.getElementById('myParetoFailChart').style.display = 'none';

//     document.querySelectorAll('.sub-menu-non-ac1200').forEach(function (submenu) {
//         submenu.style.display = 'none';
//     });
//     runByProcess_Activate = false;
//     byProcess = '';
//     modeRunAll_HW = false;
//     doubleClickProcess = false;
//     Run_All_Process(labelId, Product, Model)

//     if (subMenu.style.display === 'none') {
//         subMenu.style.display = 'block';
//     } else {
//         subMenu.style.display = 'none';
//     }
// }

function toggleSubMenu_JANNU(menuName, labelId, Product, Model) {
    var subMenu = document.getElementById(menuName + '-submenu');

    document.querySelectorAll('.tabLinks').forEach(element => {
        element.style.backgroundColor = 'white';
    })
    document.getElementById('button_1').style.backgroundColor = '#08cc77';

    document.getElementById('matrix_table').style.display = 'block';
    document.getElementById('raw_data_table').style.display = 'none';
    document.getElementById('history_data_table').style.display = 'none';
    document.getElementById('pareto_data_table').style.display = 'none';

    document.getElementById('myLineChart').style.display = 'block';
    document.getElementById('myMixChart').style.display = 'none';
    document.getElementById('myParetoChart').style.display = 'none';
    document.getElementById('myParetoFailChart').style.display = 'none';
    document.getElementById('myMixChartSecond').style.display = 'none';

    document.querySelectorAll('.sub-menu-jannu').forEach(function (submenu) {
        submenu.style.display = 'none';
    });
    runByProcess_Activate = false;
    byProcess = '';
    modeRunAll_HW = false;
    doubleClickProcess = false;
    Run_All_Process(labelId, Product, Model)

    if (subMenu.style.display === 'none') {
        subMenu.style.display = 'block';
    } else {
        subMenu.style.display = 'none';
    }
}

function toggleSubMenu_AC1200(menuName, labelId, Product, Model) {
    var subMenu = document.getElementById(menuName + '-submenu');

    document.querySelectorAll('.tabLinks').forEach(element => {
        element.style.backgroundColor = 'white';
    })
    document.getElementById('button_1').style.backgroundColor = '#08cc77';

    document.getElementById('matrix_table').style.display = 'block';
    document.getElementById('raw_data_table').style.display = 'none';
    document.getElementById('history_data_table').style.display = 'none';
    document.getElementById('pareto_data_table').style.display = 'none';

    document.getElementById('myLineChart').style.display = 'block';
    document.getElementById('myMixChart').style.display = 'none';
    document.getElementById('myParetoChart').style.display = 'none';
    document.getElementById('myParetoFailChart').style.display = 'none';
    document.getElementById('myMixChartSecond').style.display = 'none';


    document.querySelectorAll('.sub-menu-ac1200').forEach(function (submenu) {
        submenu.style.display = 'none';
    });
    runByProcess_Activate = false;
    byProcess = '';
    modeRunAll_HW = false;
    doubleClickProcess = false;
    Run_All_Process(labelId, Product, Model)

    // Toggle the visibility of the sub-menu
    if (subMenu.style.display === 'none') {
        subMenu.style.display = 'block';
    } else {
        subMenu.style.display = 'none';
    }
}

// function toggleSubMenu_ZEPHYR(menuName, labelId, Product, Model) {
//     var subMenu = document.getElementById(menuName + '-submenu');
    
//     document.getElementById('button_1').style.backgroundColor = '#08cc77';
//     document.getElementById('button_2').style.backgroundColor = '#ffffff';
//     document.getElementById('button_3').style.backgroundColor = '#ffffff';
//     document.getElementById('button_4').style.backgroundColor = '#ffffff';

//     document.getElementById('matrix_table').style.display = 'block';
//     document.getElementById('raw_data_table').style.display = 'none';
//     document.getElementById('history_data_table').style.display = 'none';
//     document.getElementById('pareto_data_table').style.display = 'none';

//     document.getElementById('myLineChart').style.display = 'block';
//     document.getElementById('myMixChart').style.display = 'none';

//     document.querySelectorAll('.sub-menu-zephyr').forEach(function (submenu) {
//         submenu.style.display = 'none';
//     });
//     runByProcess_Activate = false;
//     byProcess = '';
//     modeRunAll_HW = false;
//     doubleClickProcess = false;
//     Run_All_Process(labelId, Product, Model)

//     // Toggle the visibility of the sub-menu
//     if (subMenu.style.display === 'none') {
//         subMenu.style.display = 'block';
//     } else {
//         subMenu.style.display = 'none';
//     }
// }

function create_matrix_table(data, modeDay) {
    if (data.length > 0) {
        var uniqueDates;
        if (modeDay === 'DATE') {
            uniqueDates = [...new Set(data.map(item => item[modeDayOption]))];
            uniqueDates.sort(function(a, b) { // Sort data aecending
                var dateA = new Date(a);
                var dateB = new Date(b);
            
                return dateA - dateB;
            });
            uniqueDates.reverse()
        }
        else if (modeDay === 'MONTH') {
            uniqueDates = [...new Set(data.map(item => item[modeDayOption]))];
            uniqueDates.sort(function(a, b) { // Sort data aecending
                var dateA = new Date(a);
                var dateB = new Date(b);
            
                return dateA - dateB;
            });
            uniqueDates.reverse()
        }
        else if (modeDay === 'WEEK' || modeDay ==='QUARTER') {
            uniqueDates = [...new Set(data.map(item => item[modeDayOption]))];
            uniqueDates.reverse()
        }
        
        // forEach is a for loop but run equal amount of data
        col_header_1_template = '';
        uniqueDates.forEach (date => {
            col_header_1_template += `<th colspan="6">${date}</th>`;
        });
        
        // for loop is for run follow loop set
        second_col_name = ['Qty','FTY','RTY','Pareto','Fail']
        col_header_2_template = '';
        for (let i = 0; i < uniqueDates.length; i++) {
            col_header_2_template += `
                                    <th>Qty</th>
                                    <th>FPY</th>
                                    <th>RTY</th>
                                    <th>Pareto</th>
                                    <th>Fail</th>
                                    <th>%</th>
                                    `;
        }
        
        // Populate the table with data follow data that need to set group category
        var uniqueLegends;
        if (modeRunAll_HW === true) {
            uniqueLegends = [...new Set(data.map(item => item.Model))];
        }
        else {
            uniqueLegends = [...new Set(data.map(item => item.Process))];
        }
        row_header_template = '';
        col_1 = '';
        template_detail = '';
        uniqueLegends.forEach (legend => {
            col_1 = `
                    <tbody>
                        <tr>
                            <th style="position: sticky; left: -1px;"
                                rowspan="5">${legend}
                            </th>`;
            
            detail_template = '';
            uniqueDates.forEach (date => {
                // Group data prepare insert to table
                var rowData = data.filter(item => item.Process === legend && item[modeDayOption] === date);
                if (rowData.length > 0) {
                    dataPareto = '';
                    dataParetoFail = '';
                    dataParetoFPY = '';
                    // if (rowData[0].Pareto !== 'None') {
                    //     dataPareto = rowData[0].Pareto;
                    //     dataParetoFail = rowData[0].Fail;
                    //     dataParetoFPY = rowData[0]["%"];
                    // }
                    if (Object.values(rowData[0].Pareto).length > 0) {
                        dataPareto = rowData[0].Pareto;
                        dataParetoFail = rowData[0].Fail;
                        dataParetoFPY = rowData[0]["%"];
                    }
                    console.log()
                    backgroundColor_FPY = '';
                    if (parseFloat(rowData[0].FPY) >= 90) {
                        backgroundColor_FPY = 'background-color : #1DAD00; font-weight: bold; text-align: center;';
                    }
                    else if (parseFloat(rowData[0].FPY) >= 70) {
                        backgroundColor_FPY = 'background-color : #E28200; font-weight: bold; text-align: center;';
                    }
                    else if (parseFloat(rowData[0].FPY) < 70) {
                        backgroundColor_FPY = 'background-color : #CA0000; font-weight: bold; text-align: center;';
                    }

                    backgroundColor_RTY = '';
                    if (parseFloat(rowData[0].RTY) >= 90) {
                        backgroundColor_RTY = 'background-color : #1DAD00; font-weight: bold; text-align: center;';
                    }
                    else if (parseFloat(rowData[0].RTY) >= 70) {
                        backgroundColor_RTY = 'background-color : #E28200; font-weight: bold; text-align: center;';
                    }
                    else if (parseFloat(rowData[0].RTY) < 70) {
                        backgroundColor_RTY = 'background-color : #CA0000; font-weight: bold; text-align: center;';
                    }
                    detail_template += `
                                        <td rowspan="5" style="text-align: center;">${rowData[0].QTY}</td>
                                        <td rowspan="5" style="${backgroundColor_FPY}">${rowData[0].FPY}</td>
                                        <td rowspan="5" style="${backgroundColor_RTY}">${rowData[0].RTY}</td>
                                        <td class="for_pareto">${dataPareto}</td>
                                        <td class="for_pareto" style="text-align: right;">${dataParetoFail}</td>
                                        <td class="for_pareto" style="text-align: right;">${dataParetoFPY}</td>
                                        `;
                }
                else {
                    detail_template += `
                                        <td rowspan="5"></td>
                                        <td rowspan="5"></td>
                                        <td rowspan="5"></td>
                                        <td></td>
                                        <td></td>
                                        <td></td>
                                        `;
                }
            });
            
            // split 5 rows from cell. But ther is already 1 row. This condition is just loop only 4 rounds That mean 1 + 4 = 5 rows
            split_cell_to_5_rows = '';
            for (let i = 1; i < 5; i++) {
                cell_Pareto_and_Fail_follow_date = '';
                uniqueDates.forEach (date => {
                    var row_next_Data = data.filter(item => item.Process === legend && item[modeDayOption] === date);
                    if (row_next_Data.length > 0) {
                        if (row_next_Data[i]) {
                            dataPareto = '';
                            dataParetoFail = '';
                            dataParetoFPY = '';
                            // if (row_next_Data[i].Pareto !== 'None') {
                            //     dataPareto = row_next_Data[i].Pareto;
                            //     dataParetoFail = row_next_Data[i].Fail;
                            //     dataParetoFPY = row_next_Data[i]["%"];
                            // }
                            if (Object.values(row_next_Data[i].Pareto).length > 0) {
                                dataPareto = row_next_Data[i].Pareto;
                                dataParetoFail = row_next_Data[i].Fail;
                                dataParetoFPY = row_next_Data[i]["%"];
                            }
                            
                            cell_Pareto_and_Fail_follow_date += `
                                                                <td class="for_pareto">${dataPareto}</td>
                                                                <td class="for_pareto" style="text-align: right;">${dataParetoFail}</td>
                                                                <td class="for_pareto" style="text-align: right;">${dataParetoFPY}</td>
                                                                ` // Cell of column 'Pareto' and 'Fail'
                        }
                        else {
                            cell_Pareto_and_Fail_follow_date += `
                                                                <td></td>
                                                                <td></td>
                                                                <td></td>
                                                                `; // Cell of column 'Pareto' and 'Fail'
                        }
                    }
                    else {
                        cell_Pareto_and_Fail_follow_date += `
                                                            <td></td>
                                                            <td></td>
                                                            <td></td>
                                                            `; // Cell of column 'Pareto' and 'Fail'
                    }
                });
                split_cell_to_5_rows += `<tr>${cell_Pareto_and_Fail_follow_date}</tr>`;
            }
            template_detail += `${col_1 + detail_template}</tr>${split_cell_to_5_rows}</tbody>`;
        });

        const matrix_table = document.getElementById('matrix_table');
        matrix_table.innerHTML = '';

        const theader_1 = document.createElement('thead');
        const headerRow1 = document.createElement('tr');
        theader_1.style.position = 'sticky';
        theader_1.style.top = '-1px';
        theader_1.style.zIndex = '3';
        headerRow1.innerHTML = `<th style="position: sticky; left: 0px;">DATE</th>${col_header_1_template}`;
        theader_1.appendChild(headerRow1)
        matrix_table.appendChild(theader_1)
        
        const headerRow2 = document.createElement('tr');
        headerRow2.style.position = 'sticky';
        headerRow2.style.top = '20px';
        headerRow2.style.zIndex = '3';
        headerRow2.innerHTML = `<th style="position: sticky; left: -1px;">PROCESS</th>${col_header_2_template}`;
        theader_1.appendChild(headerRow2)
        matrix_table.appendChild(theader_1);
        
        const row = document.createElement('tbody');
        row.innerHTML = template_detail;
        matrix_table.appendChild(row);

        document.body.appendChild(matrix_table);
    }
    else {
        const matrix_table = document.getElementById('matrix_table');
        matrix_table.innerHTML = '';
        const dataRow = document.createElement('tr');
        matrix_table.appendChild(dataRow);
        document.body.appendChild(matrix_table);
    }
}

function queryHistorybyLegend(dateCutOff) {
    // Clear Raw Data Table Chart
    const raw_data_table = document.getElementById('raw_data_table');
    raw_data_table.innerHTML = '';

    var daysDifference;
    if (modeDayOption === 'DATE') {
        var timeDifference = new Date() - new Date(dateCutOff);
        daysDifference = Math.floor(timeDifference / (1000 * 60 * 60 * 24));
    }
    else if (modeDayOption === 'WEEK') {
        var currentDate_1 = new Date(new Date());
        currentDate_1.setDate(currentDate_1.getDate() + 4 - (currentDate_1.getDay() || 7));
        var yearStart = new Date(currentDate_1.getFullYear(), 0, 1);
        var weekNumber = Math.ceil(((currentDate_1 - yearStart) / 86400000 + 1) / 7);
  
        daysDifference = Math.abs(weekNumber - parseInt(dateCutOff.split(' ')[0].split('-')[1]));
    }
    else if (modeDayOption === 'MONTH') {
        var currentDate_2 = new Date();
        var dateCutOff_reFormat = new Date(dateCutOff);
        daysDifference = (currentDate_2.getFullYear() - dateCutOff_reFormat.getFullYear()) * 12 + (currentDate_2.getMonth() - dateCutOff_reFormat.getMonth());
    }
    else if (modeDayOption === 'QUARTER') {
        var now = new Date();
        var currentDate_3 = now instanceof Date ? now : new Date();
        const month = currentDate_3.getMonth();
        const quarter = Math.floor(month / 3) + 1;

        daysDifference = Math.abs(quarter - parseInt(dateCutOff.split('-')[0].split('Q')[1]));
        if (daysDifference === 0) {
            daysDifference = 1;
        }
    }
    
    $('#loader').css({'display': 'block'});
    fetch(
        `/fetch_data_by_Process?` +
        `days=${daysDifference}` +
        `&selected_Product=${selectedProduct}` +
        `&selected_Model=${selectedModel}` +
        `&mode_day_option=${modeDayOption}` +
        `&process_from_table=${byProcess}`
        )
        .then(response => response.json())
        .then(dataJSON => {
            var sortNewData = [];
            dataJSON.raw_data.forEach(data => {
                var dataGroup = {};
                dataJSON.col_name.forEach(col => {
                    dataGroup[col] = data[col];
                });
                sortNewData.push(dataGroup)
            })
            if (sortNewData.length > 0) {
                const raw_data_table = document.getElementById('raw_data_table')
                raw_data_table.innerHTML = '';
                
                const theader = document.createElement('thead');
                const headerRow = document.createElement('tr');
            
                Object.keys(sortNewData[0]).forEach(val => {
                    const colHeader = document.createElement('th');
                    if (val === 'SN') {
                        colHeader.style.position = 'sticky';
                        colHeader.style.left = '0';
                    }
                    if (val === 'Passed') {
                        colHeader.style.position = 'sticky';
                        colHeader.style.left = '59px';
                        colHeader.style.color = '#07CB22';
                    }
                    if (val === 'Failed') {
                        colHeader.style.position = 'sticky';
                        colHeader.style.left = '107px';
                        colHeader.style.color = '#EC0000';
                    }
                    colHeader.innerHTML = val;
                    headerRow.appendChild(colHeader)
                });
                theader.appendChild(headerRow)
                raw_data_table.appendChild(theader)

                const tbody = document.createElement('tbody')
                sortNewData.forEach(rowData => {
                    const dataRow = document.createElement('tr');
        
                    if (rowData["Fail Mode"] !== 'PASS') {
                        dataRow.style.backgroundColor = 'rgb(255, 0, 0)';
                    }
                    else {
                        dataRow.style.backgroundColor = 'transparent';
                    }
                    Object.keys(sortNewData[0]).forEach((key, columnIndex) => {
                        const dataCell = document.createElement('td');
                        if (key === 'SN' ||  key === 'Passed' || key === 'Failed') {
                            dataCell.style.color = '#00FFFF';
                            dataCell.style.cursor = 'pointer';
                            dataCell.style.fontWeight = 'bold';                         
                        }
                        if (key === 'SN') {
                            dataCell.style.position = 'sticky';
                            dataCell.style.left = '0';
                            dataCell.style.backgroundColor = '#28283c';
                        }
                        if (key === 'Passed') {
                            dataCell.style.position = 'sticky';
                            dataCell.style.left = '59px';
                            dataCell.style.backgroundColor = '#28283c';
                        }
                        if (key === 'Failed') {
                            dataCell.style.position = 'sticky';
                            dataCell.style.left = '107px';
                            dataCell.style.backgroundColor = '#28283c';
                        }
                        if (key === 'Fail Mode') {
                            if (rowData[key] === 'PASS') {
                                dataCell.style.color = '#07CB22';
                            }
                        }
                        // Add function Click of Col 0,1,2
                        if (columnIndex === 0) {
                            dataCell.onclick = function () {
                                SN_Searching(rowData['SN'], 'All')
                            };
                        }
                        if (columnIndex === 1) {
                            dataCell.onclick = function () {
                                SN_Searching(rowData['SN'], 'Passed')
                            };
                        }
                        if (columnIndex === 2) {
                            dataCell.onclick = function () {
                                SN_Searching(rowData['SN'], 'Failed')
                            };
                        }
                        // Add function Hover of Col 0,1,2
                        if (key === 'SN' ||  key === 'Passed' || key === 'Failed') {
                            dataCell.addEventListener('mouseover', function() {
                                dataCell.style.backgroundColor = 'rgb(255, 255, 0)';
                                dataCell.style.color = 'black';
                            });
                            dataCell.addEventListener('mouseout', function() {
                                dataCell.style.backgroundColor = '#28283c';
                                dataCell.style.color = '#00FFFF';
                            });
                        }

                        dataCell.innerHTML = rowData[key];
                        dataRow.appendChild(dataCell)
                    });
                    tbody.appendChild(dataRow)
                    raw_data_table.appendChild(tbody)
                });
                document.body.appendChild(raw_data_table)
                $('#loader').css({'display': 'none'});
            }
            else {
                const raw_data_table = document.getElementById('raw_data_table');
                raw_data_table.innerHTML = '';
                $('#loader').css({'display': 'none'});
            }
        })
}

function SN_Searching(Serial_number, Query_Mode) {
    document.querySelector('.wheel-and-hamster').style.zIndex = '8';

    document.getElementById('myLineChart').style.display = 'none';
    document.getElementById('myMixChart').style.display = 'none';
    document.getElementById('myParetoChart').style.display = 'none';
    document.getElementById('myParetoFailChart').style.display = 'none';
    document.getElementById('myMixChartSecond').style.display = 'none';

    document.getElementById('matrix_table').style.display = 'none';
    document.getElementById('raw_data_table').style.display = 'none';
    document.getElementById('history_data_table').style.display = 'block';
    document.getElementById('pareto_data_table').style.display = 'none';

    document.querySelectorAll('.tabLinks').forEach(element => {
        element.style.backgroundColor = 'white';
    })
    document.getElementById('button_4').style.backgroundColor = '#08cc77';

    // Clear Raw Data Table Chart
    const history_data_table = document.getElementById('history_data_table');
    history_data_table.innerHTML = '';
    const dataRow = document.createElement('tr');
    history_data_table.appendChild(dataRow);
    document.body.appendChild(history_data_table);

    fetch(`/history_UUT?UUT_SN_selected=${Serial_number}&Query_Mode=${Query_Mode}`)
    .then(response => response.json())
    .then(dataJSON =>{
        if (dataJSON.raw_data.length > 0) {
            var sortNewData = [];
            dataJSON.raw_data.forEach(data => {
                var dataGroup = {};
                dataJSON.col_name.forEach(col => {
                    dataGroup[col] = data[col];
                });
                sortNewData.push(dataGroup)
            })
      
            const history_data_table = document.getElementById('history_data_table')
            history_data_table.innerHTML = '';
            
            const theader = document.createElement('thead');
            const headerRow = document.createElement('tr');
          
            Object.keys(sortNewData[0]).forEach(val => {
                const colHeader = document.createElement('th');
                colHeader.innerHTML = val;
                headerRow.appendChild(colHeader)
            });
            theader.appendChild(headerRow)
            history_data_table.appendChild(theader)

            const tbody = document.createElement('tbody')
            sortNewData.forEach(rowData => {
                const dataRow = document.createElement('tr');
                if (rowData["FAIL_MODE"] !== 'PASS') {
                    dataRow.style.backgroundColor = 'rgb(255, 0, 0)';
                }
                else {
                    dataRow.style.backgroundColor = 'transparent';
                }
                Object.keys(sortNewData[0]).forEach(key => {
                    const dataCell = document.createElement('td');

                    dataCell.innerHTML = rowData[key];
                    dataRow.appendChild(dataCell)
                });
                tbody.appendChild(dataRow)
                history_data_table.appendChild(tbody)
            });
            document.body.appendChild(history_data_table)
        }
        else {
            const history_data_table = document.getElementById('history_data_table');
            history_data_table.innerHTML = '';
            const dataRow = document.createElement('tr');
            history_data_table.appendChild(dataRow);
            document.body.appendChild(history_data_table);
        }
    })
}

// function changeHeaderColor(headerCell, legend) {
//     if (headerCell.style.backgroundColor !== 'yellow') {
//         document.querySelectorAll('th').forEach(cell => {
//             cell.style.backgroundColor = 'rgb(36, 29, 142)';
//             cell.style.color = 'white';
//         })
//         headerCell.style.backgroundColor = 'yellow';
//         headerCell.style.color = 'black';

//         queryHistorybyLegend(legend, true, false)

//         document.getElementById('matrix_table').style.display = 'block';
//         document.getElementById('raw_data_table').style.display = 'none';
//         document.getElementById('history_data_table').style.display = 'none';

//         document.getElementById('button_1').style.backgroundColor = '#08cc77';
//         document.getElementById('button_2').style.backgroundColor = '#ffffff';
//         document.getElementById('button_3').style.backgroundColor = '#ffffff';
   
//     }
//     else if (headerCell.style.backgroundColor === 'yellow') {
//         headerCell.style.backgroundColor = 'rgb(36, 29, 142)';
//         headerCell.style.color = 'white';
//         document.getElementById('matrix_table').style.display = 'block';
//         document.getElementById('raw_data_table').style.display = 'none';
//         document.getElementById('history_data_table').style.display = 'none';

//         doubleClickProcess = false;
//         byProcess = '';
//         fetchData()

//         document.getElementById('myLineChart').style.display = 'block';
//         document.getElementById('myMixChart').style.display = 'none';
//         document.getElementById('myParetoChart').style.display = 'none';
//         document.getElementById('myParetoFailChart').style.display = 'none';
//     }
// }

var pareto_raw_data = [];
var group_pareto_raw_data = [];
var date_pareto_raw_data = [];
function Pareto_Chart() {
    document.querySelectorAll('.tabLinks').forEach(element => {
        element.style.backgroundColor = 'white';
    })
    document.getElementById('button_2').style.backgroundColor = '#08cc77';

    document.getElementById('matrix_table').style.display = 'none';
    document.getElementById('raw_data_table').style.display = 'none';
    document.getElementById('history_data_table').style.display = 'none';
    document.getElementById('pareto_data_table').style.display = 'block';

    document.getElementById('myLineChart').style.display = 'none';
    document.getElementById('myMixChart').style.display = 'none';
    document.getElementById('myParetoChart').style.display = 'none';
    document.getElementById('myParetoFailChart').style.display = 'none';
    document.getElementById('myMixChartSecond').style.display = 'none';

    $('#loader').css({'display': 'block'});

    const pareto_table = document.getElementById('pareto_data_table');
    pareto_table.innerHTML = '';

    fetch(
        `/pareto_query_all_process?` +
        `days=${selectedDays}` +
        `&selected_Product=${selectedProduct}` +
        `&selected_Model=${selectedModel}` +
        `&mode_day_option=${modeDayOption}` + 
        `&by_Process=${byProcess}`
        )
    .then(response => response.json())
    .then(dataJSON => {
        if (dataJSON.raw_data.length > 0) {
            pareto_raw_data = [];
            dataJSON.raw_data.forEach(val => {
                pareto_raw_data.push(val)
            });
            date_pareto_raw_data = [];
            var DATE_arr;
            if (modeDayOption === 'DATE') {
                DATE_arr = [...new Set(pareto_raw_data.map(item => item[modeDayOption]))];
                DATE_arr.sort(function(a, b) { // Sort data aecending
                    var dateA = new Date(a);
                    var dateB = new Date(b);
                
                    return dateA - dateB;
                });
                DATE_arr.reverse()
            }
            else if (modeDayOption === 'MONTH') {
                DATE_arr = [...new Set(pareto_raw_data.map(item => item[modeDayOption]))];
                DATE_arr.sort(function(a, b) { // Sort data aecending
                    var dateA = new Date(a);
                    var dateB = new Date(b);
                
                    return dateA - dateB;
                });
                DATE_arr.reverse()
            }
            else if (modeDayOption === 'WEEK' || modeDayOption === 'QUARTER') {
                DATE_arr = [...new Set(pareto_raw_data.map(item => item[modeDayOption]))];
            }
          
            date_pareto_raw_data = DATE_arr;
            
            var Result_arr = [];
            pareto_raw_data.forEach(item => {
                if (item.Result !== 'PASS') {
                    Result_arr.push(item.Result)
                }
            });
            Result_arr = [...new Set(Result_arr)];
            Result_arr.sort();
            
            group_pareto_raw_data = [];
            DATE_arr.forEach(val => {
                var object_pass = {};
                object_pass[val] = [];

                var object_fail = {};
                object_fail[val] = [];

                pareto_raw_data.forEach(item => {
                    if (item[modeDayOption] === val && item.Result === 'PASS') {
                        object_pass[val].push(parseInt(item.QTY))
                    }
                    else if (item[modeDayOption] === val && item.Result !== 'PASS') {
                        object_fail[val].push(parseInt(item.QTY))
                    }
                });

                var sum_fail = 0;
                Object.values(object_fail)[0].forEach(num => {
                    sum_fail += num;
                });
                object_fail[val] = sum_fail;

                object_pass[val].push(sum_fail)
                object_pass[val].push(parseFloat(((object_pass[val][0] / (object_pass[val][0] + sum_fail)) * 100).toFixed(2)))
                object_pass[val].push(parseFloat((100 - parseFloat(((object_pass[val][0] / (object_pass[val][0] + sum_fail)) * 100).toFixed(2))).toFixed(2)))

                group_pareto_raw_data.push(object_pass)
            });
            
            pareto_table.innerHTML = '';
            const col_header_1 = document.createElement('thead');
            const col_header_1_row = document.createElement('tr');
            col_header_1.style.position = 'sticky';
            col_header_1.style.top = '0px';
            var col_header_1_value = '';
            DATE_arr.forEach(val => {
                col_header_1_value += `<th colspan="2">${val}</th>`
            });
            col_header_1_row.innerHTML = `<th>DATE</th>${col_header_1_value}`
            col_header_1.appendChild(col_header_1_row);
            pareto_table.appendChild(col_header_1);

            const col_header_2 = document.createElement('thead');
            const col_header_2_row = document.createElement('tr');
            col_header_2.style.position = 'sticky';
            col_header_2.style.top = '20px';
            var col_header_2_value = '';
            DATE_arr.forEach(() => {
                col_header_2_value += `<th>QTY</th><th>%</th>`
            });
            col_header_2_row.innerHTML = `<th>RESULT</th>${col_header_2_value}`
            col_header_2.appendChild(col_header_2_row);
            pareto_table.appendChild(col_header_2);

            const col_header_3 = document.createElement('thead');
            const col_header_3_row = document.createElement('tr');
            col_header_3.style.position = 'sticky';
            col_header_3.style.top = '40px';
            col_header_3.style.color = '#00FF27';
            col_header_3.style.fontWeight = 'bold';
            var col_header_3_value = '';
            group_pareto_raw_data.forEach(val => {
                col_header_3_value += `<th>${Object.values(val)[0][0]}</th><th>${Object.values(val)[0][2]}</th>`
            });
            col_header_3_row.innerHTML = `<th>PASS</th>${col_header_3_value}`
            col_header_3.appendChild(col_header_3_row);
            pareto_table.appendChild(col_header_3);

            const col_header_4 = document.createElement('thead');
            const col_header_4_row = document.createElement('tr');
            col_header_4.style.position = 'sticky';
            col_header_4.style.top = '60px';
            col_header_4.style.color = '#FF0000';
            col_header_4.style.fontWeight = 'bold';
            var col_header_4_value = '';
            group_pareto_raw_data.forEach(val => {
                col_header_4_value += `<th>${Object.values(val)[0][1]}</th><th>${Object.values(val)[0][3]}</th>`
            });
            col_header_4_row.innerHTML = `<th>TOTAL FAIL</th>${col_header_4_value}`
            col_header_4.appendChild(col_header_4_row);
            pareto_table.appendChild(col_header_4);

            var sum_body_template = '';
            Result_arr.forEach(R => {
                var body_template = `<tr class="pareto_th" onclick="paretoSelectCell(this, '${R}', '')"><td>${R}</td>`;
                DATE_arr.forEach((D, idx) => {
                    var data_match = pareto_raw_data.filter(item => item[modeDayOption] === D && item.Result === R);
                    var fail_percent = Object.values(group_pareto_raw_data[idx])[0][3];
                    var qty_total_fail = Object.values(group_pareto_raw_data[idx])[0][1];
                    if (data_match.length > 0) {
                        body_template += `<td>${data_match[0].QTY}</td><td>${((fail_percent * data_match[0].QTY) / qty_total_fail).toFixed(2)}</td>`;
                    }
                    else {
                        body_template += `<td></td><td></td>`;
                    }
                    
                });
                body_template = `${body_template}</tr>`
                sum_body_template += body_template;
            })
            const tbody = document.createElement('tbody');
            tbody.innerHTML = sum_body_template;
            pareto_table.appendChild(tbody);
            document.body.appendChild(pareto_table);
            $('#loader').css({'display': 'none'});
        }
    })   
}

var paretoChart;
var paretoFailChart;
function paretoSelectCell(cell, parm, dateCutOff) {
    if (cell !== '') {
        if (cell.style.backgroundColor !== 'yellow') {
            document.querySelectorAll('.pareto_th').forEach(cell => {
                cell.style.backgroundColor = 'transparent';
                cell.style.color = 'white';
            })
            cell.style.backgroundColor = 'yellow';
            cell.style.color = 'black';
        }

        else if (cell.style.backgroundColor === 'yellow') {
            cell.style.backgroundColor = 'transparent';
            cell.style.color = 'white';
        }
    }
    
    // Create Pareto Chart
    if (dateCutOff === '') {
        document.getElementById('myLineChart').style.display = 'none';
        document.getElementById('myMixChart').style.display = 'none';
        document.getElementById('myParetoChart').style.display = 'block';
        document.getElementById('myParetoFailChart').style.display = 'none';
        document.getElementById('myMixChartSecond').style.display = 'none';

        var arr_qty_passed = [];
        var arr_qty_failed = [];
        group_pareto_raw_data.forEach(item => {
            arr_qty_passed.push(Object.values(item)[0][0])
            arr_qty_failed.push(Object.values(item)[0][1])
        });
    
        var cells = cell.closest('tr').getElementsByTagName('td');
        var rowValues = Array.from(cells).map(function(cell) {
            return cell.innerText;
        });
        var set_parm_pareto = [];
        for (let i = 0; i < arr_qty_passed.length * 2; i++) {
            if (i % 2 !== 0) {
                set_parm_pareto.push(rowValues[i])
            }
        }
        date_pareto_raw_data.reverse().sort()
        arr_qty_passed.reverse()
        arr_qty_failed.reverse()
        set_parm_pareto.reverse()
        var pareto_data = {
            labels: date_pareto_raw_data,
            datasets: [
                {
                    label: 'PASS',
                    backgroundColor: 'rgba(39, 255, 0, 0.5)',
                    data: arr_qty_passed
                },
                {
                    label: 'FAIL',
                    backgroundColor: 'rgba(255, 0, 0, 0.5)',
                    data: arr_qty_failed
                },
                {
                    label: parm,
                    type: 'line',
                    fill: false,
                    backgroundColor: '#AE00FF',
                    borderColor: '#AE00FF',
                    yAxisID: 'line-axis',
                    data: set_parm_pareto,
                }
            ]
        };
        if (!paretoChart) {
            var ctx_mix = document.getElementById('myParetoChart').getContext('2d');
            paretoChart = new Chart(ctx_mix, {
                type: 'bar',
                data: pareto_data,
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            stacked: true,
                            offset: true,
                            title: {
                                display: true,
                                text: 'DATE',
                                color: '#FFFFFF',
                                font: {
                                    size: 15,
                                    family: 'Century Gothic',
                                    weight: 'bold'
                                }
                            },
                            ticks: {
                                color: '#FFFFFF'
                            }
                        },
                        y: {
                            stacked: true,
                            title: {
                                display: false,
                                color: '#FFFFFF',
                                font: {
                                    size: 15,
                                    family: 'Century Gothic',
                                    weight: 'bold'
                                }
                            },
                            ticks: {
                                color: '#FFFFFF'
                            }
                        },
                        'line-axis': {
                            type: 'linear',
                            position: 'right',
                            display: true,
                            color: '#FFFFFF',
                            font: {
                                size: 15,
                                family: 'Century Gothic',
                                weight: 'bold'
                            },
                            ticks: {
                                color: '#FFFFFF'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            mode: 'index',
                            intersect: false,
                            callbacks: {
                                label: function (context) {
                                    var label = context.dataset.label || '';
                                    if (context.datasetIndex === 0) {
                                        label += ' : ' + context.parsed.y;
                                        pass = context.parsed.y;
                                        return label;
                                    }

                                    if (context.datasetIndex === 1) {
                                        label += ' : ' + context.parsed.y;
                                        fail = context.parsed.y;
                                        return label;
                                    }

                                    var pc_fail = 100 - ((parseInt(pass) / (parseInt(pass) + parseInt(fail))) * 100);
                                    if (context.datasetIndex === 2) {
                                        label += ' : ' + context.parsed.y + ` (${((pc_fail * context.parsed.y) / fail).toFixed(2)}) %`;
                                        return label;
                                    }
                                }
                            }
                        },
                        legend: {
                            position: 'right',
                            labels: {
                                boxWidth: 30,
                                boxHeight: 2,
                                color: '#FFFFFF'
                            }
                        },
                        title: {
                            display: true,
                            text: `ATS Trend (${byProcess.split('\n')[0]}) : ${date_pareto_raw_data[0]} - ${date_pareto_raw_data[date_pareto_raw_data.length - 1]}`,
                            color: '#FFFFFF',
                            font: {
                                size: 15,
                                family: 'Century Gothic',
                                weight: 'bold'
                            }
                        }
                    }
                }
            });
        } 
        else {
            paretoChart.data.labels = date_pareto_raw_data;
            paretoChart.data.datasets[0].data = arr_qty_passed;
            paretoChart.data.datasets[1].data = arr_qty_failed;
            paretoChart.data.datasets[2].data = set_parm_pareto;
            paretoChart.data.datasets[2].label = parm;
            paretoChart.options.plugins.title.text = `ATS Trend (${byProcess.split('\n')[0]}) : ${date_pareto_raw_data[0]} - ${date_pareto_raw_data[date_pareto_raw_data.length - 1]}`;
            paretoChart.update();
        }
    }
    // Create Pareto_Fail Chart
    else {
        document.getElementById('myLineChart').style.display = 'none';
        document.getElementById('myMixChart').style.display = 'none';
        document.getElementById('myParetoChart').style.display = 'none';
        document.getElementById('myParetoFailChart').style.display = 'block';
        document.getElementById('myMixChartSecond').style.display = 'none';

        var input_all = [];
        var total_fail = [];
        var total_percent_fail = [];
        group_pareto_raw_data.forEach(item => {
            if (Object.keys(item)[0] === dateCutOff) {
                input_all.push(parseInt(Object.values(item)[0][0]) + parseInt(Object.values(item)[0][1]))
                total_fail.push(Object.values(item)[0][1])
                total_percent_fail.push(Object.values(item)[0][3])
            }
        });
        var label = [];
        var pareto_fail = [];
        pareto_raw_data.forEach(item => {
            if (item[modeDayOption] === dateCutOff && item.Result !== 'PASS') {
                pareto_fail.push(item.QTY)
                label.push(item.Result)
            }
        })

        var pareto_data_fail = {
            labels: label,
            datasets: [
                {
                    label: '',
                    backgroundColor: 'rgba(255, 0, 0, 0.5)',
                    data: pareto_fail,
                    qty_in: input_all,
                    qty_total_fail: total_fail,
                    qty_percent_fail: total_percent_fail
                }
            ]
        };
        if (!paretoFailChart) {
            var ctx_mix_fail = document.getElementById('myParetoFailChart').getContext('2d');
            paretoFailChart = new Chart(ctx_mix_fail, {
                type: 'bar',
                data: pareto_data_fail,
                options: {
                    responsive: true,
                    scales: {
                        x: {
                            stacked: true,
                            offset: true,
                            title: {
                                display: true,
                                text: 'FAILURE',
                                color: '#FFFFFF',
                                font: {
                                    size: 15,
                                    family: 'Century Gothic',
                                    weight: 'bold'
                                }
                            },
                            ticks: {
                                color: '#FFFFFF'
                            }
                        },
                        y: {
                            stacked: true,
                            title: {
                                display: false,
                                color: '#FFFFFF',
                                font: {
                                    size: 15,
                                    family: 'Century Gothic',
                                    weight: 'bold'
                                }
                            },
                            ticks: {
                                color: '#FFFFFF'
                            }
                        }
                    },
                    plugins: {
                        tooltip: {
                            mode: 'index', // Display multiple tooltips at once
                            intersect: false,
                            callbacks: {
                                label: function (context) {
                                    var value = context.dataset.data[context.dataIndex];
                                    var qty = context.dataset.qty_in[0];
                                    var percent_fail = ((context.dataset.qty_percent_fail[0] * value) / context.dataset.qty_total_fail[0]).toFixed(2);
                                    return `FAIL : ${value} | (${percent_fail} %) | Qty : ${qty}`
                                }
                            }
                        },
                        legend: {
                            display: false
                        },
                        title: {
                            display: true,
                            text: dateCutOff,
                            color: '#FFFFFF',
                            font: {
                                size: 15,
                                family: 'Century Gothic',
                                weight: 'bold'
                            }
                        }
                    }
                }
            });
        }
        else {
            paretoFailChart.data = pareto_data_fail;
            paretoFailChart.options.plugins.title.text = dateCutOff;
            paretoFailChart.update();
        }
    }
}