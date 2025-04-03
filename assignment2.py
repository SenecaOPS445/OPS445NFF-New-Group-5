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
def parse_args(): #Defines a function that will handle command-line argument
    ''' Create an ArgumentParser object with a description of the script's purpose '''
    parser = argparse.ArgumentParser(description='Perform backups of client machines.') #Creates an object, used to process command-line args.
    
    parser.add_argument('-t', '--type', required=True,  # Add a required argument for specifying the type of backup
                        choices=['full', 'incremental', 'differential'],  # Restrict the allowed values to full, incremental, or differential
                        help='Type of backup to perform')  # Provide a help message for the argument
    
    parser.add_argument('-c', '--clients', required=True,  # Add argument for specifying client IPs that specifies which clients to back up.
                        help='Comma-separated list of client IPs or "all"') #User can use a comma to seperate or "all" to backup all clients.
    
    parser.add_argument('--ssh-user', default='lmde',  # Add an optional argument for specifying the SSH username (default: 'lmde')
                        help='SSH username for client connections (default: lmde)')
    
    return parser.parse_args()  # This allows the calling function to access the provided arguments in a structured way.

def get_clients(clients_arg):


def update_symlink(link_path, target_path):


def perform_backup(client_ip, backup_type, ssh_user):


def main():


