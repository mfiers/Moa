from conf import get_config_file
from conf import get_env_file
from conf import get_password_file

from prompt import print_sys_message
from prompt import print_error_message
from prompt import print_fatal_error_message
from prompt import print_message
from prompt import do_main_prompt
from prompt import do_prompt
from prompt import do_bool_prompt
from prompt import do_int_prompt

from  moa.logger import l

import sys
import os
import os.path
import subprocess
import time
import random
import string


sys.path.append(os.path.join(os.path.dirname(__file__), "../../"))

import wwwmoa.info.moa as moainfo

def _prepare_fs():
    try:
        if not os.access(get_var_path(), os.F_OK):
            os.makedirs(get_var_path())
        if not os.access(get_etc_path(), os.F_OK):
            os.makedirs(get_etc_path())
    except Exception as e:
        l.critical("Something went wrong: file system preparation "+
                   "failed.")
        l.critical(str(e))
        sys.exit(1)

def get_new_id():
    id=1

    while os.access(get_instance_status_path(id), os.F_OK):
        id+=1

    return id

def get_var_path():
    return os.path.join(moainfo.get_base(),"var/www/wwwmoalighty/")

def get_etc_path():
    return os.path.join(moainfo.get_base(),"etc/www/env/")

def get_port_env_path(port):
    return os.path.normpath(os.path.join(get_etc_path(), str(port)+".xml"))

def get_instance_path(id, prefix):
    return os.path.normpath(os.path.join(get_var_path(),prefix+"-"+str(int(id))))

def get_instance_status_path(id):
    return get_instance_path(id, "stat")

def get_instance_meta_path(id):
    return get_instance_path(id, "user")

def get_instance_conf_path(id):
    return get_instance_path(id, "lighty")

def get_instance_password_path(id):
    return get_instance_path(id, "lightyauth")

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
        if f[:5]=="stat-":
            try:
                ids.append(int(f[5:]))
            except:
                pass

    return ids

def port_has_env(port):
    return os.access(get_port_env_path(port), os.F_OK)

def get_random_password():
    source=string.digits+string.ascii_letters
    password=""

    for x in range(8):
        password=password+source[random.randint(0, len(source)-1)]

    return password

def run(port, home, penv, readonly=False, password=None, restrictlocal=False):
    
    l.info("I will now run a new instance of lighttpd for WWWMoa.")

    if moainfo.get_base()==None:
        
        l.critical("""Something went wrong: the Moa base directory
            could not be found.""")
        sys.exit(1)


    id=get_new_id()
    l.debug("server id %s" % id)

    conf_path=get_instance_conf_path(id)
    l.debug("Configuration path %s" % conf_path)


    if password=="":
        password=get_random_password()

        l.info("The randomly generated password is '"+password+"'.")

    if password!=None:
        l.info("The instance will be password protected. The user name is 'user'.")

    if restrictlocal:
        l.info("The instance will only be accessible from the local host.")
        l.debug("The server will only bind to 'localhost'.")

    if readonly:
        l.info("The instance will be read-only.")

    if not penv:
        try:
            env_file=open(get_port_env_path(port), "w+b")
            env_file.write(get_env_file(home, readonly))
            env_file.close()
        except:
            
            l.critical("""Something went wrong: the
                environment could not be configured. This may be
                because of your file system permissions.""")
            sys.exit()

    try:
        meta_file=open(get_instance_meta_path(id), "w+b")
        if penv:
            meta_file.write(str(port)+"\0(Content Directory Unknown)")
        else:
            meta_file.write(str(port)+"\0"+home)

        meta_file.write("\0"+str(readonly))
        meta_file.write("\0"+str(restrictlocal))
        meta_file.write("\0"+str(password!=None))

        meta_file.close()
    except:
        pass


    try:
        password_path=None

        if password!=None:
            password_path=get_instance_password_path(id)
            l.debug("start writing password configuration to %s" % password_path)
            password_file=open(password_path, "w+b")
            password_file.write(get_password_file(password))
            password_file.close()

        l.debug("start writing configuration to %s" % conf_path)
        conf=open(conf_path, "w+b")
        conf.write(get_config_file(port, home, password_path, restrictlocal))
        conf.close()


        set_instance_running(id)

        me=os.fork()

        if me==0: # i am a child
            commandline = ["lighttpd", "-D", "-f", conf_path]
            l.debug("executing %s" % " ".join(commandline))
            lighttpd=subprocess.Popen(
                commandline,0,
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE)

            while True:
                time.sleep(1)
                
                if not is_instance_running(id):
                    lighttpd.terminate()
                    break

                lighttpd.poll()

                if lighttpd.returncode!=None:
                    out, err = lighttpd.communicate()
                    
                    #print one newline - better output of the error
                    #message
                    sys.stderr.write("\n")
                    l.critical('lighthttpd terminated with rc %s' %
                            lighttpd.returncode)
                    if out:
                        l.info(out)
                    if err:
                        l.critical(err)
                    set_instance_terminated(id)
                    break

            sys.exit(0)
        else: # i am parent
            pass
        
    except Exception as e:
        l.critical("Something went wrong: lighttpd could not "+
                   " be started."),
        l.critical(str(e))
        raise
    

def kill(id):
    global _inst

    print_sys_message("I will now kill an instance.")

    set_instance_terminated(id)

    print_sys_message("I have instructed the instance to terminate.  It may take a few more seconds for it to completely terminate.")

def status():
    ids=get_running_instances()


    print "ID      Port    RO LHO PP  Content Directory"

    for i in ids:
        p=get_instance_meta_path(i)

        if os.access(p, os.R_OK):
            pf=open(p, "rb")
            mstr=pf.read(64)
            marr=mstr.split("\0")
            pf.close()

        status_line=""

        status_line+=str(i).ljust(5)[:5]+"   "
        status_line+=marr[0].ljust(5)[:5]+"   "
        status_line+=marr[2][0]+"  "
        status_line+=marr[3][0]+"   "
        status_line+=marr[4][0]+"   "
        status_line+=marr[1]

        print status_line

def killall():
    print_sys_message("I will now kill all instances.")

    ids=get_running_instances()

    for i in ids:
        set_instance_terminated(i)

    print_sys_message("I have instructed the instances to terminate.  It may take a few more seconds for all of them to completely terminate.")


_prepare_fs()
