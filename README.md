# salt-netdb
Salt automations for use with netdb. This requires the netdb package which can be found here:

https://github.com/erikjseidel/salt-netdb

It also requires redis-server be installed. This has been written for VyOS 1.3. Other target systems
(such as Junos) would require further modification to this package. This package is mainly intended for
educational / demonstration purposes. Further testing / modifications would be recommended before
putting it into production use.

It is recommended that the master and proxies be run in their own containers. A pre-rolled container
which include saltstack/salt + napalm, napalm-vyos (with net.cli support) and redis client python modules
can be found here:

https://hub.docker.com/r/erikjseidel/salt-napalm

The following steps assume that you are using the container above on a Debian 11 Bullseye host with
Docker installed per the instructions found here:

https://docs.docker.com/engine/install/debian/

and that netdb has been installed per the README instructions found at the netdb repository.

## Example installation steps (on Debian 11 bullseye)

These steps are as an example in order clarify the process. It is recommended that you modify them to fit
your cirumstances and automate them accordingly.

#### 1. Clone the repository into a location on your host:

```
# chgrp netdb      # A shared group of your choice. Make sure to add your user to this group.
# chmod g+w /srv
$ cd /srv
$ git clone https://github.com/erikjseidel/salt-netdb.git
$ ls
netdb  salt-netdb
```

#### 2. Create configuration to be used by master and minion containers
The containers are designed to run statelessly so certain directories and files on the host must first
be prepared and populated in order to maintain state:

On the master host:
```
$ mkdir -p /etc/salt/master.d
$ cat /etc/salt/master.d/master.conf <<EOF
enable_ssh_minions: True
timeout: 120

file_roots:
  base:
    - /srv/salt-netdb/states

pillar_roots:
  base:
    - /srv/salt-netdb/pillars

ext_pillar:
  - netdb: noarg
EOF
# cat /etc/salt/master.d/_netdb.conf <<EOF
netdb:
  url: "https://192.0.2.5:8572/api/"       # IP address and port selected during netdb setup
  key: "/etc/salt_keys/01-salt.full.pem"   # Client auth key generated during netdb setup
EOF
# mkdir /var/scratch   # scratch directory shared by host and master container (optional)
# chgrp netdb /var/scratch
# chmod g+w /var/scratch
```

On proxy minion host(s):

```
# mkdir -p /etc/salt/proxy.d
# echo "master: 192.0.2.3" > /etc/salt/proxy.d/proxy.conf  # The IP address of the master host
```

On both master and proxy minion host(s):

```
# mkdir /etc/salt_keys
# cp 01-salt.full.pem /etc/salt_keys   # The client auth key generated during netdb setup
````

There should be one salt master and one minion each for salt managed devices. The master and
minions can be on different hosts (indeed this is recommended in the case of more than 5 managed
devices or so or where devices are far away from the master host).

#### 3. Make sure that redis-server is installed on each host that has minion containers. 

In the case that you are not using host networking mode for the containers (as is the case in this 
example), make sure that redis-server is bound to the host docker IP e.g. 172.17.0.1 in addition to
the loopback IP.

#### 4. Configure firewall to allow minion access to master and redis

Also make sure that the firewall rules on your master are set to allow connections to ports from
4505 and 4506 from all minion hosts. Finally, in the case you are not using host networking mode
make sure to add a rule allowing all incoming from the docker container net (e.g. 172.17.0.0/16).

#### 5. Configure systemd to manage master and minion containers

We will use systemd to manage of containers. Install systemd launchers as per the examples below:

For the salt master container:
```
# cat /lib/systemd/system/salt-master.service <EOF
[Unit]
Description=salt netdb master containerized service
Wants=docker.service
After=docker.service

[Service]
User=root
TimeoutStartSec=0
ExecStartPre=-/usr/bin/docker kill master
ExecStartPre=-/usr/bin/docker rm master
ExecStart=/usr/bin/docker run \
	--name master \
	--hostname netops2 \
	--volume "/srv/salt-netdb:/srv/salt-netdb:rw" \
	--volume "/etc/salt/master.d/master.conf:/etc/salt/master.d/master.conf:ro" \
	--volume "/etc/salt/master.d/_netdb.conf:/etc/salt/master.d/_netdb.conf:ro" \
	--volume "/etc/salt_keys:/etc/salt_keys:ro" \
	--volume "/etc/salt/pki.master:/etc/salt/pki:rw" \
	--volume "/var/scratch:/var/scratch:rw" \
	-p 4505-4506:4505-4506 -p 8000:8000 \
	erikjseidel/salt-napalm
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
```

For the salt minion containers:
```
$ cat /lib/systemd/system/salt-cproxy@.service <EOF
[Unit]
Description=dockerized salt-proxy service for %i
Wants=docker.service
After=docker.service

[Service]
User=root
TimeoutStartSec=0
ExecStartPre=-/usr/bin/docker kill %i
ExecStartPre=-/usr/bin/docker rm %i
ExecStart=/usr/bin/docker run \
	--name %i \
	--hostname netops2 \
	--volume "/etc/salt/proxy.d/proxy.conf:/etc/salt/proxy.d/proxy.conf:ro" \
	--volume "/etc/salt/pki.%i:/etc/salt/pki:rw" \
	--volume "/etc/salt_keys:/etc/salt_keys" \
	-e SALT_PROXY_ID=%i \
	erikjseidel/salt-napalm
