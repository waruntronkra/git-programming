import paramiko
import os
import csv

class ConnectWinSCP_GET:
    def start_get_file(self):
        print("Run...")
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Set the remote folder path
        remote_folder_path = '/data/Storage/'

        # List files in the remote folder
        file_list = sftp.listdir(remote_folder_path)

        list_csv_files = [file for file in file_list if file.endswith('.csv')]

        STATION_NAME = []
        for x in list_csv_files:
            split = x.split('_')
            merged = split[2] + "_" + split[3] + "_" + split[4]
            merged = merged.split(' ')
            STATION_NAME.append(merged[0])

        path_csv = []
        for i in list_csv_files:
            path_csv.append(remote_folder_path + i)

        Dict_Data = {}
        Dict_Time = {}
        if len(path_csv) > 0:
            for csv_file, station in zip(path_csv, STATION_NAME):
                with sftp.open(csv_file, 'r') as f:
                    csv_reader = csv.reader(f)
                    next(csv_reader)

                    column_temp = [row[3] for row in csv_reader]                
                    Dict_Data[station] = column_temp

                    column_time = [row[4] for row in csv_reader]
                    Dict_Time[station] = column_time

            return Dict_Data, STATION_NAME, Dict_Time

        else:
            return []
        
        # Close the SFTP session and SSH connection
        sftp.close()
        client.close()

