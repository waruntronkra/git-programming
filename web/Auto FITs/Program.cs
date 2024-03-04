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

app.MapGet("/get-param-fits", async (HttpContext context) => {
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var process = context.Request.Query["process"];
    var sqlQuery = $@"
                    SELECT [PARAMETER] FROM [dbAcacia_Center].[dbo].[tb_web_FITs] NOLOCK WHERE [PROCESS] = '{process}'
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

app.MapGet("/get-last-test", async (HttpContext context) => {
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var parameter = context.Request.Query["parameter"];
    var sn = context.Request.Query["sn"];
    var process = context.Request.Query["process"];

    var sqlQuery = $@"
                    [dbAcacia_Center]..[sp_web_FITs]
                    @param = '{parameter}',
                    @sn = '{sn}',
                    @process = '{process}'
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

app.MapGet("/get-model", async (HttpContext context) => {
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();
   
    var sqlQuery = $@"
                    SELECT DISTINCT [buildtype] FROM [dbAcacia_VW].[dbo].[vw_event_master]
                    where sn_attr_code in ('1001','410001','1100001','100000001') 
                    and model is not null 
                    and model not in ('','n/a','RMA','na')
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

app.MapGet("/get-pn", async (HttpContext context) => {
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();
   
    var sqlQuery = $@"
                    SELECT DISTINCT [part_no] FROM [dbAcacia_VW].[dbo].[vw_event_master]
                    where sn_attr_code in ('1001','410001','1100001','100000001') 
                    and part_no is not null
                    and part_no not in ('','n/a','na')
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

app.MapGet("/get-workflow", async (HttpContext context) =>
{
    var server = "FITS-026,14000";
    var database = "dbAcacia_VW";
    var username = "ACACIA_USER";
    var password = "User@cac1a";
    var connectionString = $"Server={server};Database={database};User Id={username};Password={password};";

    using var connection = new SqlConnection(connectionString);
    await connection.OpenAsync();

    var serial_number = context.Request.Query["serialnumber"];
   
    var sqlQuery = $@"
                    SELECT * FROM vw_attribute WITH(NOLOCK)
                    WHERE serial_no IN (
                        SELECT buildtype FROM vw_event_master WITH(NOLOCK) 
                        WHERE sn_attr_code  = 410001 AND serial_no = '{serial_number}'
                    )
                    AND description LIKE 'Seq%'
                    AND attribute_value not in ('-')
                    order by date_time DESC
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
