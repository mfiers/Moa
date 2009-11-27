from conf import get_config_file
from prompt import print_sys_message
from prompt import print_error_message
from prompt import print_message
from prompt import do_main_prompt
from prompt import do_prompt
from prompt import do_bool_prompt
from prompt import do_int_prompt


import sys
import os
import os.path
import subprocess
import random
import threading
import time

_inst=[]



def show_status():
    global _inst

    print "ID   | Port | Name            | Content Dir"
    print "----------------------------------------------------------------"

    for i in _inst:
        print str(i["id"]).ljust(5)[:5]+"  "+str(i["port"]).ljust(5)[:5]+"  "+ i["name"].ljust(16)[:16]+ "  "+("\""+ i["contentdir"].replace("\"", "\\\"")+"\"").ljust(32)[:32]

    print ""


        
    
def get_current_ids():
    ids=[]

    for i in _inst:
        ids.append(i["id"])    

    return ids

def get_next_instance_id():
    global _inst

    ids=get_current_ids()

    x=1
    while x in ids:
        x+=1

    return x

def add_instance(name, port, contentdir, conffile, conffile2, process):
    global _inst

    _inst.append({"name" : name, "port" : port, "contentdir" : contentdir, "conffile" : conffile, "conffile2" : conffile2, "process" : process, "id" : get_next_instance_id()})


def do_cleanup():
    global _inst

    for i in _inst:
        i["process"].poll()

        if i["process"].returncode!=None:
            _inst.remove(i)

            if i["process"].returncode>0:
                print_error_message("It appears that lighttpd encountered a fatal error.  It said:")
                print "\"" + i["process"].stderr.read(2048)+"\"" # cap the output so that things do not get out of hand

            i["process"].stdin.close()
            i["process"].stdout.close()
            i["process"].stderr.close()
            os.unlink(i["conffile"])
            os.unlink(i["conffile2"])

    schedule_cleanup()


def schedule_cleanup():
    threading.Timer(1, do_cleanup).start()
