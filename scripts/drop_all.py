#!/usr/bin/env python3

from .spinup import DigitalOcean

if __name__ == '__main__':
    do = DigitalOcean()
    droplets = do.list_all_droplets()
    for droplet in droplets:
        droplet_id = droplet[0]
        do.drop_droplet(droplet_id)
