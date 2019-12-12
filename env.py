""" Environment variables for server commands """
import os
NUM_BACKUPS = os.getenv('MC_ENV_NUM_BACKUPS', 10)
BACKUP_BASE = os.getenv('MC_ENV_BACKUP_BASE', '/opt/minecraft/backups')
BASE = os.getenv('MC_ENV_BASE', '/opt/minecraft')
