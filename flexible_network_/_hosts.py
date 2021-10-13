from ._cli import Argument_Parser
arg_parser = Argument_Parser()
arg_parser.argparse()

class Inventory:
    def __init__(self):
        self.hosts_file = arg_parser.hosts_file # Unused for now

    def text_file(self, file=arg_parser.hosts_file):
        hosts_file_ = open(file, 'r')
        h1 = hosts_file_.read().split("\n")
        info = {}
        info['hosts'] = [string for string in h1 if string != '']
        info['hosts_number'] = len(info['hosts'])
        return info

