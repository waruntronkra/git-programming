import paramiko
import os

class CopyFilesWinSCP:
    def run(self, host, username, password, port, remote_path, local_path, file_name, extension_file):
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
            files = [file for file in sftp.listdir(remote_path) if file.endswith(extension_file)]
            if len(files) > 0:
                for f in files:
                    sftp.get(os.path.join(remote_path, f), os.path.join(local_path, f))
                    
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
