import paramiko

class ListFilesWinSCP:
    def run(self, host, username, password, port, remote_path):
        try:
            # Create an SSH client
            client = paramiko.SSHClient()

            # Automatically add the server's host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SFTP server
            client.connect(host, port=port, username=username, password=password)

            # Open an SFTP session
            sftp = client.open_sftp()

            # Set the remote folder path
            remote_folder_path = '/data/FTP/'
            remote_files = sftp.listdir(remote_path)
            files = [file for file in remote_files]

            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return files

        except Exception as e:
            return e