import os
import re
import subprocess
import shutil
import time
import datetime
import glob

from env import *

def backup(server):
    world_path = os.path.join(BASE, server, 'world')
    if not os.path.exists(world_path):
        print('Error: Failed to find server world folder')
        print('{}: does not exist'.format(world_path))
        return

    if not os.path.isdir(world_path):
        print('Error: world path is not a directory')
        print('{}: is not a directory'.format(word_path))
        return

    backup_path = os.path.join(BACKUP_BASE, server)
    if not os.path.isdir(backup_path):
        os.makedirs(backup_path)

    datestr = datetime.date.today().isoformat()
    backup_dest = os.path.join(backup_path, 'world_{}'.format(datestr))

    shutil.copytree(world_path, backup_dest)


def clean(server, num_backups):
    backup_path = os.path.join(BACKUP_BASE, server)
    if not os.path.isdir(backup_path):
        os.makedirs(backup_path)

    backups = glob.glob('{}/world_*'.format(backup_path))
    
    backup_dates = []
    for backup in backups:
        match = re.search('world_(?P<year>\\d{4})-(?P<month>\\d{1,2})-(?P<day>\\d{1,2})$', backup)
        if not match:
            print('Failed to parse date out of backup: {}'.format(backup))
            pass
        backup_date = datetime.date(
            int(match.group('year')), 
            int(match.group('month')), 
            int(match.group('day'))
        )
        backup_dates.append(backup_date)
    
    backup_dates.sort(reverse=True)
    to_delete = backup_dates[num_backups:]
    
    for backup in to_delete:
        datestr = backup.isoformat()
        backup_path = os.path.join(BACKUP_BASE, server, 'world_{}'.format(datestr))
        shutil.rmtree(backup_path)


def status(server):
    """ Prints status of specified server """
    server = 'survival'
    service_status = subprocess.check_output(
        'service minecraft@{} status'.format(server).split(' ')
    ).decode('utf-8')
    
    match = re.search('Active: (?P<status>.*$)', service_status, re.M)
    if not match:
        print('No service found')
        return
    print(match.group('status'))

    match = re.search('(?P<pid>\\d{1,5})\\s/usr/bin/java', service_status, re.M)
    if not match:
        print('No PID found')
        return
    pid = match.group('pid')
    print('PID: {}'.format(pid))
   
    ps = subprocess.Popen(
        'top -p{} -b -n1'.format(pid).split(' '), 
        stdout=subprocess.PIPE
    )
    resources = subprocess.check_output(
        'tail -1'.split(' '),
        stdin=ps.stdout
    ).decode('utf-8')

    resource_list = resources.split()
    mem = resource_list[5]
    cpu_perc = resource_list[8]
    mem_perc = resource_list[9]
    print('RAM: {}'.format(mem))
    print('CPU%: {}%'.format(cpu_perc))
    print('MEM%: {}%'.format(mem_perc))


def list_servers(base_dir):
    """ Lists all minecraft servers found """
    dirs = os.listdir(base_dir)
    servers = []
    for d in dirs:
        if os.path.exists(os.path.join(base_dir,d,'minecraft_server.jar')):
            servers.append(d)
    return servers
