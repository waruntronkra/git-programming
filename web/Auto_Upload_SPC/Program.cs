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

app.Run();