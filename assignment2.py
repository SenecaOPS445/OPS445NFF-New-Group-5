def get_clients(clients_arg):
    if clients_arg.lower() == 'all':
        return CLIENT_IPS
    return [ip.strip() for ip in
clients_arg.split(',')]
