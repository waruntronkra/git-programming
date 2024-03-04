import paramiko
import os

class ConnectWinSCP_READ:
    def start_read_file(self):
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Set the remote folder path
        remote_folder_path = '/data/ORL utility [Programmatically]/Fiber_Inspection_Record/'
        remote_files = sftp.listdir(remote_folder_path)
        txt_files = [file for file in remote_files if file.endswith('.txt')]

        local_folder_path = 'temp'

        # Copy .txt files from remote to local
        for txt_file in txt_files:
            remote_path = os.path.join(remote_folder_path, txt_file)
            local_path = os.path.join(local_folder_path, txt_file)
            sftp.get(remote_path, local_path)

        # Close the SFTP session and SSH connection
        sftp.close()
        client.close()

ConnectWinSCP_READ().start_read_file()

