import paramiko
import zipfile

class GETFileWinSCP:
    def start_get_file(self):
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Set the remote folder path
        remote_folder_path = '/data/Storage/Log_Test_Result/log.zip'

        local_folder_path = 'temp/log/log.zip'

        # Download the file from the remote server to the local path
        sftp.get(remote_folder_path, local_folder_path)

        sftp.close()
        client.close()