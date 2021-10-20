import time
from datetime import datetime
import os
from pygments import highlight, lexers, formatters
import re
import json
import atexit

from ._ssh_auth import SSH_Auth
ssh_auth = SSH_Auth()

from ._colors import Bcolors
bcolors = Bcolors()

from ._backup import Backup
backup = Backup()
backup.build_state_info()

from .vendors._cisco import Cisco
from .vendors._huawei import Huawei
cisco = Cisco()
huawei = Huawei()




class SSH_Connection:
    """
    Class to Connect & execute commands to hosts/devices via ssh
    """

    def __init__(self, host, user, password, port=22, ssh_timeout=10, allow_agent=True, vendor='Cisco'):
        self.info = {}
        self.hosts = None
        self.host = host
        self.user = user
        self.password = password
        self.port = port
        self.ssh_timeout = ssh_timeout
        self.is_connected = False
        self.channel = None
        self.vendor = vendor
        self.backup_command = None
        self.stderr_search_keyword = None
        self.clean_output_search_keyword = None

        # INfo
        supported_vendors = ['Cisco', 'Huawei']

        # Check for vendor
        if self.vendor not in supported_vendors:
            print("[ ERROR ] Unsupported Vendor: {}".format(vendor))
            print("Supported vendors :" + str(supported_vendors))
            exit(1)

        # Check for error_search_keyword
        if self.vendor == 'Cisco':
            self.stderr_search_keyword = cisco.stderr_search_keyword
        elif self.vendor == 'Huawei':
            self.stderr_search_keyword = huawei.stderr_search_keyword

        ssh_auth.auth(self.host,self.user,self.password,self.port,self.ssh_timeout, allow_agent)
        self.is_connected = ssh_auth.is_connected
        self.channel      = ssh_auth.channel


    def get_stderr(self, string):
        """
        function to search for keywords inside of text and to get several lines of the matched keywords
        so that it can be represented as STDERR
        :param string: string text to search for an error keyword
        :param search: Regex search in the text provided in "String" Parameter'
        :return: dict consists of 2 keys {list: list of matched lines (can contain empty lines), string: matched lines as a string}
        """
        n = 0
        string_list_with_number = {}
        found_with_number = {}
        string_list = string.split("\n")  # split the text into lines separated by "new line"
        for line in string_list:  # create a dict "string_list_with_number" which consists of line number & text of each line
            n += 1
            string_list_with_number[n] = line
            found = re.findall("{}.*$".format(self.stderr_search_keyword), line)  # searches the keyword inside the lines
            found_with_number[n] = found  # dict "found_with_number" consists of line number & matched lines; lines that does
            # not match the search will be empty arr like: {1: [], 2: [], 3: ['% bla bla], 4: []}

        err_lines = []
        for key, value in found_with_number.items():  # iterate over matched lines in the dict "found_with_number"
            if value:
                err_lines.append(key)  # save the line number of the matched lines in "err_lines" list

        result = []
        lines_to_print = []
        for num in err_lines:
            num -= 1  # get a previous line (to get the command line)
            for i in range(6):  # get 6 lines after the error detected line
                lines_to_print.append(
                    num + i)  # append the result to "lines_to_print" dict (which contains needed line numbers)
        try:
            for i in list(set(lines_to_print)):  # list(set(lines_to_print)) --> to get rid of duplicates
                result.append(string_list_with_number[i])  # save the matched lines (strings) to "result" list

        except KeyError:
            return
        finally:
            dict = {'list': result, 'string': '\n'.join(result)}
            return dict

    def print(self, msg, level='info', force=False):
        """
        Method to Print with different print Levels ('info', 'warn', 'fail')
        :param force: by default it NOT print if the failed to connect to the host, use this option to print anyway
        :param level: info (green color), warn(yellow color), fail(red color)
        :param msg: The message to be printed
        :return:
        """
        color = None
        start = None
        if level == 'info':
            color = bcolors.OKGREEN
            start = bcolors.BOLD + bcolors.OKGREEN + "-- INFO --" + bcolors.ENDC + bcolors.ENDC
        elif level == 'warn':
            color = bcolors.WARNING
            start = bcolors.BOLD + bcolors.WARNING + "-- WARNING --" + bcolors.ENDC + bcolors.ENDC
        elif level == 'alert':
            color = bcolors.FAIL
            start = bcolors.BOLD + bcolors.FAIL + "-- ALERT --" + bcolors.ENDC + bcolors.ENDC
        else:
            print(
                bcolors.FAIL + " Supported print level options are: ['info', 'warn', 'alert'] - Your input: ({})".format(
                    level) + bcolors.ENDC)
            exit(1)
        if not force:
            if self.is_connected:
                print(start + color + ' ' + msg + bcolors.ENDC)
        else:
            print(start + color + ' ' + msg + bcolors.ENDC)

        ### To be removed later ### (This project is focused on Network Automation)
    # def exec_cmd(self, cmd):
    #     """
    #     Run a command on a remote host via ssh (Suitable for Servers)
    #     :param cmd: Command to run on a remote host
    #     :return: dict
    #     """
    #     if self.is_connected:
    #         stdin, stdout, stderr = self.ssh.exec_command(cmd)
    #         self.info['connected'] = self.is_connected
    #         self.info['cmd'] = cmd
    #         self.info['stdout'] = stdout.read().decode("utf-8")
    #         self.info['stderr'] = stderr.read().decode("utf-8")
    #         self.info['exit_code'] = stdout.channel.recv_exit_status()
    #         return self.info
    #     elif not self.is_connected:
    #         self.info['cmd'] = cmd
    #         self.info['connected'] = self.is_connected
    #         self.info['stdout'] = ''
    #         self.info['stderr'] = ("Failed to connect to %s" % self.host)
    #         self.info['exit_code'] = ''
    #         return self.info


    def execute(self, cmd=None, cmd_from_file=None, print_stdout=False, exit_on_fail=True,
              print_json=False, search=None, ask_for_confirmation=False):
        """
        Method to execute execute commands through SSH execute channel, similar to attaching to a execute session
        :param cmd_from_file: to run commands from a text file
        :param exit_on_fail: fail if STDERR is found
        :param print_json: Whether to print JSON to output
        :param cmd: command to be run, make sure the the command ends with a new line, i.e "sh vlan br\n"
        :param print_stdout: to print cmd stdout in terminal with (Blue color)
        :param search: Option to Search the command stdout with Regexp
        :return: dictionary
        """

        if self.is_connected:

            if (cmd_from_file is not None) and (cmd is not None):
                print("[ Error ] " + bcolors.FAIL + "You can only use 'cmd' or 'cmd_from_file' options" + bcolors.ENDC)
                exit(1)

            if cmd_from_file is not None:
                if os.path.exists(cmd_from_file):
                    f = open(cmd_from_file, 'r')
                    cmd = f.read()
                elif not os.path.isfile(cmd_from_file):
                    print(
                        "[ Error ] " + bcolors.FAIL + "You've specified 'cmd_from_file option' but ({}) is NOT a file".format(
                            cmd_from_file) + bcolors.ENDC)
                    exit(1)

            if ask_for_confirmation:
                options = ['yes', 'no', 'skip']
                decision = None
                while decision not in options:
                    confirm = input(
                        "\n[ WARNING ] " + bcolors.WARNING + "Confirm before running the following command: \n" + bcolors.ENDC
                        + "\n"
                        + bcolors.OKBLUE + cmd + bcolors.ENDC + "\n"
                        + "\nyes || no \n\n"
                        + "yes: Run & continue\n"
                        + "no:  Abort\n"
                        + "YOUR Decision: ")
                    if confirm == 'yes':
                        print(bcolors.OKGREEN + "> Ok .. Let\'s continue ...\n" + bcolors.ENDC)
                        break
                    elif confirm == 'no':
                        print(bcolors.FAIL + "> See you \n" + bcolors.ENDC)
                        exit(1)

            self.channel.send(cmd + '\n' + '\n')
            # Important to set wait time, if not set it might not be able to read full output.
            time.sleep(0.5)
            self.info['cmd'] = cmd.replace("\r", '').split("\n")
            cmd_original = self.info['cmd']
            self.info['connected'] = self.is_connected
            self.info['stdout'] = self.channel.recv(9999).decode("utf-8")
            stdout_original = self.info['stdout']
            self.info['stdout'] = self.info['stdout'].replace(cmd, '')

            if self.vendor == 'Cisco':
                self.clean_output_search_keyword = cisco.clean_output_search_keyword
            if self.clean_output_search_keyword is not None:
                self.info['stdout'] = re.sub(self.clean_output_search_keyword, '', self.info['stdout'])
            self.info['stdout'] = self.info['stdout'].strip()
            self.info['stderr'] = self.get_stderr(stdout_original)['string'].replace("\r", '').split(
                "\n")
            self.info['search'] = search
            self.info['search_found?'] = None
            self.info['search_match'] = None
            stderr_ = [x for x in self.info['stderr'] if x]
            if len(stderr_) > 0:
                self.info['exit_code'] = 1
            else:
                self.info['stderr'] = []
                self.info['exit_code'] = 0
            if search:
                found = re.findall(search, self.info['stdout'])
                if len(found) > 0:
                    self.info['search_match'] = found
                    self.info['search_found?'] = True
                else:
                    self.info['search_found?'] = False

            if print_json:
                self.info['stdout'] = self.info['stdout'].replace("\r", '')
                self.info['stdout'] = self.info['stdout'].split("\n")
                self.info['stdout'] = [x for x in self.info['stdout'] if x]
                # Get rid of old spaces
                self.info['cmd'] = [x for x in self.info['cmd'] if x]
                formatted_json = json.dumps(self.info, indent=4, sort_keys=True, ensure_ascii=False)
                colorful_json = highlight(formatted_json.encode('utf8'), lexers.JsonLexer(),
                                          formatters.TerminalFormatter())
                print(colorful_json)
                self.info['stdout'] = stdout_original
                self.info['cmd'] = cmd_original
            else:
                self.info['stdout'] = stdout_original

            if print_stdout:
                print(bcolors.OKBLUE + stdout_original + bcolors.ENDC)
            if exit_on_fail:
                if self.info['exit_code'] > 0:
                    print("")
                    print(bcolors.FAIL + "* * * * * * * * * * * * * * * * * * * * * * *" + bcolors.ENDC)
                    print("[ ERROR ] " + bcolors.FAIL + "Found the following Error:" + bcolors.ENDC)
                    print('')
                    err = self.get_stderr(stdout_original)['string']
                    # for c in self.info['cmd']:
                    #    print(bcolors.OKBLUE + c + bcolors.ENDC)
                    print('')
                    print(bcolors.FAIL + err + bcolors.ENDC)
                    print(bcolors.FAIL + "* * * * * * * * * * * * * * * * * * * * * * *" + bcolors.ENDC)
                    print("")
                    exit(1)
            return self.info

        elif not self.is_connected:
            self.info['cmd'] = cmd
            self.info['connected'] = self.is_connected
            self.info['stdout'] = ''
            self.info['stderr'] = ("Failed to connect to %s" % self.host)
            self.info['search_found?'] = None
            self.info['search_match'] = None
            self.info['exit_code'] = None
            return self.info

    def execute_from_file(self, file, print_stdout=False, exit_on_fail=True,
              print_json=False, search=None, ask_for_confirmation=False):

        # Check if the file exists
        if not os.path.exists(file):
            print("[ Error ] " + bcolors.FAIL + "({}) file does NOT exist".format(file) + bcolors.ENDC)
            exit(1)

        if not os.path.isfile(file):
            print("[ Error ] " + bcolors.FAIL + "({}) is NOT a file".format(file) + bcolors.ENDC)
            exit(1)

        # read the file to array
        with open(file, 'r') as f:
            cmd_from_file = f.read()
            lines = cmd_from_file.split("\n")
            lines = [x for x in lines if x]

        if ask_for_confirmation:
            options = ['yes', 'no']
            decision = None
            while decision not in options:
                confirm = input(
                    "\n[ WARNING ] " + bcolors.WARNING + "Confirm before running the following command: \n" + bcolors.ENDC
                    + "\n"
                    + bcolors.OKBLUE + cmd_from_file + bcolors.ENDC + "\n"
                    + "\nyes || no \n\n"
                    + "yes: Run & continue\n"
                    + "no:  Abort\n"
                    + "YOUR Decision: ")
                if confirm == 'yes':
                    print(bcolors.OKGREEN + "> Ok .. Let\'s continue ...\n" + bcolors.ENDC)
                    break
                elif confirm == 'no':
                    print(bcolors.FAIL + "> See you \n" + bcolors.ENDC)
                    exit(1)

        for cmd in lines:
            self.execute(cmd=cmd,print_stdout=print_stdout, exit_on_fail=exit_on_fail, print_json=print_json, search=search)





    def backup_config(self, comment=''):
        if self.vendor == 'Cisco':
            test = self.execute('show version', exit_on_fail=False)
            if test['exit_code'] == 0:
                self.backup_command = cisco.backup_command
            else:
                self.backup_command = cisco.backup_command_conf

        elif self.vendor == 'Huawei':
            pass

        backup_cmd = self.execute(self.backup_command)
        if backup_cmd['exit_code'] == 1:
            print("[ Error ] " + bcolors.FAIL + "something went wrong while taking the backup" + bcolors.ENDC)
            exit(1)
        backup.create_task_directory()
        date = datetime.today().strftime('%d-%m-%Y-%H-%M-%S')
        backup_file_name = backup.task_dir + '/' +self.host + '__' + date + '.txt'

        ### Clean backup output
        backup_cmd['stdout'] = re.sub(self.clean_output_search_keyword, '', backup_cmd['stdout'])
        for i in self.backup_command.split("\n"):
            backup_cmd['stdout'] = backup_cmd['stdout'].replace(i, '')
        backup_cmd['stdout'] = backup_cmd['stdout'].strip()
        ###

        backup.save_backup_to_file(file=backup_file_name, data=backup_cmd['stdout'])
        if (os.path.isfile(backup_file_name)) and (os.path.getsize(backup_file_name) > 0):
            print("[ INFO ] " + bcolors.OKGREEN + "configuration backup taken successfully" + bcolors.ENDC)
            print("\t Device: " + self.host)
            print("\t Comment: " + comment)
            print("\t Backup saved in: {}".format(backup_file_name))
        else:
            print("[ Error ] " + bcolors.FAIL + "something went wrong while taking the backup" + bcolors.ENDC)
            print("\t Backup saved in: {}".format(backup_file_name))
            exit(1)

        # Writing backup information in the state file

        if not self.host in backup.state[backup.task_name]['Backups']:
            backup.state[backup.task_name]['Backups'][self.host] = []
        backup.state[backup.task_name]['Backups'][self.host].append({'date': date, 'backup': backup_file_name, 'comment': comment})


        def exit_handler():
            backup.save_state_to_json()

        atexit.register(exit_handler)

    def close(self):
        """
        Close the ssh session, ssh session is opened at the initialization of the Class
        :return:
        """
        ssh_auth.close()

