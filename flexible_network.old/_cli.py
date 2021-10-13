import sys
import os
import argparse

from ._colors import Bcolors
bcolors = Bcolors()

class Argument_Parser:
    def __init__(self):
        self.hosts_file   = None
        self.task_name    = None
        self.task_comment = False
        self.list_backups = None
        self.show_backups = None
        self.filter_date  = None

    def argparse(self):
        parser = argparse.ArgumentParser(description='A Python script to automate network devices with ease.')
        parser.add_argument('-f', '--hosts_file', type=str, required=False, metavar='', help='The hosts file')
        parser.add_argument('-t', '--task', type=str, required=False, default='task', metavar='', help='The task name')
        parser.add_argument('-m', '--comment', type=str, required=False, metavar='', help='The task Comment')
        parser.add_argument('-L', '--list', action='store_true', help='List tasks with Backups')
        parser.add_argument('-F', '--filter_date', type=str, required=False, metavar='', help='List only tasks in a specific date')
        parser.add_argument('-s', '--show', type=str, required=False, metavar='', help='Show backups of a task using task ID')

        results = parser.parse_args()
        self.hosts_file = results.hosts_file
        self.task_name = results.task
        self.task_comment = results.comment
        self.list_backups = results.list
        self.show_backups = results.show
        if results.list:
            self.filter_date = results.filter_date

        if (self.hosts_file is None) and (self.show_backups is None) and (self.list_backups is None):
            print("[ Error ] " + bcolors.FAIL + "--hosts_file option must be specified" + bcolors.ENDC)
            print('')
            parser.print_help(sys.stderr)
            exit(1)

        if (self.task_name is None) and (self.show_backups is None) and (self.list_backups is None):
            print("[ Error ] " + bcolors.FAIL + "--task option must be specified" + bcolors.ENDC)
            print('')
            parser.print_help(sys.stderr)
            exit(1)

        if self.hosts_file is not None:
            if not os.path.isfile(self.hosts_file):
                print("[ Error ] " + bcolors.FAIL + "({}) is NOT a File".format(self.hosts_file) + bcolors.ENDC)
                print('')
                parser.print_help(sys.stderr)
                exit(1)


        if len(sys.argv) < 2:
            parser.print_help(sys.stderr)
            exit(1)

