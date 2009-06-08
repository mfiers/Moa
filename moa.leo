<?xml version="1.0" encoding="utf-8"?>
<?xml-stylesheet ekr_test?>
<leo_file>
<leo_header file_format="2" tnodes="0" max_tnode_index="0" clone_windows="0"/>
<globals body_outline_ratio="0.5">
	<global_window_position top="10" left="10" height="790" width="1258"/>
	<global_log_window_position top="0" left="0" height="0" width="0"/>
</globals>
<preferences/>
<find_panel_settings/>
<vnodes>
<v t="mf.20090529111457.1" str_leo_pos="2"><vh>@chapters</vh></v>
<v t="mf.20090530071644.1"><vh>Virtual machine</vh>
<v t="mf.20090530071644.2"><vh>install log</vh></v>
</v>
<v t="mf.20090529111457.2"><vh>bin</vh></v>
<v t="mf.20090529111457.22"><vh>templates</vh>
<v t="mf.20090529111457.21"
expanded="mf.20090529111457.24,"><vh>@shadow template/blast.mk</vh></v>
<v t="mf.20090529152037.1"><vh>@shadow template/moaBase.mk</vh></v>
<v t="mf.20090529153542.1"><vh>@shadow template/traverse.mk</vh></v>
<v t="mf.20090529153542.9"><vh>@shadow template/upload2gbrowse.mk</vh></v>
<v t="mf.20090529193921.1"><vh>@shadow template/upload2gbrowseInclude.mk</vh></v>
<v t="mf.20090530092652.3"><vh>@shadow template/createBlastDb.001.mk</vh></v>
<v t="mf.20090531095217.2"><vh>@shadow template/create.gbrowse.db.mk</vh></v>
<v t="mf.20090601150139.1"><vh>@shadow template/getFromNcbi.mk</vh></v>
</v>
</vnodes>
<tnodes>
<t tx="mf.20090529111457.1"></t>
<t tx="mf.20090529111457.2"></t>
<t tx="mf.20090529111457.22"></t>
<t tx="mf.20090530071644.1"></t>
<t tx="mf.20090530071644.2">@language text
JEOS Ubuntu 8.04LTS

executed on the host, to allow ssh:
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/ssh/HostPort" 2222
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/ssh/GuestPort" 22
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/ssh/Protocol" TCP
and http:
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/http/HostPort" 8080
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/http/GuestPort" 80
 VBoxManage setextradata moaM8 "VBoxInternal/Devices/pcnet/0/LUN#0/Config/http/Protocol" TCP

standard ubuntu packages installed:
 - sshds
 - qemacs
 - wget 
 - make
 - gcc
 - blast2
 - apache2
 - libapache2-mod-perl2
 - libapache2-mod-perl2-dev
 - libapache2-mod-perl2-doc
 - apache2-doc
 - libgd2-xpm-dev

Installation of generic genome browser following:
 http://gmod.org/wiki/GBrowse_Ubuntu_HOWTO
This included the installation of bioperl 1.6

Further packages, all installed under /usr/local
emboss 6.0.1</t>
</tnodes>
</leo_file>
