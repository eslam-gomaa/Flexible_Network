import paramiko
import time
import socket


from ._colors import Bcolors
bcolors = Bcolors()

class SSH_Auth:
    def __init__(self):
        self.is_connected = False
        self.channel = None
        self.host = None

    def auth(self, host, user, password, port=22, ssh_timeout=10, allow_agent=True):
        print(bcolors.WARNING + "> Trying to connect to (%s)" % host + bcolors.ENDC)
        i = 1
        while True:
            try:
                self.host = host
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(host, port, user, password, timeout=ssh_timeout,
                                 allow_agent=allow_agent, look_for_keys=False)
                self.is_connected = True
                connected_msg = (bcolors.OKGREEN + "> Connected to (%s)" % host + bcolors.ENDC)
                print(connected_msg)

                self.channel = self.ssh.invoke_shell()
                output = self.channel.recv(9999)
                self.channel.send_ready()
                time.sleep(1)
                break
            except paramiko.AuthenticationException as e:
                print(
                    "[ ERROR ] " + bcolors.FAIL + "Authentication failed when connecting to %s" % host + bcolors.ENDC)
                print("\t --> " + str(e))
                print("\t --> (%s) " % host + bcolors.FAIL + "Skipped" + bcolors.ENDC)
                print("")
                self.is_connected = False
                break
            except socket.gaierror as e:
                print(
                    "[ ERROR ] " + bcolors.FAIL + "Could not resolve hostname (%s) Name or service not known" % host + bcolors.ENDC)
                print("\t --> " + str(e))
                print("\t --> (%s) " % host + bcolors.FAIL + "Skipped" + bcolors.ENDC)
                print("")
                self.is_connected = False
                break
            except (paramiko.ssh_exception.NoValidConnectionsError, paramiko.SSHException, socket.error)  as e:
                print(
                    "[ ERROR ] " + bcolors.FAIL + "Not able to establish ssh connection with %s" % host + bcolors.ENDC + " , Trying again...")
                print("\t --> " + str(e))
                i += 1
                time.sleep(1)
                self.is_connected = False
                if i == 5:
                    print("[ ERROR ] " + bcolors.FAIL + "Could not connect to %s. Giving up" % host + bcolors.ENDC)
                    print("\t --> (%s) " % host + bcolors.FAIL + "Skipped" + bcolors.ENDC)
                    print("")
                    break


    def close(self):
        """
        Close the ssh session, ssh session is opened at the initialization of the Class
        :return:
        """
        if self.is_connected:
            self.ssh.close()
            print(bcolors.BOLD + "> Connection closed with (" + self.host + ')' + bcolors.ENDC)
