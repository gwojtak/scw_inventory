#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Generate an inventory of servers from scaleway which is
suitable for use as an ansible dynamic inventory

Right now, only the group 'cci-customer' is exported
'''

import argparse
import json
import configparser

from scaleway.apis import ComputeAPI

class SCWInventory(object):
    '''
    The inventory class which calls out to scaleway and digests
    the returned data, making it usable by ansible as an inventory
    '''
    def __init__(self):
        self.args = None
        self.inventory = None
        self.auth_token = None
        self.response = {
            '_meta': {
                'hostvars': {
                }
            }
        }

    def parse_config(self, creds_file='scw_credentials.ini'):
        '''
        Parse the ini file to get the auth token
        '''
        config = configparser.ConfigParser()
        config.read(creds_file)
        self.auth_token = config['credentials']['auth_token']

    def parse_arguments(self):
        '''
        Use argparse to interpret flags passed into the script
        '''
        parser = argparse.ArgumentParser(
            description='generate an ansible dnyamic inventory from scaleway api'
        )
        parser.add_argument(
            "--list",
            help="generate a json list of hosts and groups",
            action="store_true",
            default=True
        )
        self.args = parser.parse_args()

    def get_servers(self):
        '''
        query scaleway api and pull down a list of servers
        '''
        self.parse_config()
        api = ComputeAPI(auth_token=self.auth_token)
        result = api.query().servers.get()
        self.inventory = [
            [i['name'], i['public_ip'], i['tags']] for i in result['servers']
        ]
        for host, ip_info, tags in self.inventory:
            if ip_info:
                self.response['_meta']['hostvars'][host] = {
                    'ansible_host': ip_info['address']
                }
            if tags:
                for tag in tags:
                    if tag.startswith('group:'):
                        self._add_to_response(
                            tag.split(':')[1],
                            host
                        )

    def _add_to_response(self, group, hostname):
        '''
        add a host to a group within the response
        '''
        if group not in self.response:
            self.response[group] = list()
        if group in self.response:
            self.response[group].append(hostname)

    def print_inventory(self):
        '''
        simply display the collected inventory
        '''
        print(json.dumps(self.response))

def main():
    '''
    run the program starting here
    '''
    inventory = SCWInventory()
    inventory.get_servers()
    inventory.print_inventory()

if __name__ == '__main__':
    main()
