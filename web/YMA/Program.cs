using Microsoft.AspNetCore.Builder;
using Microsoft.AspNetCore.Hosting;
using Microsoft.AspNetCore.Http;
using Microsoft.Extensions.DependencyInjection;
using Microsoft.Extensions.Hosting;
using Microsoft.Extensions.FileProviders;
using System.IO;
using System.Data.SqlClient;
using System.Text.Json;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();

app.MapGet("/", (HttpContext context) => {
    var filePath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "index.html");

    if (File.Exists(filePath))
    {
        return context.Response.SendFileAsync(filePath);
    }
    else
    {
        context.Response.StatusCode = 404;
        return context.Response.WriteAsync("File not found");
    }
});

app.MapGet("/fetch_data", async (HttpContext context) => {
    var server = "10.6.1.145,14000";
    var database = "ATS_Center";
    var username = "db_rw";
    var password = "Wr1te4@sta";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var by_Process_Mode = "";

    var selectedDay = context.Request.Query["days"];
    var selectedProduct = context.Request.Query["selected_Product"];
    var selectedModel = context.Request.Query["selected_Model"];
    var modeDayOption = context.Request.Query["mode_day_option"];
    var by_Process = context.Request.Query["by_Process"];

    if (!string.IsNullOrEmpty(by_Process)) {
        by_Process_Mode = $"@Process = '{by_Process}',";
    }

    var sqlQuery = $@"
                    ATS_Center..[71_sp_All_Report]
                    @Level = '{selectedProduct}',
                    @Model = '{selectedModel}',
                    {by_Process_Mode}
                    @Backward = '{selectedDay}',
                    @BackTo = '1',
                    @GroupBy = '{modeDayOption}',
                    @DrillOn = 'YIELD',
                    @IncEngBld = '3',
                    @Filter = ' AND Mode IN(''Production'', ''NPI'')',
                    @PreTest = '1',
                    @MinCumCal = '1',
                    @FirstMonth = '0'
        ";
    using var command = new SqlCommand(sqlQuery, connection);
    using var reader = await command.ExecuteReaderAsync();

    var data = new List<Dictionary<string, object>>();

    while (await reader.ReadAsync()) {
        var rowData = new Dictionary<string, object>();

        for (int i = 0; i < reader.FieldCount; i++) {
            var columnName = reader.GetName(i);
            var value = reader[i];

            rowData.Add(columnName, value);
        }
        data.Add(rowData);
    }

    var jsonData = JsonSerializer.Serialize(new { data });

    context.Response.ContentType = "application/json";
    await context.Response.WriteAsync(jsonData);
});

app.MapGet("/fetch_data_by_Process", async (HttpContext context) => {
    var server = "10.6.1.145,14000";
    var database = "ATS_Center";
    var username = "db_rw";
    var password = "Wr1te4@sta";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var by_Process_Mode = "";

    var selectedDay = context.Request.Query["days"];
    var selectedProduct = context.Request.Query["selected_Product"];
    var selectedModel = context.Request.Query["selected_Model"];
    var modeDayOption = context.Request.Query["mode_day_option"];
    var by_Process = context.Request.Query["by_Process"];
    var process_from_table = context.Request.Query["process_from_table"];

    if (!string.IsNullOrEmpty(by_Process)) {
        by_Process_Mode = $"@Process = '{by_Process}',";
    }

    var sqlQuery = $@"
                    ATS_Center..[71_sp_All_Report]
                    @Level = '{selectedProduct}',
                    @Model = '{selectedModel}',
                    @Process  = '{process_from_table}',
                    @Backward = '{selectedDay}',
                    @BackTo = '1',
                    @GroupBy = '{modeDayOption}',
                    @DrillOn = 'RAW DATA',
                    @IncEngBld = '3',
                    @Filter = ' AND Mode IN(''Production'', ''NPI'')',
                    @PreTest = '1',
                    @MinCumCal = '1',
                    @FirstMonth = '0'
        ";
    using var command = new SqlCommand(sqlQuery, connection);
    using var reader = await command.ExecuteReaderAsync();

    var raw_data = new List<Dictionary<string, object>>();
    var column_names = new List<String>();

    while (await reader.ReadAsync()) {
        var rowData = new Dictionary<string, object>();

        for (int i = 0; i < reader.FieldCount; i++) {
            var columnName = reader.GetName(i);
            var value = reader[i];

            rowData.Add(columnName, value);
            column_names.Add(columnName);
        }
        raw_data.Add(rowData);
    }

    string[] col_name = column_names.Distinct().ToArray();
    var jsonData = JsonSerializer.Serialize(new { raw_data, col_name });

    context.Response.ContentType = "application/json";
    await context.Response.WriteAsync(jsonData);
});

