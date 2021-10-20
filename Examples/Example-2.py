# import FlexibleNetwork
from FlexibleNetwork import SSH_Connection
from FlexibleNetwork import inventory

hosts = inventory.text_file()


username = 'orange'
password = 'cisco'
enable_pwd = 'cisco'

# ****************************** Start **************************************

for host in hosts['hosts']:
    connection = SSH_Connection(host, username, password, vendor='Cisco')

    connection.execute(cmd='enable\n' + enable_pwd)
    # connection.execute(cmd='enable\n')

    check_version = connection.execute(cmd="sh version", search='Cisco IOS Software, IOSv Software', exit_on_fail=False)
    if not check_version['search_found?']:
        connection.print("Based on the output of the last command --> This device is a Cisco Switch", level='warn')

    connection.print('Let\'s do some more testing ... ^_^', level='info')
    connection.print('Will run a command based on the "exit_code" of another command', level='alert')
    if connection.execute(cmd="show ip int br", print_json=True, ask_for_confirmation=False)['exit_code'] == 0:
        connection.backup_config(comment='Taking backup before running important commands')
        connection.print('Now will execute commands from a file', level='info')
        connection.print('Each command will be executed separately & will abort an error was encountered', level='warn')
        connection.execute_from_file(file='conf_file.txt', print_json=False, ask_for_confirmation=True)
        connection.backup_config(comment='Taking another backup')


    # ******************************* End ***************************************

    connection.close()
