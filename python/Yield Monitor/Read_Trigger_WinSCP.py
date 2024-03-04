import paramiko
import os

class ReadTriggerWinSCP:
    def start_read_trigger_file(self):
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Set the remote folder path
        remote_folder_path = '/data/Storage/Log_Test_Result/run_state.txt'

        with sftp.open(remote_folder_path, 'r') as f:
            file_read = f.read()

        return file_read

        # Close the SFTP session and SSH connection
        sftp.close()
        client.close()

