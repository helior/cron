## Cron

This utility contains a script that will backup a list of `files` to a specified `destination`. Given a `retention` value, it will automatically delete files from the destination. Given a `threshold` value, the script will limit the frequency of backups, so it can be safely ran multiple times.

### Install
1. Create a `.helior-cron.ini` file in your home directory. See the provided `.helior-cron.ini.example`
2. Edit the crontab `crontab -e`
3. Add an entry to run script:
`*/15 * * * * /path/to/python /path/to/cron/daily.py >> /path/to/some/log/file.log 2>&1`

### Protip
- Cron jobs will only execute so long the computer is running. I recommend running the cron frequently since the script will ensure that only one backup is created per configured `threshold` value.
- `files` are comma-separated in the `~/.helior-cron.ini`

## TODO:
- change name of project and config file
- allow external destinations like S3
- allow for infinite retention
- fix: reconcile when files to be backed up have the same filename
