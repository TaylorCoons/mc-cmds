#!/usr/bin/python3
import argparse

import cmds
from env import *

def backup(args):
    if args.server.lower() == 'all':
        servers = cmds.list_servers(BASE)
        for server in servers:
            cmds.backup(server)
    else:
        cmds.backup(args.server)

def clean(args):
    if args.server.lower() == 'all':
        servers = cmds.list_servers(BASE)
        for server in servers:
            cmds.clean(server, args.n)
    else:
        cmds.clean(args.server, args.n)

def env(args):
    print('MC_ENV_NUM_BACKUPS: Number of backups to keep on clean operation')
    print('MC_ENV_BACKUP_BASE: The base folder where backup worlds are stored')
    print('MC_ENV_BASE: The base folder for the servers')


def status(args):
    if args.server.lower() == 'all':
        servers = cmds.list_servers(BASE)
        for server in servers:
            print('Server: {}'.format(server))
            cmds.status(server)
    else:
        cmds.status(args.server)


def list_servers(args):
    servers = cmds.list_servers(args.dir)
    print('Servers found: {}'.format(', '.join(servers)))
   

def main():
    servers = cmds.list_servers(BASE)
    servers.insert(0, 'all')

    parser = argparse.ArgumentParser(description='Minecraft server tools')
    
    subparsers = parser.add_subparsers()
    
    backup_parser = subparsers.add_parser(
        'backup',
        help='Backup specified minecraft server world'
    )

    backup_parser.add_argument(
        'server', 
        help='Server world to back up',
        choices=servers
    )

    backup_parser.set_defaults(func=backup)
    
    clean_parser = subparsers.add_parser(
        'clean',
        help='Clean backups folder'
    )

    clean_parser.add_argument(
        'server',
        help='Server backups to clean',
        choices=servers
    )

    clean_parser.add_argument(
        '-n',
        '--n',
        default=NUM_BACKUPS,
        type=int,
        help='Number of backups to keep, if not specified the environment default is used'
    )

    clean_parser.set_defaults(func=clean)

    env_parser = subparsers.add_parser(
        'env',
        help='Lists environment variables and descriptions'
    )

    env_parser.set_defaults(func=env)

    status_parser = subparsers.add_parser(
        'status',
        help='Lists status of minecraft server'
    )

    status_parser.add_argument(
        'server',
        help='Server to get status',
        choices=servers
    )
    
    status_parser.set_defaults(func=status)

    list_parser = subparsers.add_parser(
        'list',
        help='Lists all servers found'
    )

    list_parser.add_argument(
        '-d',
        '--dir',
        help='Base directory of minecraft servers',
        default=BASE
    )

    list_parser.set_defaults(func=list_servers)

    args = parser.parse_args()
    args.func(args)
    




if __name__ == '__main__':
   main()
