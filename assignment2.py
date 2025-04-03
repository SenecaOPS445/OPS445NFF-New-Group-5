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


def main():


