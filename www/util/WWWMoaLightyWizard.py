from WWWMoaLightyConf import get_config_file
from WWWMoaLightyConf import get_env_file

from WWWMoaLightyPrompt import print_sys_message
from WWWMoaLightyPrompt import print_error_message
from WWWMoaLightyPrompt import print_message
from WWWMoaLightyPrompt import do_main_prompt
from WWWMoaLightyPrompt import do_prompt
from WWWMoaLightyPrompt import do_bool_prompt
from WWWMoaLightyPrompt import do_int_prompt

from WWWMoaLightyInst import add_instance
from WWWMoaLightyInst import show_status
from WWWMoaLightyInst import get_current_ids
from WWWMoaLightyInst import _inst

import sys
import os
import os.path
import subprocess
import random
import threading
import time



def get_tmp_file_path(dir_path):
    file_path=""

    while file_path=="":
        file_path=os.path.join(dir_path, "wc-"+str(random.randint(100000, 999999))+".tmp")

        if os.access(file_path, os.F_OK):
            file_path=""

    return file_path


def get_env_file_path(port):
    return os.path.join(os.getcwd(), "../conf/env/"+str(port)+".xml")


def do_run_wizard():
    print_sys_message("I will now help you run a new instance of lighttpd for WWWMoa.")




    param_name=do_prompt("Please enter a descriptive name for your instance.  If left blank, we will choose one for you.  Note that the name is not used as a unique identifier, and, therefore, does not need to be unique.")

    param_name=param_name.strip()

    if param_name=="":
        param_name="Untitled Instance"





    while True:
        param_port=do_int_prompt("Please enter the TCP port that you want to start the instance on.  Note that the TCP port should be an integer between 1 and 65535.  Also note that, if you are on a Unix-like system and are not the root user, you may not be able to start the instance on ports less than 1025.")

        param_port_path=get_env_file_path(param_port)
        

        if param_port<1 or param_port>65535:
            param_port_conf=do_bool_prompt("The TCP port you entered does not appear to be valid.  Do you wish to enter another port? If you do not enter another port, you will not be able to start the instance.")

            if not param_port_conf:
                return
        elif os.access(param_port_path, os.F_OK):
            param_port_path_conf=do_bool_prompt("Currently, there appears to be an environment configuration present for port "+str(param_port)+". Continuing would overwrite this configuration.  Do you want to continue?")

            if not param_port_path_conf:
                return

            break
        else:
            break



    while True:
        param_path=do_prompt("Please enter the path of the content path for the instance.  The content path will be where the data the Moa uses will be placed.")

        if not os.access(param_path, os.F_OK):
            param_path_conf=do_bool_prompt("The path you entered does not exist.  Do you wish to enter another path?  If you do not enter another path, you will not be able to start the instance.")

            if not param_path_conf:
                return

        elif not os.access(param_path, os.R_OK | os.W_OK):
            param_path_conf=do_bool_prompt("You do not seem to have read / write permission for the path you entered.  This is a requirement for the content path.  Do you wish to enter another path?  If you do not enter another path, you will not be able to start the instance.")

            if not param_path_conf:
                return

        elif not os.path.isdir(param_path):
            param_path_conf=do_bool_prompt("The path you typed does not correspond to a directory.  Do you wish to enter another path?  If you do not enter another path, you will not be able to start the instance.")

            if not param_path_conf:
                return

        else:
            break




    print_sys_message("You have now entered all of the required parameters.")

    
    confirmation=do_bool_prompt("Are you sure you want to start the new instance?")
    
    if not confirmation:
        print_sys_message("The new instance will NOT be started.")
        return

    print_sys_message("I will now attempt to start up the instance.")
    print_sys_message("I am currently performing several steps nessesary to configure the instance.")

    tmp_conf_dir=os.path.join(os.getcwd(), "conf")

    try:
        if not os.access(tmp_conf_dir, os.F_OK):
            os.mkdir(tmp_conf_dir)
        
        tmp_conf_file_path=get_tmp_file_path(tmp_conf_dir)

        tmp_conf_file=open(tmp_conf_file_path, "w+b")
        tmp_conf_file.write(get_config_file(param_port))
        tmp_conf_file.close()

    except:
        print_error_message("Something went wrong: an file system error was encountered while performing configuration. This may be because of your file system permissions.")

    try:
        env_file=open(param_port_path, "w+b")
        env_file.write(get_env_file(param_path))
        env_file.close()
    except:
        print_error_message("Something went wrong: the environment could not be configured. This may be because of your file system permissions.")
        os.unlink(tmp_conf_file_path)

    try:
        lighttpd=subprocess.Popen(["lighttpd", "-D", "-f", tmp_conf_file_path],0,None,subprocess.PIPE,subprocess.PIPE,subprocess.PIPE)
    except:
        print_error_message("Something went wrong: lighttpd could not be started.")

        os.unlink(tmp_conf_file_path)
    else:
        add_instance(param_name, param_port, param_path, tmp_conf_file_path, param_port_path, lighttpd)

        print_sys_message("I was able to start the instance successfully (as far as I can tell).")

        time.sleep(2.5) # wait a brief time to see if lighttpd terminates immediatly
        
   

def do_kill_wizard():
    global _inst

    print_sys_message("I will help you kill an instance.  The currently running instances are shown below.")

    show_status()

    tokill=do_int_prompt("Please type the number of the instance you wish to kill.")

    if not tokill in get_current_ids():
        print_message("The instance you specified is not currently running.")
        return

    kill_conf=do_bool_prompt("Are you sure you want to terminate the instance?")

    if not kill_conf:
        print_sys_message("The instance was NOT terminated.")
        return

    tk=None
    for i in _inst:
        if i["id"]==tokill:
            tk=i
            break

    try:
        tk["process"].terminate()
    except Exception as err:
        print_error_message("I was unable to terminate the instance.")
    else:
        print_sys_message("I have instructed the instance to terminate.  It may take a little bit longer to terminate completely.")


