import paramiko

class WriteFilesWinSCP:
    def run(self, remote_path, file_name, state):
        try:
            # Create an SSH client
            client = paramiko.SSHClient()

            # Automatically add the server's host key
            client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

            # Connect to the SFTP server
            client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

            # Open an SFTP session
            sftp = client.open_sftp()

            files = [f for f in sftp.listdir(remote_path)]
            if file_name in files:
                with sftp.open(f'{remote_path}{file_name}', 'w') as f:
                    f.write(state)

                # Close the SFTP session and SSH connection
                sftp.close()
                client.close()

                return 'success'
            else:
                # Close the SFTP session and SSH connection
                sftp.close()
                client.close()
                
                return f"Not found file {file_name} in {remote_path}"
            
            


        except Exception as e:
            return e