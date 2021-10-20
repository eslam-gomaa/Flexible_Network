# Import 'colors' class
from ._colors import Bcolors

bcolors = Bcolors()

# Import 'CLI arguments' class
from ._cli import Argument_Parser

arg_parser = Argument_Parser()
arg_parser.argparse()

from ._list_backups import List_Backups

list_backups = List_Backups()

if arg_parser.list_backups:
    list_backups.list_tasks_table()
    exit(1)

if arg_parser.show_backups is not None:
    list_backups.show_backups_table()
    exit(1)

# Import 'ssh methods' class
from ._ssh import SSH_Connection

# Import 'Hosts file' class
from ._hosts import Inventory

inventory = Inventory()
inventory.text_file()
