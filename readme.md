## Cron


### Install
1. Create the log file of your choosing (`cron.log` in my example)
2. Edit the crontab `crontab -e`
3. Add an entry to run script:
`*/15 * * * * /path/to/python /path/to/cron/cron.py >> /path/to/cron/cron.log 2>&1`
