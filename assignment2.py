#!/usr/bin/evn python3
import argparse #purpose: to parse command line arguments
import os  # purpose: to interact with the operating system
import subprocess  # purpose: to run shell commands ie, rsync
import shutil  # purpose: to copy files
from datetime import datetime  # purpose: to get the current date and time
import getpass  # purpose: to get the current user
import sys  # purpose: to exit the program

CLIENT_IPS = ['192.168.27.5', '192.168.27.10']  # Client-One and Client-Two
CLIENT_MAPPING = {
    '192.168.27.5': 'Client-One',
    '192.168.27.10': 'Client-Two'
}  # Mapping of client IPs to client names to be used dirctory structure

def get_client_name(ip):
    '''
    Get the client name based on the IP address.
    '''
    return CLIENT_MAPPING.get(ip, ip)

def parse_args():
   '''
    Parse command line arguments.
    '''

def get_clients(clients_arg):


def update_symlink(link_path, target_path):


def perform_backup(client_ip, backup_type, ssh_user):
    client_name = get_client_name(client_ip)  # Get the client name based on the IP address
    timestamp = datetime.now().strftime("%Y%m%d-%H%M%S") # Get the current date and time
    dest_base = f"/home/lmde/backup/{client_name}" # Destination base directory
    backup_dir = os.path.join(dest_base, backup_type, timestamp) # Create the backup directory
    source_path = f"{ssh_user}@{client_ip}:/home/lmde/dmuhammad4/" # Source path for the backup

    #creatting destination directory
    try:
        os.makedirs(backup_dir, exist_ok=True) # Create the backup directory
    except OSError as e:
        print(f"Error crating backup directory: {e}") # Print error message if directory creation fails
        raise

    # Determine link destination based on backup type
    link_dest = None  # Initialize link destination
    if backup_type == 'incremental':  #if backup type is incremental
        latest_link = os.path.join(dest_base, 'latest') # Create the latest link path
        if not os.path.exists(latest_link): # Check if the latest link exists
            raise Exception(f"No existing backup found for incremental backup on {client}") # Print error message if latest link does not exist
        link_dest = os.path.realpath(latest_link)  # Get the real path of the latest link
    elif backup_type == 'differential': #if backup type is differential
        latest_full_link = os.path.join(dest_base, 'latest_full')  # Create the latest full link path
        if not os.path.exists(latest_full_link): # Check if the latest full link exists
            raise Exception(f"No full backup found for differential backup on {client}")  # Print error message if latest full link does not exist
        link_dest = os.path.realpath(latest_full_link)  # Get the real path of the latest full link

    # Build the rsync command
    rsync_cmd = [  # Initialize the rsync command
        'rsync', # Purpose: to synchronize files and directories
        '-az', # Purpose: to archive and compress files
        '--delete', # Purpose: to delete files that are not in the source
        '-e', 'shh -o StrictHostKeyChecking=no', # Purpose: to use ssh for remote access
    ]
    if link_dest: # If link destination is not None
        rsync_cmd.extend(['--link-dest', link_dest]) # Add the link destination to the command
    rsync_cmd.extend([source_path, backup_dir])  # Add source and destination to the command


def main():


