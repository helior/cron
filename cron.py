from datetime import datetime
import os
import tarfile
import shutil

now = datetime.now()
now_iso8601 = now.strftime('%Y-%m-%dT%H:%M:%S+00:00')
print(now_iso8601)
'''
TODO: When this code is done, it will literally only post data to a webhook to
kick-off a server-side event. All downstream operations will be managed there.
'''

'''
Evaluate whether portion of script should execute, per cadence rules (like 5 times a day, once a week, etc.)
🤔 Collect Global context from free external web APIs
🤔Invoke Event to feed into Rules-based engine
Backups app

(🚀) Ultimate Weapon Rules-based Engine - Cron event executor

(🚀) Backup System

(🚀) Auto-garbage collect huge log files
(1) Read configuration file
- which directory to backup
- what location to save backup
- what cadence?
(2) (compress, then) Copy files
(3) Log outcome
'''

'''
Ideas:
- Move to folders that I can use as inboxes, so that the next manual step is obvious — like move these files to external hard drive
- Automate the logic for moving files through ALL phases
- Allow backups to be blocked until files are moved ⬇
- Each layer of backups have their own configuration for maximum allotted size to allow/prevent backups from even starting.
- Model "Backup Destination" objects:
  - isAvailable() per max threshold limits
  - currentSize() per saved metadata
  - isDisabled() per saved metadata
  - count() per introspection via saved metadata
  - requestBackup() internally checks isAvailable() and isDisabled()
  - removeNthItems() first, last, until size range (oldest 8GB), or count range (earliest 12)
- Each backup instance is a directory with a metadata file (class initiator), all interaction is handled by backups

==============================
Implementation notes:

* Metadata is an optimization; first get data on-demand *

On Cron, invoke Invoker, which references Sender 1.
Sender 1 references Backup Destination 1 (by path)
Read backup destination 1 metadata, create metadata defaults if not found, but file referenced is found.
★ Config is ini file for each file referenced (directory for Destination, or files/directory for Senders)
- determine last backup time, allow backup if surpasses threshold
Invoker determines that a backup must be ran

Invoke Sender 1, which references backup destination 1:
Sender requests if backup destination is available, otherwise, backups are blocked; send notification.
Sender compresses all files into year-month-day-hour-minute-backup-name.tar.gz
Sender copies all files into destination prefix path
Backup Destination returns success event
On success, Sender logs event (into webhook)
On Fail, Sender logs event (into webhook)

Backup Destination metadata for





==============================


🦋 Backup Phases:
- Copy to destination 1 (personal cloud drive)
  Every week, up to maximum of [12] copies (about 3 months worth)
  After which, notify me to manually move to hard drive ⬇ and reasonably purge cloud drive

- Copy to destination 2 (external hard drive)
  Every 3 months, up to maximum of [52] copies (about a years worth)
  After which, notify me to burn to CD ⬇ and reasonably purge hard drive

- Copy to destination 3 (burn CD)
  Every 6 - 12 months, no maximum. Hold in CD wallet
  Bury in time capsule


🦋 Restore strategy:
- Revert to latest healthy backup
- Try to replay insertions (via logs, original media — this will be a manual process)
'''

class BackupDestination:
  def init(self, file_path):
    self.filepath = file_path

  def isAvailable(proposed_file_size):
    '''
    Checks condition of destination to ensure it can save the proposed number of bytes to disk.
    '''
    return True


number_of_backups = 12


# TODO: Config
backup_cadence = 604800 # 7 days in seconds
backup_targets=[
  '/Users/helior/Code/helior/memento/cms/db.sqlite3',
  '/Users/helior/Code/helior/memento/cms/media'
]

backup_destination_1 = '/Users/helior/My Drive/backups'

bd = BackupDestination(backup_destination_1)

# Sanity checks
if not os.path.exists(backup_destination_1):
  os.makedirs(backup_destination_1)

# Create gzip backup of targetted files
tmp_archive_name = 'tmp-backup' + now_iso8601
tar = tarfile.open(tmp_archive_name, 'w:gz')
for file_name in backup_targets:
  # TODO: Actually, don't pollute the log space
  print('Adding %s...' % file_name)
  tar.add(file_name, os.path.basename(file_name))
tar.close()

# Read file size
backup_file_size = os.path.getsize(tmp_archive_name)

# Check if backup can support incoming payload
# Backup compares max hard-limit, max allowance, return if available
if not bd.isAvailable(backup_file_size):
  # send notification that backups are blocked.
  print('Backup destination is not available. Backup is cancelled.')


# copy command executes (formally)
# log last updated time so cron job can evaluate later.
)
