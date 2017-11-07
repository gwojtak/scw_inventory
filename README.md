# scw_inventory
> A dynamic inventory script for Scaleway instances in Ansible

This script uses the Scaleway API to generate a dynamic inventory that Ansible
understands.  This can be used to manage your instances.

## Getting started

Simply clone this repository and copy the scw_inventory.py script to a location
in your PATH.

```shell
$ git clone https://github.com/gwojtak/scw_inventory.git
$ cd scw_inventory
$ sudo cp scw_inventory.py scw_credentials.ini /usr/local/bin
```

This script requires python 3 and the scaleway SDK.  python 3 can be installed using
your Linux distribution's package manager.  Scaleway SDK can be installed via pip

```shell
$ sudo pip3 install scaleway-sdk
```

The script can be run from command line without ansible to test functionality.
```shell
$ scw_inventory.py --list
```

## Configuration

Edit /usr/local/bin/scw_inventory.ini in your favorite editor and set auth_token to you
Scaleway AUTH_TOKEN.

## Contributing

If you wish to contribute:
    * fork this repository
    * clone your fork
    * make your updates
    * commit and push
    * submit a pull request

## Licensing

The code in this project is licensed under MIT license.
