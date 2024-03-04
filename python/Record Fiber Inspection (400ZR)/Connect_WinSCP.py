import paramiko
import os
import csv

class ConnectWinSCP_GET:
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
        remote_folder_path = '/data/Storage/Result/'

        # List files in the remote folder
        file_list = sftp.listdir(remote_folder_path)

        list_csv_files = [file for file in file_list if file.endswith('.csv')]

        path_csv = []
        for i in list_csv_files:
            path_csv.append(remote_folder_path + i)

        group = {}
        for index, i in enumerate(path_csv):
            array = []
            with sftp.open(i, 'r') as f:
                csv_reader = csv.reader(f)
                for row in csv_reader:
                    array.append(row)
            group[str(list_csv_files[index].split('.')[0])] = array
        
        # Close the SFTP session and SSH connection
        sftp.close()
        client.close()

        if csv_reader:
            return group
        else:
            return 99

