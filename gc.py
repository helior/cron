import os
import time
import utils

now = int(time.time())
destination = '/Users/heliorcolorado/My Drive/backups'
retention_seconds = 60*60*24*7 # 7 days

files = list(filter(None, map(utils.filenametotimestamp, os.listdir(destination))))
files.sort()

print(files)
print(len(files))
