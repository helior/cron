from datetime import datetime

def trim(str):
  return str.strip()

def get_list(str):
  return list(map(trim, str.split(',')))

def filenametotimestamp(str):
  # ex: 2022-03-18_14-20-02
  date, time = str.split('_')
  year, month, day = date.split('-')
  hour, minute, second = time.split('-')
  dt = datetime(int(year), int(month), int(day), int(hour), int(minute), int(second))
  return int(dt.timestamp())

def timestamptofilename(ts):
  # ex: 2022-03-18_14-20-02
  dt = datetime.fromtimestamp(ts)
  return dt.strftime('%Y-%m-%d_%H-%M-%S')
