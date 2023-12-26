from ftplib import FTP
import os

def upload_file_to_ftp(ftp_server, username, password, local_file_path):
    try:
        # Connect to the FTP server
        ftp = FTP(ftp_server)
        ftp.login(username, password)

        # Read the remote folder from the text file
        with open("uploaded_files.txt", 'r') as folder_file:
            remote_folder = folder_file.read().strip()

        # Change to the remote folder (create it if it doesn't exist)
        ftp.cwd(remote_folder)

        # Open the local file in binary mode
        with open(local_file_path, 'rb') as local_file:
            # Upload the file to the server
            ftp.storbinary('STOR ' + os.path.basename(local_file_path), local_file)

        print(f"File '{os.path.basename(local_file_path)}' uploaded successfully to '{remote_folder}' on {ftp_server}")

        # Clear the contents of the text file after successful upload
        with open("uploaded_files.txt", 'w') as folder_file:
            folder_file.write("")

    except Exception as e:
        print(f"Error: {e}")

    finally:
        # Close the FTP connection
        ftp.quit()

# Replace these values with your FTP server details and file paths
ftp_server = 'ftp.adisingh.in'
username = 'tgftpbot@adisingh.in'
password = 'eB]++DGxPGEW'
local_file_path = 'index.php'

upload_file_to_ftp(ftp_server, username, password, local_file_path)
