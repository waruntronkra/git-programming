using System.Text.Json;
using System.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();

app.MapGet("/", (HttpContext context) =>
{
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

app.MapPost("/get-linecard-usage", async (HttpContext context) => {
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    // Recieve (json) POST from Javascript
    var requestBody = await new StreamReader(context.Request.Body).ReadToEndAsync();
    var requestData = JsonSerializer.Deserialize<Dictionary<string, string>>(requestBody);
    var serial_number = requestData?["sn"];
    
    var sqlQuery = $@"
                    SELECT [Line Card Serial Number]
                        ,[Usage Counts]
                        ,[Remaining Usage]
                        ,[Rework Counts]
                        ,[Current OPN]
                        ,[Current M/C]
                        ,[Latest Module SN]
                        ,[Latest Using Date]
                    FROM [dbAcacia_VW].[dbo].[vw_linecard_mapping]
                    WHERE [Line Card Serial Number] in ({serial_number})
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

app.MapPost("/get-linecard-today", async (HttpContext context) => {
    var server = "10.6.1.145,14000";
    var database = "ATSResults";
    var username = "ats_read";
    var password = "R6ad4r#Acac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var sqlQuery = $@"
                    SELECT DISTINCT [FIXTURE_ID]
   
                    FROM [ATSResults].[dbo].[vw_test_defect_latest]
                    WHERE PROCESS = 'EBT'
                    AND CONVERT(date, DATEADD(hour, 7, START_DATE_TIME)) = CONVERT(date, GETDATE())
                    and FIXTURE_ID not in ('')
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

app.Run();

