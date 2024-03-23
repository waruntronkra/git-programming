import paramiko

class WriteFilesWinSCP:
    def run(self, host, username, password, port, state):
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
            remote_folder_path = '/data/FTP/state.txt'

            # Put files to the remote folder
            with sftp.open(remote_folder_path, 'w') as f:
                f.write(state)
            
            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return "success"

        except Exception as e:
            return e