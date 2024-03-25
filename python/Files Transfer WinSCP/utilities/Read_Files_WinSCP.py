import paramiko

class ReadFilesWinSCP:
    def run(self, host, username, password, port, remote_path, file_name):
        try:
            # Create an SSH client
            client = paramiko.SSHClient()

            # Automatically add the server's host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SFTP server
            client.connect(host, port=port, username=username, password=password)

            # Open an SFTP session
            sftp = client.open_sftp()

            # Put files to the remote folder
            with sftp.open(remote_path + file_name, 'r') as f:
                file_read = f.read()
            
            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return f'{file_read}'

        except Exception as e:
            return e