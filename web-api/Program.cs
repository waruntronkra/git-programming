using System.Data.SqlClient;
using System.Text.Json;
using System.Diagnostics;
using WinSCP;
using System;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.MapGet("/", () => "Hello World!");

app.MapGet("/query-data-last", async (HttpContext context) =>
{
    var server = "10.6.1.145,14000";
    var database = "ATSResults";
    var username = "ats_read";
    var password = "R6ad4r#Acac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    var serial_number = context.Request.Query["serialnumber"];
    var process = context.Request.Query["operation"];

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var sqlQuery = @"
                    SELECT [STATION_ID], [TEST_SOCKET_INDEX], [TEST_COUNT]
                    FROM [ATSResults].[dbo].[vw_test_defect_latest]
                    where UUT_SERIAL_NUMBER = @serial_number
                    and PROCESS = @process
                ";
    using var command = new SqlCommand(sqlQuery, connection);
    command.Parameters.AddWithValue("@serial_number", serial_number);
    command.Parameters.AddWithValue("@process", process);
    
    using var reader = await command.ExecuteReaderAsync();

    var data = new List<Dictionary<string, object>>();

    while (await reader.ReadAsync())
    {
        var rowData = new Dictionary<string, object>();

        for (int i = 0; i < reader.FieldCount; i++)
        {
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

app.Run();
