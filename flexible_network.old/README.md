# Flexible_Network



* This is a Python Project that aims to make network automation with Python more flexible
* 

Automating network devices isn't really nice because you're dealing with a dump device (only returns output, no STDERR, no exit_code .. only output) ... which makes automating them a bit static

* So the main Idea of this project is give you the same feeling as automating Linux machines. by returning  different information upon executing a command on a network device, (i.e `STDOUT`, `STDERR`, `EXIT_CODE`) among others
  * That is possible by detecting the errors when executing commands on network devices
* The above concept gave a lot of flexibility to add more features



#### How it works 

* All you have to do 



---



## Features

* Ability to **detect errors** when executing commands on network devices
* **Returns different outputs** as the result of commands (`STDOUT`, `STDERR`, `EXIT_CODE`) which you can use with python conditions
* Ability to **search in a command output** using Regular Expressions.
* Ability to **ask for confirmation** before executing a particular command
* Ability to **backup config** locally (at any point of time within your script)
* List tasks with backups (Keeps the state of backups)
* Print commands outputs
* Print commands output in `Json`
* print messages with different levels (colors) i.e  `info`, `warning`, `alert`
* 



### Example 

```bash
python3.6 Example-2.py -f hosts.txt --task test4
```





