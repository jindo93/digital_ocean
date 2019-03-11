#!/usr/bin/env python3

from .spinup import DigitalOcean

if __name__ == '__main__':
    do = DigitalOcean()
    print(do.list_all_droplets())
