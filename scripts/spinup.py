#!/usr/bin/env python3

import json
import os
import time

import requests


class DigitalOcean:

    ''' personal access token file path hard coded'''

    def __init__(self):
        self.pat_filepath = "/tmp/do-pat.md"
        self.endpoint = 'https://api.digitalocean.com/v2/'

    def fetch_token(self):
        with open(self.pat_filepath, 'r') as tp:
            return tp.read().strip()

    def get_metadata(self):
        metadata = {'Content-Type': 'application/json',
                    'Authorization': 'Bearer {token}'.format(token=self.fetch_token())}
        return metadata

    def fetch_keys(self):
        endpoint = self.endpoint + 'account/keys'
        keys = json.loads(requests.get(endpoint, headers=self.get_metadata()).text)[
            'ssh_keys']
        return [str(key['id']) for key in keys if key['name'] == 'mac_workspace_test']

    def create_droplet(self, droplet_name):
        endpoint = self.endpoint + 'droplets'

        data = {'name': droplet_name,
                'region': 'nyc1',
                'size': 's-1vcpu-1gb',
                'image': 'ubuntu-18-04-x64',
                'ssh_keys': self.fetch_keys(),
                'tags': ['Byte']}

        response = json.loads(requests.post(
            endpoint, headers=self.get_metadata(), json=data).text)

        return response['droplet']['id']

    def create_droplets(self, droplet_names_list):
        endpoint = self.endpoint + 'droplets'

        data = {'names': droplet_names_list,
                'region': 'nyc1',
                'size': 's-1vcpu-1gb',
                'image': 'ubuntu-18-04-x64',
                'ssh_keys': self.fetch_keys(),
                'tags': ['Byte']}

        response = json.loads(requests.post(
            endpoint, headers=self.get_metadata(), json=data).text)

        ids = [res['id'] for res in response['droplets']]

        return ids

    def list_all_droplets(self):
        endpoint = self.endpoint + 'droplets?page=1&per_page=10'
        response = json.loads(requests.get(
            endpoint, headers=self.get_metadata()).text)['droplets']
        droplets = []
        for res in response:
            droplets.append([res['id'], res['name'], res['tags'],
                             res['networks']['v4'][0]['ip_address']])
        return droplets

    def drop_droplet(self, droplet_id):
        endpoint = self.endpoint + \
            'droplets/{droplet_id}'.format(droplet_id=droplet_id)
        try:
            return requests.delete(endpoint, headers=self.get_metadata())
        except:
            return "Error destroying droplet: {droplet_id}".format(
                droplet_id=droplet_id)

    def get_ip_address(self, droplet_id):
        endpoint = self.endpoint + \
            'droplets/{droplet_id}'.format(droplet_id=droplet_id)
        response = json.loads(requests.get(
            endpoint, headers=self.get_metadata()).text)
        return response['droplet']['networks']['v4'][0]['ip_address']

    def install_dependencies(self, ip_address):
        os.system(
            'ssh -o \'StrictHostKeyChecking no\' root@{ip_address} \'bash -s\' < install.sh'.format(ip_address=ip_address))
        return "dependencies were installed for new operating system at {ip_address}".format(ip_address=ip_address)

    def send_commands(self, ip_address):
        # TODO Send arbitrary bash commands to the remote server to be executed
        os.system(
            'ssh -o \'StrictHostKeyChecking no\' root@{ip_address} \'bash -s\' < install.sh'.format(ip_address=ip_address))

        return "Dependencies installed for new operating system at: {ip_address}".format(ip_address=ip_address)
