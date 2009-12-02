from conf import get_config_file
from conf import get_env_file
from conf import get_env_file_path

from prompt import print_sys_message
from prompt import print_error_message
from prompt import print_fatal_error_message
from prompt import print_message
from prompt import do_main_prompt
from prompt import do_prompt
from prompt import do_bool_prompt
from prompt import do_int_prompt



import sys
import os
import os.path
import subprocess
import time


def get_new_id():
    id=1

    while os.access(get_instance_status_path(id), os.F_OK):
        id+=1

    return id

def get_var_path():
    return os.path.normpath(os.path.join(os.path.dirname(__file__),"../../../../../../var/www/"))

def get_instance_status_path(id):
    return os.path.join(get_var_path(),".stat."+str(int(id)))

def get_instance_meta_path(id):
    return os.path.join(get_var_path(),".meta."+str(int(id)))

def is_instance_running(id):
    return os.access(get_instance_status_path(id), os.F_OK)

def set_instance_running(id):
    fstat=open(get_instance_status_path(id), "w+")
    fstat.write("")
    fstat.close()

def set_instance_terminated(id):
    fstat_path=get_instance_status_path(id)

    if os.access(fstat_path, os.F_OK):
        os.unlink(fstat_path)

def get_running_instances():
    ids=[]

    idf=os.listdir(get_var_path())

    for f in idf:
        if f[:6]==".stat.":
            try:
                ids.append(int(f[6:]))
            except:
                pass

    return ids

def run(port, home, penv):
    print_sys_message("I will now run a new instance of lighttpd for WWWMoa.")

    try:
        if not os.access(get_var_path(), os.F_OK):
            if os.access(os.path.normpath(os.path.join(get_var_path(),"../../")), os.F_OK):
                os.makedirs(get_var_path())
            else:
                print_fatal_error_message("Something went wrong: the Moa base directory could not be found")
    except Exception as e:
        print_fatal_error_message("Something went wrong: file system preparation failed."+str(e))
    

    conf_path=os.path.join(get_var_path(),".conf."+str(port))
    
    id=get_new_id()

    if not penv:
        try:
            env_file=open(get_env_file_path(port), "w+b")
            env_file.write(get_env_file(home))
            env_file.close()
        except:
            print_fatal_error_message("Something went wrong: the environment could not be configured. This may be because of your file system permissions.")

    try:
        meta_file=open(get_instance_meta_path(id), "w+b")
        if penv:
            meta_file.write(str(port)+"\0(Content Directory Unknown)")
        else:
            meta_file.write(str(port)+"\0"+home)
        meta_file.close()
    except:
        pass


    try:
        conf=open(conf_path, "w+b")
        conf.write(get_config_file(port, home))
        conf.close()

        set_instance_running(id)

        me=os.fork()

        if me==0: # i am a child
            lighttpd=subprocess.Popen(["lighttpd", "-D", "-f", conf_path],0,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)

            while True:
                time.sleep(1)
                
                if not is_instance_running(id):
                    lighttpd.terminate()
                    break

                lighttpd.poll()

                if lighttpd.returncode!=None:
                    set_instance_terminated(id)
                    break

            sys.exit(0)
        else: # i am a parent
            pass
    except Exception as e:
        print_fatal_error_message("Something went wrong: lighttpd could not be started. "+str(e))
    

def kill(id):
    global _inst

    print_sys_message("I will now kill an instance.")

    set_instance_terminated(id)

    print_sys_message("I have instructed the instance to terminate.  It may take a few more seconds for it to completely terminate.")

def status():
    ids=get_running_instances()

    print "Instance Listing"
    print "----------------------------------------------------------"
    print " ID   |  Port  |  Content Directory"
    print "----------------------------------------------------------"

    for i in ids:
        p=get_instance_meta_path(i)

        if os.access(p, os.R_OK):
            pf=open(p, "rb")
            mstr=pf.read(64)
            marr=mstr.split("\0")
            pf.close()


        print str(i).center(5)[:5]+"   "+marr[0].center(5)[:5]+"   "+marr[1].center(42)[:42]

def killall():
    print_sys_message("I will now kill all instances.")

    ids=get_running_instances()

    for i in ids:
        set_instance_terminated(i)

    print_sys_message("I have instructed the instances to terminate.  It may take a few more seconds for all of them to completely terminate.")
