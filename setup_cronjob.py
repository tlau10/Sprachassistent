from crontab import CronTab
import os

# setups and shedules cronjob to receive latest mensa data
USER = os.getlogin()
COMMAND = "python _04_dialog_manager/mensa_parser/mensa_data_requester.py"

crontab_ = CronTab(user = USER)

print(f"setting up cron job for user {USER}...")

cron_job = crontab_.new(command = COMMAND)
cron_job.setall('0 6 * * 1')
crontab_.write()

print(f"cron job successfully set up for user {USER}")