app.MapGet("/history_UUT", async (HttpContext context) => {
    var server = "10.6.1.145,14000";
    var database = "ATSResults";
    var username = "ats_read";
    var password = "R6ad4r#Acac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var code = "";

    var UUT_SN_selected = context.Request.Query["UUT_SN_selected"];
    var Query_Mode = context.Request.Query["Query_Mode"];

    if (Query_Mode == "All") {
        code = "";
    }
    else if (Query_Mode == "Passed") {
        code = "AND UUT_STATUS = 'Passed'";
    }
    else if (Query_Mode == "Failed") {
        code = "AND UUT_STATUS not in ('Passed')";
    }

    var sqlQuery = $@"
                    SELECT [ID]
                        ,[STATION_ID]
                        ,[BATCH_SERIAL_NUMBER]
                        ,[TEST_SOCKET_INDEX]
                        ,[UUT_SERIAL_NUMBER]
                        ,[USER_LOGIN_NAME]
                        ,[START_DATE_TIME]
                        ,convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) as LOCAL_START_DATE_TIME
                        ,[EXECUTION_TIME]
                        ,[UUT_STATUS]
                        ,[UUT_ERROR_CODE]
                        ,[UUT_ERROR_MESSAGE]
                        ,[LOT_CODE]
                        ,[FIXTURE_ID]
                        ,[MODE]
                        ,[PROCESS]
                        ,[TEST_COUNT]
                        ,[PRODUCT_CODE]
                        ,[PRODUCT_CODE_REV]
                        ,[HW_PART_NUMBER]
                        ,[HW_REV]
                        ,[TPS_NAME]
                        ,[TPS_PART_NUMBER]
                        ,[TPS_REV]
                        ,[SW_NAME]
                        ,[SW_PART_NUMBER]
                        ,[SW_REV]
                        ,[FW_NAME]
                        ,[FW_PART_NUMBER]
                        ,[FW_REV]
                        ,[FAIL_MODE]
                    FROM [ATSResults].[dbo].[vw_test_defect] WITH(NOLOCK)
                    WHERE UUT_SERIAL_NUMBER = '{UUT_SN_selected}'
                    {code}
                    ORDER BY START_DATE_TIME DESC
        ";
    using var command = new SqlCommand(sqlQuery, connection);
    using var reader = await command.ExecuteReaderAsync();

    var raw_data = new List<Dictionary<string, object>>();
    var column_names = new List<String>();

    while (await reader.ReadAsync()) {
        var rowData = new Dictionary<string, object>();

        for (int i = 0; i < reader.FieldCount; i++) {
            var columnName = reader.GetName(i);
            var value = reader[i];

            rowData.Add(columnName, value);
            column_names.Add(columnName);
        }
        raw_data.Add(rowData);
    }

    string[] col_name = column_names.Distinct().ToArray();
    var jsonData = JsonSerializer.Serialize(new { raw_data, col_name });

    context.Response.ContentType = "application/json";
    await context.Response.WriteAsync(jsonData);
});

app.MapGet("/pareto_query_all_process", async (HttpContext context) => {
    var server = "10.6.1.145,14000";
    var database = "ATS_Center";
    var username = "db_rw";
    var password = "Wr1te4@sta";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var code_with_process = "";

    var selectedDay = context.Request.Query["days"];
    var selectedProduct = context.Request.Query["selected_Product"];
    var selectedModel = context.Request.Query["selected_Model"];
    var modeDayOption = context.Request.Query["mode_day_option"];
    var by_Process = context.Request.Query["by_Process"];

    if (!string.IsNullOrEmpty(by_Process)) {
        code_with_process = $"@Process = '{by_Process}',";
    }
    else {
        code_with_process = "";
    }

    var sqlQuery = $@"
                    ATS_Center..[71_sp_All_Report]
                    @Level = '{selectedProduct}',
                    @Model = '{selectedModel}',
                    {code_with_process}
                    @Backward = '{selectedDay}',
                    @BackTo = '1',
                    @GroupBy = '{modeDayOption}',
                    @DrillOn = 'PARETO',
                    @IncEngBld = '3',
                    @Filter = ' AND Mode IN(''Production'', ''NPI'')',
                    @PreTest = '1',
                    @MinCumCal = '1',
                    @FirstMonth = '0'
        ";
    using var command = new SqlCommand(sqlQuery, connection);
    using var reader = await command.ExecuteReaderAsync();

    var raw_data = new List<Dictionary<string, object>>();

    while (await reader.ReadAsync()) {
        var rowData = new Dictionary<string, object>();

        for (int i = 0; i < reader.FieldCount; i++) {
            var columnName = reader.GetName(i);
            var value = reader[i];

            rowData.Add(columnName, value);
        }
        raw_data.Add(rowData);
    }

    var jsonData = JsonSerializer.Serialize(new { raw_data });

    context.Response.ContentType = "application/json";
    await context.Response.WriteAsync(jsonData);
});

app.Run();
