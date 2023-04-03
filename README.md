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

The installation steps outlined in doc/installation.md assume that you are using the container above on a 
Debian 11 Bullseye host with Docker installed per the instructions found here:

https://docs.docker.com/engine/install/debian/

and that netdb has been installed per the README instructions found at the netdb repository.
