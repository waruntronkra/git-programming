[Get start create Web API C#]
CMD = dotnet new web -n folder_name

[Package SQL]
CMD = dotnet add package System.Data.SqlClient

[Package WinSCP]
CMD = dotnet add package WinSCP --version 6.3.2

[Publish .NET]
CMD = dotnet publish --configuration Release --output "\\10.3.2.120\d$\web_sites\web-api"
