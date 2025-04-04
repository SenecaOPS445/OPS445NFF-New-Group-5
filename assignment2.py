def get_clients(clients_arg): 
    if clients_arg.lower() == 'all':  # If the user types "all" it returns the full list of IP addresses.
        return CLIENT_IPS # Return all client IP addresses stored in the CLIENT_IPS list.
    return [ip.strip() for ip in clients_arg.split(',')] # this splits the addresses into individual IPs, removes any spaces, and returns them as a list.
