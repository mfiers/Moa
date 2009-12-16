## Imports ##

from optparse import OptionParser

import sys
sys.path.append("../../../")

from wwwmoa import info
from prompt import print_sys_message
from prompt import print_error_message
from prompt import print_fatal_error_message
from prompt import print_message
from prompt import do_bool_prompt

from actions import port_has_env

import os
import os.path
import subprocess
import random
import threading
import time


cl_parser=OptionParser()

cl_parser.set_defaults(port=8080, instance=None, home_dir=None,
                       act_run=False, act_kill=False, act_status=False, act_kill_all=False,
                       flag_noconf=False, flag_preserve=False)

cl_parser.add_option(
    "-r", "--run",
    action="store_true",
    dest="act_run",
    help="run an instance of lighttpd that hosts "+info.get_name()
    )

cl_parser.add_option(
    "-m", "--home",
    action="store",
    dest="home",
    type="string",
    help="specifies the content directory to use for "+info.get_name()+"; required for -r"
    )

cl_parser.add_option(
    "-p", "--port",
    action="store",
    dest="port",
    type="int",
    help="specifies the TCP port to start the instance of lighttpd on"
    )

cl_parser.add_option(
    "-k", "--kill",
    action="store_true",
    dest="act_kill",
    help="terminate an instance of lighttpd that was started using this utility"
    )

cl_parser.add_option(
    "-l", "-s", "--status",
    action="store_true",
    dest="act_status",
    help="display the currently running instances of lighttpd that were started using this utility"
    )

cl_parser.add_option(
    "-K", "--kill-all",
    action="store_true",
    dest="act_kill_all",
    help="terminate all instances of lighttpd that were started using this utility"
    )

cl_parser.add_option(
    "-q", "--no-conf",
    action="store_true",
    dest="flag_noconf",
    help="do not prompt for confirmations or additional information"
    )

cl_parser.add_option(
    "-i", "--id", "--instance",
    action="store",
    type="int",
    dest="instance",
    help="specifies the lighttpd instance id to use when altering an existing instance; this may or may not be the process id associated with the instance"
    )

cl_parser.add_option(
    "-e", "--preserve-env",
    action="store_true",
    dest="flag_preserve",
    help="preserves the environment currently associated with the given port; causes -m to be ignored"
    )

(opt, leftover_args)=cl_parser.parse_args()



action_count=0

if opt.act_run: action_count+=1
if opt.act_kill: action_count+=1
if opt.act_status: action_count+=1
if opt.act_kill_all: action_count+=1

if action_count==0:
    print_fatal_error_message("Sorry, but you did not include any action to complete.  Please use -h for more information.")
elif action_count>1:
    print_fatal_error_message("Sorry, but you specified too many actions to complete at once.  Please use -h for more information.")

inter=not opt.flag_noconf

if not inter:
    print_sys_message("No confirmations or additional information will be requested.")


if opt.act_run:
    if opt.home==None and not opt.flag_preserve:
        print_fatal_error_message("Sorry, but you did not specify a content directory using -m.  This is required when using -r.  Please use -h for more information.")


    opt.home=os.path.expanduser(opt.home)

    if opt.port<1 or opt.port>65535:
        print_fatal_error_message("Sorry, but the TCP port you specified is outside the range allowed.")
    elif opt.port<1024:
        print_error_message("Note that the server may not start successfully unless you are the root user.  This is because the TCP port you specified is below 1024.  On most Unix-like systems, you can only \"bind\" ports lower than 1024 if you are the root user.")

    if opt.flag_preserve and not port_has_env(opt.port):
        print_fatal_error_message("Sorry, but no configuration currently exists for the environment on port "+str(opt.port)+". To run the new instance, please rerun this utility without -e or --preserve-env.")

    if opt.flag_preserve:
        print_sys_message("The content directory will not be modified from its current value for port "+str(opt.port)+".")
    else:
        print_sys_message("The content directory that will be used is \""+opt.home+"\".")

    print_sys_message("The TCP port that the server will listen on is "+str(opt.port)+".")



    if inter and port_has_env(opt.port) and not opt.flag_preserve:
        if not do_bool_prompt("There is currently an environment configuration associated with TCP port "+str(opt.port)+". Do you wish to overwrite it?  If you do not, the instance will not be able to be started.  To preserve the environment, please rerun the utility with -e."):
            sys.exit()

    from actions import run

    if inter:
        if not do_bool_prompt("Are you sure you wish to start the instance?"):
            sys.exit()

    run(opt.port, opt.home, opt.flag_preserve)

elif opt.act_status:
    from actions import status

    status()

elif opt.act_kill:
    if opt.instance==None:
        print_fatal_error_message("Sorry, but you did not specify an instance id using -i.  This is required when using -k. Please use -h for more information.")
    elif opt.instance<1:
        print_fatal_error_message("Sorry, but the instance id you specified is outside the range allowed.")

    from actions import kill
    from actions import is_instance_running

    if not is_instance_running(opt.instance):
        print_fatal_error_message("Sorry, but the instance you specified is not currently running.")

    if inter:
        if not do_bool_prompt("Are you sure you wish to kill the instance?"):
            sys.exit()

    kill(opt.instance)

elif opt.act_kill_all:
    from actions import killall

    if inter:
        if not do_bool_prompt("Are you sure you wish to kill all instances?"):
            sys.exit()

    killall()

sys.exit(0x00)
