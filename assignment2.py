#!/usr/bin/env python3
import argparse  # purpose: to parse command line arguments
import os  # purpose: to interact with the operating system
import subprocess  # purpose: to run shell commands, e.g., rsync
import shutil  # purpose: to copy files
from datetime import datetime  # purpose: to get the current date and time
import getpass  # purpose: to get the current user
import sys  # purpose: to exit the program

CLIENT_IPS = ['192.168.27.5', '192.168.27.10']  # Client-One and Client-Two
CLIENT_MAPPING = {
    '192.168.27.5': 'Client-One',
    '192.168.27.10': 'Client-Two'
}  # Mapping of client IPs to client names to be used in the directory structure


def get_client_name(ip):
    '''
    Get the client name based on the IP address.
    '''
    return CLIENT_MAPPING.get(ip, ip)


def parse_args():
    '''
    Create an ArgumentParser object with a description of the script's purpose.
    '''
    parser = argparse.ArgumentParser(description='Perform backups of client machines.')  # Creates an object, used to process command-line args.
    parser.add_argument('-t', '--type', required=True,  # Add a required argument for specifying the type of backup
                        choices=['full', 'incremental', 'differential'],  # Restrict the allowed values to full, incremental, or differential
                        help='Type of backup to perform')  # Provide a help message for the argument
    parser.add_argument('-c', '--clients', required=True,  # Add argument for specifying client IPs that specifies which clients to back up.
                        help='Comma-separated list of client IPs or "all"')  # User can use a comma to separate or "all" to backup all clients.
    parser.add_argument('--ssh-user', default='lmde',  # Add an optional argument for specifying the SSH username (default: 'lmde')
                        help='SSH username for client connections (default: lmde)')
    return parser.parse_args()  # This allows the calling function to access the provided arguments in a structured way.


def get_clients(clients_arg):
    '''
    Get the list of client IPs from the command line argument.
    '''
    if clients_arg.lower() == 'all':  # If the user types "all" it returns the full list of IP addresses.
        return CLIENT_IPS  # Return all client IP addresses stored in the CLIENT_IPS list.
    return [ip.strip() for ip in clients_arg.split(',')]  # this splits the addresses into individual IPs, removes any spaces, and returns them as a list.


def update_symlink(link_path, target_path):
    '''
    Update the symlink to point to the new backup. This function takes
    the symlink path and the target path as arguments. It checks if the
    symlink exists and removes it if it does. Then it creates a new
    symlink pointing to the target path. If an error occurs during the
    symlink update, it prints an error message and raises an exception.
    '''
    try:
        if os.path.lexists(link_path):  # Check if the symlink exists
            os.unlink(link_path)  # Remove the existing symlink
        os.symlink(target_path, link_path)  # Create a new symlink
    except OSError as e:  # Check if the symlink update was successful
        print(f"Error updating symlink {link_path}: {e}")  # Print error message if symlink update fails
        raise


def perform_backup(client_ip, backup_type, ssh_user):
    '''
    Perform the backup using rsync. it takes the client
    IP address, backup type (full, incremental, or differential),
    and SSH user as arguments. Determines link destination based on backup type.
    Builds the rsync command and runs it. Updates symlinks to point to the new backup.
    '''
    # Getting the client name based on the IP address
    client_name = get_client_name(client_ip)  # Get the client name based on the IP address
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")  # Get the current date and time
    dest_base = f"/home/lmde/backup/{client_name}"  # Destination base directory
    backup_dir = os.path.join(dest_base, backup_type, timestamp)  # Create the backup directory
    source_path = f"{ssh_user}@{client_ip}:/home/lmde/dmuhammad4/"  # Source path for the backup

    #creatting destination directory
    try:
        os.makedirs(backup_dir, exist_ok=True)  # Create the backup directory
    except OSError as e:
        print(f"Error creating backup directory: {e}")  # Print error message if directory creation fails
        raise

    # Determine link destination based on backup type
    link_dest = None  # Initialize link destination
    if backup_type == 'incremental':  # if backup type is incremental
        latest_link = os.path.join(dest_base, 'latest')  # Create the latest link path
        if not os.path.exists(latest_link):  # Check if the latest link exists
            raise Exception(f"No existing backup found for incremental backup on {client}")  # Print error message if latest link does not exist
        link_dest = os.path.realpath(latest_link)  # Get the real path of the latest link
    elif backup_type == 'differential':  # if backup type is differential
        latest_full_link = os.path.join(dest_base, 'latest_full')  # Create the latest full link path
        if not os.path.exists(latest_full_link):  # Check if the latest full link exists
            raise Exception(f"No full backup found for differential backup on {client}")  # Print error message if latest full link does not exist
        link_dest = os.path.realpath(latest_full_link)  # Get the real path of the latest full link

    # Build the rsync command
    rsync_cmd = [  # Initialize the rsync command
        'rsync',  # Purpose: to synchronize files and directories
        '-az',  # Purpose: to archive and compress files
        '--delete',  # Purpose: to delete files that are not in the source
        '-e', 'ssh -o StrictHostKeyChecking=no',  # Purpose: to use ssh for remote access
    ]
    if link_dest:  # If link destination is not None
        rsync_cmd.extend(['--link-dest', link_dest])  # Add the link destination to the command
    rsync_cmd.extend([source_path, backup_dir])  # Add source and destination to the command

    # Run the rsync command
    try:
        subprocess.run(rsync_cmd, check=True)  # Run the rsync command
    except subprocess.CalledProcessError as e:  # Check if the command was successful
        print(f"rsync failed for {client}: {e}")  # Print error message if rsync fails
        shutil.rmtree(backup_dir, ignore_errors=True)  # Remove the backup directory if rsync fails
        raise

    # Update the symlink to point to the new backup
    try:
        # Update global latest
        latest_link = os.path.join(dest_base, 'latest')  # Create the latest link path
        update_symlink(latest_link, backup_dir)  # Update the symlink to point to the new backup

        # Update type-specific latest
        type_latest = os.path.join(dest_base, backup_type, 'latest')  # Create the type-specific latest link path
        update_symlink(type_latest, timestamp)  # Update the symlink to point to the new backup

        # Update latest_full if full backup
        if backup_type == 'full':  # If the backup type is full
            latest_full_link = os.path.join(dest_base, 'latest_full')  # Create the latest full link path
            update_symlink(latest_full_link, backup_dir)  # Update the symlink to point to the new backup
    except Exception as e:  # Check if the symlink update was successful
        print(f"Error updating symlinks: {e}")  # Print error message if symlink update fails
        raise


def main():
    args = parse_args()  # Parse command-line arguments
    clients = get_clients(args.clients)  # Get list of clients from input (file or string)
    for client in clients:  # Loop through each client to perform backup
        print(f"Starting {args.type} backup for {client}")  # Notify backup start for this client
        try:
            perform_backup(client, args.type, args.ssh_user)  # Attempt to perform backup
            print(f"Successfully completed {args.type} backup for {client}") # Notify backup success
        except Exception as e:
            print(f"Failed {args.type} backup for {client}: {e}")  # Print error message if backup fails
            sys.exit()  # Exit program with error status

if __name__ == "__main__":  # Check if the script is being run directly
    main()  # Call the main function