import json
import os
from tabulate import tabulate

from ._cli import Argument_Parser
arg_parser = Argument_Parser()
arg_parser.argparse()

from ._colors import Bcolors
bcolors = Bcolors()

from ._backup import Backup
backup = Backup()
backup.build_state_info()

class List_Backups:
    def __init__(self):
        self.tasks_table = [['ID','Task', 'Comment', 'Date', 'Time', 'Backups']]
        self.backups_table = [['Host' ,'Comment', 'Backup Location']]

    def list_tasks_table(self):
        if not os.path.isfile(backup.backup_state_file):
            print(bcolors.FAIL + "> Backup state file does NOT exist" + bcolors.ENDC)
            if os.path.isdir(backup.backup_directory):
                print(">> Can NOT list backups")
                print(">> Backup directory exists @ ({})".format(backup.backup_directory))
            exit(1)
        # Load the json state file
        with open(backup.backup_state_file, 'r') as f:
            json_data = json.load(f)

            tasks_list = json_data.keys()
            if arg_parser.filter_date:
                tasks_list = []
                for task in json_data.keys():
                    date = json_data[task]['date']
                    if date == arg_parser.filter_date:
                        tasks_list.append(task)
                if len(tasks_list) == 0:
                    print(bcolors.FAIL + '> No data found for the given date' + bcolors.ENDC)
                    print('>> Make sure you entered a valid date')

            for task in tasks_list:
                task_name = json_data[task]['task_name']
                task_comment = json_data[task]['comment']
                date = json_data[task]['date']
                time = json_data[task]['time']
                id = task
                row = [id, task_name, task_comment, date, time, ]
                self.tasks_table.append(row)
        print(tabulate(self.tasks_table, headers='firstrow', tablefmt='grid'))


    def show_backups_table(self, id=arg_parser.show_backups):
        with open(backup.backup_state_file, 'r') as f:
            json_data = json.load(f)

            # Check input
            if id not in list(json_data.keys()):
                print(bcolors.FAIL +  "> the ID you entered does NOT exist " + bcolors.ENDC)
                print()
                exit(1)

            backups = json_data[id]['Backups']

            for key, value in backups.items():
                # print(bcolors.WARNING + '> ' + key + bcolors.ENDC)
                for b in value:
                    comment = b['comment']
                    backup_location  = b['backup']
                    date = b['date']
                    row = [bcolors.WARNING + key + bcolors.ENDC, comment, backup_location]
                    self.backups_table.append(row)
        print(tabulate(self.backups_table, headers='firstrow', tablefmt='grid'))

