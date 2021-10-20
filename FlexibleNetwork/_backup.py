from ._cli import Argument_Parser
arg_parser = Argument_Parser()
arg_parser.argparse()

import os
import re
from datetime import datetime
import json


class Backup:
    def __init__(self):
        task_name = arg_parser.task_name
        task_name = re.sub("\s", '-', task_name)
        date = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
        self.date_only = datetime.today().strftime('%d-%m-%Y')
        self.time_only = datetime.today().strftime('%H:%M:%S')


        self.date_d_m_y = datetime.today().strftime('%d-%m-%Y')
        self.backup_directory = '.Backup'
        self.backup_state_file = '.Backup-State.json'
        self.state = {}
        self.task_name = task_name + "__" + date
        self.task_dir  = self.backup_directory + '/' + self.task_name

    def create_task_directory(self):

        # Create Backup dir
        if not os.path.exists(self.backup_directory):
            os.makedirs(self.backup_directory)

        # Create task dir
        if not os.path.exists(self.backup_directory + '/' + self.task_name):
            os.makedirs(self.backup_directory + '/' + self.task_name)

    def build_state_info(self):
        # Store the Backup state in Json file
        self.state = {}
        self.state[self.task_name]  = {}
        self.state[self.task_name]['date']      = self.date_only
        self.state[self.task_name]['time']      = self.time_only
        self.state[self.task_name]['task_name'] = arg_parser.task_name
        self.state[self.task_name]['comment']   = arg_parser.task_comment
        self.state[self.task_name]['Backups']   = {}


    def save_state_to_json(self):
        try:
            if os.path.exists(self.backup_state_file):
                json_data = None
                with open(self.backup_state_file, 'r') as f:
                    json_data =  json.load(f)
                    if json_data is not None:
                        if self.task_name not in json_data.keys():
                            # Add new task
                            json_data[self.task_name] = {}
                            json_data[self.task_name] = self.state[self.task_name]
                            # write changes
                            with open(self.backup_state_file, 'w') as jsonFile:
                                json.dump(json_data, jsonFile, sort_keys=True, indent=4)
            else:
                with open(self.backup_state_file, 'w') as f:
                    json.dump(self.state, f, sort_keys=True, indent=4)
        except json.decoder.JSONDecodeError:
            print("[ ERROR ] Could NOT read Json from :" + self.backup_state_file)
            exit(1)





    def save_backup_to_file(self, file, data):
        with open(file, 'w') as backup_file:
            backup_file.write(data)
