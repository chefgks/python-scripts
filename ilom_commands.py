# Python Script to Login to ILOM and execute ILOM commands like set boot device, reboot etc
# Written By Gaurav Singh
# Email: <er.gaurav83@yahoo.in>
import pexpect
from pexpect import pxssh
import sys
from getpass import getpass

def process_args():
    from optparse import OptionParser
    usage = "usage: %prog [options] <hostname> [<hostname> <hostname>]"
    parser = OptionParser(usage)
    parser.add_option("-u", "--username", dest="username",
            help="iLOM username (default: %default)")
    parser.add_option("-p", "--password", dest="password",
            help="iLOM password (default: %default)")
    parser.add_option("-f", "--file", dest="commands_file",
            help="file with commands to run (default: stdin/pipe)")
    parser.add_option("-v", "--verbose", dest="verbose", action="store_true",
            help="be verbose in output (default: %default)")


    parser.set_defaults(username = 'gaurav',
                        password = 'abc123',
                        commands_file = False,
                        verbose = False)
    return parser.parse_args()

def get_commands(commands_file):
    commands = []
    if commands_file:
        f = open(commands_file, "r")
        commands = f.read().splitlines()
        f.close()
    else:
        while True:
            line = sys.stdin.read().splitlines()
            if line:
                commands.append(line)
            else:
                break
    return commands

def exec_on_hosts(commands, hosts, options):

    if not options.password:
        options.password = getpass("Password: ")

    for host in hosts:
        try:
            if options.verbose:
                print 'ssh %s@%s' %(options.username,host)
            child = pexpect.spawn('ssh %s@%s' %(options.username,host))
            child.expect('(?i)Password:')
            if options.verbose:
                child.logfile = sys.stdout
            child.sendline(options.password)

            for command in commands:
                child.expect(['~\#',
                              '\(y/n\)\?'])
                child.sendline(command)

            child.expect('~\#')
            child.sendline('exit')
            child.close()
        except:
            error='Error: at least one command failed to execute on %s\n' %host
            sys.stderr.write(error)
            child.close()


def main():
    (options, hosts) = process_args()
    commands = get_commands(options.commands_file)
    print(commands)
    print(options)
    print(hosts)
    exec_on_hosts(commands, hosts, options)

if __name__ == '__main__':
    main()

