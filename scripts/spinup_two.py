#!/usr/bin/env python3

from .spinup import DigitalOcean

if __name__ == '__main__':
    do = DigitalOcean()
    droplet_ids = do.create_droplets(['droplet-1', 'droplet-2'])
    for droplet_id in droplet_ids:
        ip = do.get_ip_address(droplet_id)
        print(do.install_dependencies(ip))
