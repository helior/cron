''''
(1) Read user config
if nothing, do nothing.

(2) Guard running backup
Check if past threshold
Archive selected files
Move to destination

(3) Garbage collection

??? Log
??? Notifications
??? Install instructions
'''

import configparser
from datetime import datetime
import os
import shutil
import tarfile
import time
from utils import get_list, filenametotimestamp, timestamptofilename

PERIOD = 'daily'


'''
(1) Read Config
'''
conf = configparser.ConfigParser()
config_path = os.path.expanduser('~/.helior-cron.ini')

if not os.path.exists(config_path):
  print('❌ Config file "{}" does not exist. Goodbye 👋 '.format(config_path))
  exit()

print('Config file: {}'.format(config_path))
conf.read(config_path)



'''
(2) Run Backup, if applicable.
'''
if not PERIOD in conf.sections():
  print('❌ The period "{}" is not found in your config file. Goodbye 👋 '.format(PERIOD))
  exit()

try:
  threshold = conf.getint(PERIOD, 'threshold_seconds')
  last_updated = conf.getint(PERIOD, 'last_updated')
except configparser.NoOptionError as e:
  print('❌ Oops! Missing configuration.')
  print(e)
  exit()

elapsed_time = int(time.time() - last_updated)
threshold_difference = threshold - elapsed_time
if threshold_difference > 0:
  print('❌ Threshold time for backup not met. {} seconds remaining.'.format(threshold_difference))
  exit()

try:
  files = get_list(conf.get(PERIOD, 'files'))
  destination = conf.get(PERIOD, 'destination')
except configparser.NoOptionError as e:
  print('❌ Oops! Missing configuration.')
  print(e)
  exit()

if not os.path.exists(destination):
  try:
    os.makedirs(destination) # assumes filesystem write access
  except PermissionError as e:
    print('❌ Oops! Cannot create destination directory.')
    print(e)
    exit()

now_timestamp = int(datetime.now().timestamp())
filename = timestamptofilename(now_timestamp)
archive_name = filename + '.tar.gz'

tar = tarfile.open(archive_name, 'w:gz')
for f in files:
  print("✔ Adding %s" % f)
  try:
    tar.add(f, os.path.basename(f))
  except FileNotFoundError as e:
    print('❌ Oops! Skipping this file: {}'.format(os.path.basename(f)))
    print(e)
tar.close()

archive_size = os.path.getsize(archive_name)
# TODO:check if destination will allow more archives

try:
  shutil.move(archive_name, destination)
except (shutil.SameFileError, shutil.SpecialFileError, PermissionError) as e:
  print('❌ Oops! Error moving backup to destination.')
  print(e)
  exit()

print('✅ Successful backup of {}.'.format(archive_name))
try:
  conf.set(PERIOD, 'last_updated', str(now_timestamp))
  with open(config_path, 'w') as c:
    conf.write(c)
except TypeError as e:
  print('❌ Ooops!! Unable to update config file. This may result in excessive backups! 😬')
  print(e)



'''
(3) Garbage Collection
'''
