import paramiko

class ConnectWinSCP_CLEAR_PDF:
    def clear_pdf_files(self):
        # Create an SSH client
        client = paramiko.SSHClient()

        # Automatically add the server's host key
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

        # Connect to the SFTP server
        client.connect('144.121.8.174', port=2666, username='waruntronk', password='IEpHoiFOqXaZ6')

        # Open an SFTP session
        sftp = client.open_sftp()

        # Set the remote folder path where PDF files need to be cleared
        remote_folder_path = '/path/to/your/remote/folder'

        try:
            # List all files in the remote folder
            files = sftp.listdir(remote_folder_path)

            for file_name in files:
                if file_name.endswith('.pdf'):
                    # Construct the full path of the PDF file
                    pdf_file_path = f"{remote_folder_path}/{file_name}"

                    # Remove the PDF file
                    sftp.remove(pdf_file_path)

        except Exception as e:
            print(f"Error: {e}")

        finally:
            # Close the SFTP session and SSH connection
            sftp.close()
            client.close()

if __name__ == "__main__":
    connector = ConnectWinSCP_CLEAR_PDF()
    connector.clear_pdf_files()
