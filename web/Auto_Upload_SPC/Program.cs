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

app.MapPost("/query-date-latest", async (HttpContext context) => {
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
                    SELECT TOP (1) convert(varchar, date_time, 22) as Local_Date_Time
                    FROM [dbAcacia_VW].[dbo].[vw_attribute]
                    WHERE serial_no = '{serial_number}'
                    AND OPERATION = 'SPC270'
                    ORDER BY date_time DESC
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

app.MapGet("/webservice-fits", async (HttpContext context) => {
    var serial_number = context.Request.Query["serialnumber"];
    var operation = context.Request.Query["operation"];
    var type = context.Request.Query["type"];
    var parameter = context.Request.Query["parameter"];
    var value = context.Request.Query["value"];
    var model = context.Request.Query["model"];
    var revision = context.Request.Query["revision"];

    var client = new HttpClient();

    var request = new HttpRequestMessage(HttpMethod.Post, "https://service.fabrinet.co.th/FBNFITSService/FBNFITSServices.svc");
    request.Headers.Add("SOAPAction", $"http://tempuri.org/IFBNFITSServices/{type}");

    var optional_code = $"<tem:serial>{serial_number}</tem:serial>";
    if (type == "fn_Log") {
        optional_code = $@"
                            <tem:parameters>{parameter}</tem:parameters>
                            <tem:values>{value}</tem:values>
                            <tem:fsp>,</tem:fsp>
                        ";
    }
    
    var content = new StringContent($@"
                                        <x:Envelope
                                            xmlns:x='http://schemas.xmlsoap.org/soap/envelope/'
                                            xmlns:tem='http://tempuri.org/'>
                                            <x:Header/>
                                            <x:Body>
                                                <tem:{type}>
                                                    <tem:project_id>279</tem:project_id>
                                                    <tem:user_name>acaciax</tem:user_name>
                                                    <tem:user_password>acaciawebservice</tem:user_password>
                                                    <tem:model>{model}</tem:model>
                                                    <tem:operation>{operation}</tem:operation>
                                                    <tem:revision>{revision}</tem:revision>
                                                    {optional_code}
                                                </tem:{type}>
                                            </x:Body>
                                        </x:Envelope>", null, "text/xml"
                                    );

    request.Content = content;
    var response = await client.SendAsync(request);
    response.EnsureSuccessStatusCode();

    var data = await response.Content.ReadAsStringAsync();

    context.Response.ContentType = "text/xml";
    await context.Response.WriteAsync(data);
});

app.Run();