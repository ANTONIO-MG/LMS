"""
the cron  job will run this script every 15 minutes
allowing me t automatically make backups of the database
"""

from django.core.management import call_command


def my_backup():
    try:
        print("Started backup process")
        call_command('dbbackup')
        print("Backup Completed")
    except:
        pass
    