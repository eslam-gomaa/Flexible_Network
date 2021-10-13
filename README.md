# Flexible_Network

This is a Python Project that aims to make network automation with Python more flexible

---

## Drive

Automating network devices isn't really nice because you're dealing with a dump device (only returns output, no `STDERR`, no `exit_code` .. only output) ... which makes automating them a bit of static task

* So the main Idea of this project is give you the same feeling as automating Linux machines. by returning  different information upon executing a command on a network device, (e.g `STDOUT`, `STDERR`, `EXIT_CODE`) among others
  * That is possible by detecting errors when executing commands on network devices
* The above concept gave a lot of flexibility to add [more features](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/README.md#features)


---


# Features

* Ability to **detect errors** when executing commands on network devices [[Sample output](https://i.imgur.com/5taJkl2.png)]
    * Default behaviour is to abort if an error was encountered
* **Returns different outputs** as the result of commands (`STDOUT`, `STDERR`, `EXIT_CODE`) which you can use with python conditions
* Ability to **search in a command output** using Regular Expressions. [[Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L22)]
* Ability to **ask for confirmation** before executing a particular command [[Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L32)] [[Sample Output](https://i.imgur.com/331PPsy.png)]
* Ability to **backup config** locally (at any point of time within your script) [[Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L29)] [[Sample Output](https://i.imgur.com/8AS8d6a.png)]
* List tasks with backups (Keeps the state of backups) [[Sample output](https://i.imgur.com/sKiZogL.png)]
* Print commands outputs
* Print commands output in `Json` [[Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L28)] [[Sample Output](https://i.imgur.com/Dgeh4kQ.png)]
* print messages with different levels (colors) i.e  `info`, `warning`, `alert` [[Example](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L21)]



---


# Usage

1. Create an empty Python script; [Sample Script](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L1)
2. Import needed classes
```python
from flexible_network.main import SSH_Connection
from flexible_network.main import inventory

# This hosts variable returns a dict i,e  {hosts: [host1, host2], hosts_number: N}
hosts = inventory.text_file()
```
3. [Loop](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L14) over the hosts in the `hosts['hosts']` variable & start use the provided methods

4. Run your script using CLI
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
To be documented ... (Still in progress)

#### `execute()`
Execute commands on the network device



#### `execute_from_file()`  
Loads commands from a file & executes them 1 by 1

`NOTE` running each line 1 by 1 will detect the error faster



#### `print()`  

Print messages with different levels

🟢 Info

🟡 warning

🔴 alert

#### `backup_config`  




---

`NOTE` -- If you used the [backup_config](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py#L29) method within your script, the state of your task will be stored

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

Example Screenshot

![image](https://user-images.githubusercontent.com/33789516/137085811-63770ec9-55e7-41ca-9c3c-22909c8047f2.png)

--- 

* Show the backups of a task

```bash
python3.6 Example-2.py --show Day-4__11-10-2021-09-32-01
```



---


## Screenshoots

Output of a [Example-2.py](https://gitlab.com/eslam.gomaa1/flexible_network/-/blob/main/Example-2.py)

![1](https://i.imgur.com/TRcFcSN.png)

![2](https://i.imgur.com/pWYqqfR.png)


---


