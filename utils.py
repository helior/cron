from datetime import datetime
import re
def trim(str):
  return str.strip()

def get_list(str):
  return list(map(trim, str.split(',')))

def filenametotimestamp(filename, truncate_ext=".tar.gz"):
  filename = filename.rstrip(truncate_ext)
  pattern = '^(\d{4})-(\d{2})-(\d{2})_(\d{2})-(\d{2})-(\d{2})$'
  # sample: 2022-03-18_14-20-02
  
  match = re.findall(pattern, filename)
  if not match:
    return
  
  year, month, day, hour, minute, second = match[0]
  dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
  return int(dt.timestamp())

def timestamptofilename(ts):
  # ex: 2022-03-18_14-20-02
  dt = datetime.fromtimestamp(ts)
  return dt.strftime('%Y-%m-%d_%H-%M-%S')
