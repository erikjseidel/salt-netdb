base:
  sin1-proxy:
    - proxies/sin1-proxy
    - node/sin1/firewall
    - node/sin1/policy
    - node/sin1/bgp
  sin2-proxy:
    - proxies/sin2-proxy
    - node/sin2/bgp
  sin3-proxy:
    - proxies/sin3-proxy
    - node/sin3/bgp
#  fra1:
#    - proxies/fra1
#    - node/fra1/isis
#  dfw2:
#    - proxies/dfw2
#    - node/dfw2/isis
#  dfw3:
#    - proxies/dfw3
#    - node/dfw3/isis
#  dfw4:
#    - proxies/dfw4
#    - node/dfw4/isis
#    - node/dfw4/firewall
#  mci2:
#    - proxies/mci2
#    - node/mci2/isis
#  mci3:
#    - proxies/mci3
#    - node/mci3/isis
#  aus4:
#    - proxies/aus4
#    - node/aus4/firewall
#    - node/aus4/policy
#    - node/aus4/bgp
  '*':
    - firewall
    - policy
    - bgp
    - netdb
