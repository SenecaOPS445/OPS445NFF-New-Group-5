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
    if clients_arg.lower() == 'all':  # If the user types "all" it returns the full list of IP addresses.
        return CLIENT_IPS # Return all client IP addresses stored in the CLIENT_IPS list.
    return [ip.strip() for ip in clients_arg.split(',')] # this splits the addresses into individual IPs, removes any spaces, and returns them as a list.


def update_symlink(link_path, target_path):


def perform_backup(client_ip, backup_type, ssh_user):


def main():

