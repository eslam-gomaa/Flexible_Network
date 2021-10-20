
class Cisco:
    def __init__(self):
        self.stderr_search_keyword='\^'
        self.clean_output_search_keyword='.*#'
        self.backup_command = """
                    terminal length 0
                    show run
                    term no len 0
                    """
        self.backup_command_conf = """
                    do terminal length 0
                    do show run
                    do term no len 0
                    """