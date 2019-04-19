# Importing fabric module for checking the host details
# It is multipurpose Script to perform action on remote machine.
# Written by Gaurav Kumar Singh.
# It is used for Adding Routes on ZFS filer
# Login to Sun ILOM and initiate OS installation.
from fabric.api import *
import sys
import os
import json

# Reading Host file to Determine the Target hosts
try :
    with open ( 'host.txt', 'r' ) as f :
        env.hosts = f.read ().splitlines ()

except :
    print ( "ERROR:::::>>>>:::::Please make sure host.txt file exists" )
    exit ()

# Reading Credential file to Determine the usename and Passowrd

try :
    with open ( 'filename.json', 'r' ) as f :
        datastore = json.load ( f )
        env.password = datastore['password']
        env.user = datastore['username']

except :
    print ( "ERROR::::::>>>>:::::Credential file missing" )
    exit ()


# Reading Command file to Determine Commands to run on  Target hosts


def host_commands() :
    try :
        with open ( 'commands.txt', 'r' ) as f :
            commands = f.read ().splitlines ()
            for x in commands :
                run ( x )
    except :
        print ( "Something went Bad" )


