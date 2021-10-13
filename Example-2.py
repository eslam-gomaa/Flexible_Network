from flexible_network_.main import SSH_Connection
from flexible_network_.main import inventory

hosts = inventory.text_file()


username = 'orange'
password = 'cisco'
enable_pwd = 'cisco'

# ****************************** Start **************************************

print("[ INFO ] Number of hosts left: " + str(hosts['hosts_number']))
for host in hosts['hosts']:
    connection = SSH_Connection(host, username, password, vendor='Cisco')

    connection.execute(cmd='enable\n' + enable_pwd)
    # connection.execute(cmd='enable\n')

    # connection.execute_from_file('conf_file.txt', ask_for_confirmation=False, print_stdout=True, print_json=False)
    connection.print("Testing using conditions...", level='info')
    check_version = connection.execute(cmd="sh version", search='Cisco IOS Software, IOSv Software', exit_on_fail=False)
    if check_version['search_found?']:
        connection.print("This device is a Cisco Switch", level='warn')

    connection.print('Let\'s do some more testing ... ^_^', level='info')
    connection.print('Will run a command based on the "exit_code" of another command', level='alert')
    if connection.execute(cmd="show ip int br", print_json=True, ask_for_confirmation=False)['exit_code'] == 0:
        connection.backup_config(comment='Taking backup before running important command')
        connection.print('The next command will ask for confirmation before execution', level='info')
        connection.execute_from_file(file='conf_file.txt', print_json=False, ask_for_confirmation=False)
        connection.backup_config(comment='Taking another backup')


    # ******************************* End ***************************************

    hosts['hosts_number'] -= 1
    print('')
    connection.close()
