## Cron


### Install
1. Create a crontab `crontab -e`
2. Run every minute `*/1 * * * * python $HOME/cron/cron.py >> $HOME/cron/cron.log 2>&1`