from datetime import datetime
import re

def trim(string):
  return string.strip()


def get_list(string):
  return list(map(trim, string.split(',')))


def filenametotimestamp(filename):
  ext = '.tar.gz'
  filename = filename.rstrip(ext)
  pattern = '^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})$'
  # sample: 2022-03-18_14-20-02

  match = re.findall(pattern, filename)

  if not match:
    return

  year, month, day, hour, minute, second = match[0]
  dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
  return int(dt.timestamp())


def timestamptofilename(ts):
  ext = '.tar.gz'
  dt = datetime.fromtimestamp(ts)
  filename = dt.strftime('%Y-%m-%d_%H-%M-%S')
  # ex: 2022-03-18_14-20-02
  return filename + ext
