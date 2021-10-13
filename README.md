# Flexible_Network

This is a Python Project that aims to make network automation with Python more flexible

---

## Drive

Automating network devices with Python isn't really flexible because you're dealing with a dump device (only returns output, no `STDERR`, no `exit_code` .. only output) ... which makes automating them a bit of static task

* So the main Idea of this project is give you the same feeling as automating Linux machines. by returning  different information upon executing a command on a network device, (e.g `STDOUT`, `STDERR`, `EXIT_CODE`) among others
  * That is possible by detecting errors when executing commands on network devices
* The above concept gave a lot of flexibility to add [more features](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/README.md#features)



---



### Why should we use this Project while we can use Ansible for network automation !

 Ansible provides good means for network automation, it is idempotent, gather facts, & supports config backups as well among other features

But the question should be **Python vs. Ansible for network automation** and this is a controversy topic as each is suitable for different use cases



This project aims to improve the way we use python for network automation. :hand:





---



# Features

* Ability to **detect errors** when executing commands on network devices [[Sample output](https://i.imgur.com/5taJkl2.png)]
    * Default behaviour is to abort if an error was encountered
* **Returns different outputs** as the result of commands (`STDOUT`, `STDERR`, `EXIT_CODE`) which you can use with python conditions
* Ability to **search in a command output** using Regular Expressions. 
* Ability to **ask for confirmation** before executing a particular command  [[Sample Output](https://i.imgur.com/331PPsy.png)]
* Ability to **backup config** locally (at any point of time within your script)  [[Sample Output](https://i.imgur.com/8AS8d6a.png)]
* List tasks with backups (Keeps the state of backups) [[Sample output](https://i.imgur.com/sKiZogL.png)]
* Print commands outputs
* Print commands output in `Json` [[Sample Output](https://i.imgur.com/Dgeh4kQ.png)]
* print messages with different levels (colors) i.e  `info`, `warning`, `alert` 





---



## To be done

- [ ]  supports groups in the hosts file (In other words using the same mechanism Ansible uses for the inventory)
- [ ] Support Backup restore (Still thinking)







---


# Usage

1. Create an empty Python script; [Sample Script](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L1)
2. Import needed classes
```python
from flexible_network_.main import SSH_Connection
from flexible_network_.main import inventory

# This 'hosts' variable returns a dict i,e  {hosts: [host1, host2], hosts_number: N}
hosts = inventory.text_file()
```
3. [Loop](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L14) over the hosts in the `hosts['hosts']` variable & start use the provided methods
4. Write your code using the [available methods](https://github.com/eslam-gomaa/Flexible_Network#methods-documentation) -- [Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L1)
5. Run your script as a CLI
```bash
python 3.6 <your script>.py -h
```



**Example**

```bash
python3.6 Example-2.py -f hosts.txt --task 'Day 4' --comment 'Some checks & taking backups of some devices'
# --task is important
```

---

## Methods Documentation


#### `execute()`

Execute commands on the network device



> Method options

| Option               | Description                                                  | Default Value |
| -------------------- | ------------------------------------------------------------ | ------------- |
| cmd                  | Command to run on the network device                         |               |
| cmd_from_file        | File to load commands from (will be run as 1 command)        |               |
| print_stdout         | Print the output                                             | False         |
| print_json           | Print the output in Json format                              | False         |
| ask_for_confirmation | Ask for information before running specific command          | False         |
| search               | keyword to search in the command's output (using Regular Expressions) | None          |
| exit_on_fail         | Abort if got an error while executing the command            | True          |





#### `execute_from_file()`  
Loads commands from a file & executes them 1 by 1

`NOTE` running each line 1 by 1 will detect the error faster



> Method options

| Option               | Description                                                  | Default Value |
| -------------------- | ------------------------------------------------------------ | ------------- |
| file                 | Specify the file to load commands from (each line will run seperately) |               |
| print_stdout         | Print the output                                             | False         |
| print_json           | Print the output in Json format                              | False         |
| ask_for_confirmation | Ask for information before running specific command          | False         |
| search               | keyword to search in the command's output (using Regular Expressions) | None          |
| exit_on_fail         | Abort if got an error while executing the command            | True          |




#### `print()`  

Print messages with different levels

🟢 Info

🟡 warning

🔴 alert



> Method options

| Option | Description                                      | Default Value | Options                    |
| ------ | ------------------------------------------------ | ------------- | -------------------------- |
| msg    | The message to print                             |               |                            |
| level  | The print level (Each level has different color) | 'info'        | 'info', 'warning', 'alert' |



#### `backup_config()`

Take backup from the configuration of the device & store it locally



> Method options

| Option  | Description            | Default Value |
| ------- | ---------------------- | ------------- |
| Comment | Comment for the backup |               |





#### `close()`

Close the SSH Connection with the device




---



## Access configurations backups 



`NOTE` -- If you used the [backup_config](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L29) method within your script, the state of your task will be stored

`NOTE` --  **Currently** the state of backups is stored in a Json file in the current direction.

---


* List the tasks

```bash
python3.6 Example-2.py --list
```

---

* Filter the tasks with date

```bash
# Date format --> day-month-year
python3.6 Example-2.py --list --filter_date 11-10-2021
```



* Show the backups of a task

```bash
python3.6 Example-2.py --show Day-4__11-10-2021-09-32-01
```



---



Example Screenshot

![image](https://user-images.githubusercontent.com/33789516/137085811-63770ec9-55e7-41ca-9c3c-22909c8047f2.png)



---


## Screenshoots

Output of a [Example-2.py](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py)

![1](https://i.imgur.com/TRcFcSN.png)

![2](https://i.imgur.com/pWYqqfR.png)


---

