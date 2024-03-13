using System.Text.Json;
using System.Data.SqlClient;

var builder = WebApplication.CreateBuilder(args);
var app = builder.Build();

app.UseStaticFiles();

app.MapGet("/", (HttpContext context) => {
    var filePath = Path.Combine(Directory.GetCurrentDirectory(), "wwwroot", "index.html");
    if (File.Exists(filePath)) {
        return context.Response.SendFileAsync(filePath);
    }
    else {
        context.Response.StatusCode = 404;
        return context.Response.WriteAsync("File not found!");
    }
});

app.MapPost("/query-data", async (HttpContext context) => {
    var server = "Acacia_Test_DB,14000";
    var database = "ATSResults";
    var username = "ats_read";
    var password = "R6ad4r#Acac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    // Recieve (json) POST from Javascript
    var requestBody = await new StreamReader(context.Request.Body).ReadToEndAsync();
    var requestData = JsonSerializer.Deserialize<Dictionary<string, string>>(requestBody);
    var day = requestData?["day"];

    var sqlQuery = $@"
                    SELECT 
                    UUT.UUT_SERIAL_NUMBER,
                    convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) as START_DATE_TIME,
                    UUT.HW_PART_NUMBER,
                    CONCAT(UUT.STATION_ID,'_',UUT.TEST_SOCKET_INDEX) AS MC_Slot,
                    (SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_TYPE in ('NumericLimitTest') AND SR.STEP_NAME LIKE ('ACR1_Avg%%'))) AS ACR1_Avg,
                    (SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_TYPE in ('NumericLimitTest') AND SR.STEP_NAME LIKE ('Max_ACR1_Dev%%'))) AS Max_ACR1_Dev
                    FROM [ATSResults].[dbo].[UUT_RESULT] UUT WITH(NOLOCK)

                    Where UUT.PROCESS in ('KGB')
                    AND convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) > getdate()-{day}
                    AND UUT.MODE in ('KGB')
                    AND UUT.UUT_STATUS in ('Passed')
                    AND UUT.TPS_NAME in ('uITLA TEC ACR SPC Test')
                    Order by UUT.START_DATE_TIME desc
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

app.MapPost("/query-data-last", async (HttpContext context) => {
    var server = "Acacia_Test_DB,14000";
    var database = "ATSResults";
    var username = "ats_read";
    var password = "R6ad4r#Acac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var sqlQuery = $@"
                    SELECT 
                    UUT.UUT_SERIAL_NUMBER,
                    convert(varchar,DATEADD(hour, 7, START_DATE_TIME),22) as START_DATE_TIME,
                    UUT.HW_PART_NUMBER,
                    CONCAT(UUT.STATION_ID,'_',UUT.TEST_SOCKET_INDEX) AS MC_Slot,
                    (SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_TYPE in ('NumericLimitTest') AND SR.STEP_NAME LIKE ('ACR1_Avg%%'))) AS ACR1_Avg,
                    (SELECT Top 1 DT.DATA FROM [ATSResults].[dbo].[PROP_RESULT] DT WHERE DT.STEP_RESULT = (SELECT Top 1 SR.ID FROM [ATSResults].[dbo].[STEP_RESULT] SR WITH(NOLOCK) WHERE SR.UUT_RESULT = UUT.ID AND SR.STEP_TYPE in ('NumericLimitTest') AND SR.STEP_NAME LIKE ('Max_ACR1_Dev%%'))) AS Max_ACR1_Dev
                    
                    FROM [ATSResults].[dbo].[UUT_RESULT] UUT WITH(NOLOCK)

                    Where UUT.PROCESS in ('KGB')
                    AND convert(varchar, DATEADD(hour, 7, START_DATE_TIME),22) = CONVERT(DATE, GETDATE())
                    AND UUT.MODE in ('KGB')
                    AND UUT.UUT_STATUS in ('Passed')
                    AND UUT.TPS_NAME in ('uITLA TEC ACR SPC Test')
                    Order by UUT.START_DATE_TIME desc
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