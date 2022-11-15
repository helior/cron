import configparser
from datetime import datetime
import os
import shutil
import tarfile
import time
import utils

def run(period):
  now = int(time.time())
  print('')

  '''
  (1) Read Config
  '''
  conf = configparser.ConfigParser()
  config_path = os.path.expanduser('~/.helior-cron.ini')

  if not os.path.exists(config_path):
    print('❌ Config file "{}" does not exist. Goodbye 👋 '.format(config_path))
    exit()

  print('👀 {} backup using {}'.format(period.title(), config_path))
  conf.read(config_path)

  if not period in conf.sections():
    print('❌ The period "{}" is not found in your config file. Goodbye 👋 '.format(period))
    exit()

  try:
    threshold = conf.getint(period, 'threshold_seconds')
    files = utils.get_list(conf.get(period, 'files'))
    destination = conf.get(period, 'destination')
    retention_seconds = conf.getint(period, 'retention_seconds')
    last_updated = conf.getint(period, 'last_updated', fallback=0)
  except configparser.NoOptionError as e:
    print('❌ Oops! Missing configuration.')
    print(e)
    exit()


  '''
  (2) Garbage Collection
  '''
  all_archives = filter(None, map(utils.filenametotimestamp, os.listdir(destination)))
  archives_to_delete = filter(lambda x: x < now - retention_seconds, all_archives)

  for ts in archives_to_delete:
    filename = utils.timestamptofilename(ts)
    try:
      os.remove(os.path.join(destination, filename))
    except FileNotFoundError as e:
      print('❌ File not found:{}'.format(filename))
      print(e)
    print('🚫 Deleted {}'.format(filename))


  '''
  (3) Run Backup, if applicable.
  '''
  elapsed_time = now - last_updated
  threshold_difference = threshold - elapsed_time
  if threshold_difference > 0:
    print('❌ Threshold time for backup not met. {} seconds remaining.'.format(threshold_difference))
    exit()

  if not os.path.exists(destination):
    try:
      os.makedirs(destination) # assumes filesystem write access
    except PermissionError as e:
      print('❌ Oops! Cannot create destination directory.')
      print(e)
      exit()

  now_timestamp = int(datetime.now().timestamp())
  archive_name = utils.timestamptofilename(now_timestamp)

  tar = tarfile.open(archive_name, 'w:gz')
  for f in files:
    print("⤵️  Adding {}".format(f))
    try:
      tar.add(f, os.path.basename(f))
    except FileNotFoundError as e:
      print('❌ Oops! Skipping this file: {}'.format(os.path.basename(f)))
      print(e)
  tar.close()

  # TODO:check if destination will allow more archives
  # archive_size = os.path.getsize(archive_name)

  try:
    shutil.move(archive_name, destination)
  except (shutil.SameFileError, shutil.SpecialFileError, PermissionError) as e:
    print('❌ Oops! Error moving backup to destination.')
    print(e)
    exit()

  print('✅ Backup created in {}.'.format(os.path.join(destination, archive_name)))
  try:
    conf.set(period, 'last_updated', str(now_timestamp))
    with open(config_path, 'w') as c:
      conf.write(c)
  except TypeError as e:
    print('🤷 Ooops!! Unable to update config file. This may result in excessive backups! 😬')
    print(e)
