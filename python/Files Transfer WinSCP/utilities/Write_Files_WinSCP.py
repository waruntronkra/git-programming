import paramiko

class WriteFilesWinSCP:
    def run(self, host, username, password, port, state, remote_path, file_name):
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
            with sftp.open(remote_path + file_name, 'w') as f:
                f.write(state)
            
            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return "success"

        except Exception as e:
            return e