Restart=always
RestartSec=5s

[Install]
WantedBy=multi-user.target
EOF
```

Make sure that the volume declarations in this step align with the configuration created in
step 2.

#### 6. Enable and start the salt master

```
$ sudo systemctl enable salt-master.service
$ sudo systemctl start salt-master.service
$ systemctl status salt-master.service
$ systemctl status salt-master.service
● salt-master.service - salt netdb master containerized service
     Loaded: loaded (/lib/systemd/system/salt-master.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-04-03 07:26:33 UTC; 3h 54min ago
   Main PID: 194109 (docker)
      Tasks: 6 (limit: 1129)
     Memory: 6.3M
        CPU: 437ms
     CGroup: /system.slice/salt-master.service
             └─194109 /usr/bin/docker run --name master --hostname netops2 --volume /srv/salt-netdb>
$ sudo docker ps
erik@netops3:~$ sudo docker ps
CONTAINER ID   IMAGE                                     COMMAND                  CREATED        STATUS        NAMES
c49756887c3a   erikjseidel/salt-napalm                   "/usr/bin/dumb-init …"   Seconds ago    Seconds ago   master
701b01b40c79   mongodb/mongodb-community-server:latest   "python3 /usr/local/…"   42 hours ago   Up 42 hours   netdb
$
$ sudo docker exec -it master salt-run saltutil.sync_all
```

#### 7. Define your first minion

```
$ cat /srv/salt-netdb/pillars/proxies/sin2.sls <EOF
proxy:
  proxytype: napalm
  driver: vyos 
  device_type: vyos
  host: 192.168.34.8      # Example IP
  username: my_username
  password: my_password
  multiprocessing: False  # important. keep this

netdb:
  id: SIN2                # As defined in netdb initial device load.
EOF
$ cat /srv/salt-netdb/pillars/top.sls <EOF
base:
  sin2:
    - proxies/sin2
```

#### 8. Enable and start your first minion and accept its key on the master

```
minion-host$ sudo systemctl enable salt-cproxy@sin2.service 
minion-host$ sudo systemctl start salt-cproxy@sin2.service 
minion-host$ systemctl status salt-cproxy@sin2.service
● salt-cproxy@sin2.service - dockerized salt-proxy service for sin2
     Loaded: loaded (/lib/systemd/system/salt-cproxy@.service; enabled; vendor preset: enabled)
     Active: active (running) since Mon 2023-04-03 07:30:34 UTC; 4h 2min ago
   Main PID: 196414 (docker)
      Tasks: 6 (limit: 1129)
     Memory: 6.7M
        CPU: 448ms
     CGroup: /system.slice/system-salt\x2dcproxy.slice/salt-cproxy@sin2.service
             └─196414 /usr/bin/docker run --name sin2 --hostname netops2 --volume /etc/salt/proxy.d>

minion-host$ sudo docker ps
CONTAINER ID   IMAGE                                     COMMAND                  CREATED        STATUS        NAMES
4c9609e2443a   erikjseidel/salt-napalm                   "/usr/bin/dumb-init …"   Seconds ago    Seconds ago   sin2

master-host$ sudo docker exec -it master salt-key -a sin2

```

#### 9. Test the minion

Give a minute or so to settle and try running some commands on the master:
```
$ sudo docker exec -it master salt sin2 test.ping
sin2:
    True
$ sudo docker exec -it master salt sin2 net.cli 'sh ip bgp sum' 'sh isis neigh'
sin2:
    ----------
    comment:
    out:
        ----------
        sh ip bgp sum:
            
            IPv4 Unicast Summary:
            BGP router identifier 23.181.64.236, local AS number 36198 vrf-id 0
            BGP table version 15901365
            RIB entries 1668323, using 305 MiB of memory
            Peers 6, using 128 KiB of memory
            Peer groups 6, using 384 bytes of memory
            
            Neighbor                V         AS   MsgRcvd   MsgSent   TblVer  InQ OutQ  Up/Down State/PfxRcd   PfxSnt
            23.181.64.71            4      65085    171150    171159        0    0    0 01w1d20h           16       26
            23.181.64.73            4      65085    171150    171159        0    0    0 01w1d20h           16       26
            169.254.169.254         4      64515   6093617     28540        0    0    0 02w5d19h       910176        4
            fd00:136:a009:af00::227 4      36198  11772551  12579501        0    0    0 2d13h49m           24   910188
            fd00:136:a009:af00::228 4      36198  12690426  12269270        0    0    0 2d13h49m           24   910188
            fd00:136:a009:af00::237 4      36198  11899863  11885396        0    0    0 02w5d19h       910190   910188
            
            Total number of neighbors 6
        sh isis neigh:
            Area VyOS:
              System Id           Interface   L  State        Holdtime SNPA
              sin3                eth1        2  Up            30       5a00.0444.1d0d
              fra1                tun202      2  Up            28       1a55.3f06.9e59
              dallas2             tun263      2  Up            28       667a.edb8.4a77
    result:
        True
```
