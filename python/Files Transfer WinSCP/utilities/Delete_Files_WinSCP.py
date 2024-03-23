import paramiko

class DeleteFilesWinSCP:
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
            
            files = [f for f in sftp.listdir(remote_path)]
            if file_name in files:
                sftp.remove(f"{remote_path}/{file_name}")
            else:
                return f"Not file {file_name} in {remote_path}"

            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

            return "success"

        except Exception as e:
            return e

        finally:
            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()