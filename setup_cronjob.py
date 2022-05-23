from crontab import CronTab

# setups and shedules cronjob to receive latest mensa data
USER = "pi"
COMMAND = "python _04_dialog_manager/mensa_parser/mensa_data_requester.py"

crontab_ = CronTab(user = USER)

print(f"setting up cron job for user {USER}...")

cron_job = crontab_.new(command = COMMAND)
cron_job.setall('0 0 * * 0')
crontab_.write()

print("cron job successfully set up")
