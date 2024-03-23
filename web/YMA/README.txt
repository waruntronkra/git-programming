[Get start create Web API C#]
CMD = dotnet new web -n folder_name

[Package SQL]
CMD = dotnet add package System.Data.SqlClient

[Publish .NET]
CMD = dotnet publish --configuration Release --output "\\10.3.2.120\d$\web_sites\auto-upload-spc"
