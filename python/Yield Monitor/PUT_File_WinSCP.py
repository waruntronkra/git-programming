import paramiko
import csv

class PUTFileWinSCP:
    def start_put_file(self):
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Local file path
        local_file_path = 'temp/trigger/trigger.txt'

        # Set the remote folder path
        remote_folder_path = '/data/Storage/Log_Test_Result/'

        sftp.put(local_file_path, remote_folder_path + 'trigger.txt')

        sftp.close()
        client.close()

