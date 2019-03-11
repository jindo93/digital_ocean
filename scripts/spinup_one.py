#!/usr/bin/env python3

from .spinup import DigitalOcean

if __name__ == '__main__':
    do = DigitalOcean()
    droplet_id = do.create_droplet('droplet-1')
    droplet_ip = do.get_ip_address(droplet_id)
    print(do.install_dependencies(droplet_ip))
