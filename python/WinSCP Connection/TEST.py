import pysftp

def upload_file(hostname, username, password, local_path, remote_path):
    try:
        # Connect to the SFTP server
        with pysftp.Connection(hostname, username=username, password=password) as sftp:
            # Change to the desired remote directory (if needed)
            sftp.chdir(remote_path)

            # Upload the file to the server
            sftp.put(local_path)

            print(f"File '{local_path}' uploaded to '{remote_path}' successfully.")

    except Exception as e:
        print(f"Error: {e}")

# Replace these values with your SFTP server details
hostname = '144.121.8.174'
username = 'waruntronk'
password = 'IEpHoiFOqXaZ6'
local_path = '/data/ORL utility [Programmatically]/Fiber_Inspection_Record/'
remote_path = '/remote/directory/file.txt'

# Call the function to upload the file
upload_file(hostname, username, password, local_path, remote_path)
