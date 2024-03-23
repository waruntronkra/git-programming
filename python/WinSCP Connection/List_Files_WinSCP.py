import paramiko

class ListFilesWinSCP:
    def run(self, remote_path):
        try:
            # Create an SSH client
            client = paramiko.SSHClient()

            # Automatically add the server's host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SFTP server
            client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

            # Open an SFTP session
            sftp = client.open_sftp()

            remote_files = sftp.listdir(remote_path)
            files = [file for file in remote_files]

            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return files

        except Exception as e:
            return e