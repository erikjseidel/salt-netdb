base:
  sin1:
    - proxies/sin1
    - node/sin1/firewall
    - node/sin1/policy
    - node/sin1/bgp
  sin2:
    - proxies/sin2
    - node/sin2/isis
    - node/sin2/bgp
  sin3:
    - proxies/sin3
    - node/sin3/isis
    - node/sin3/bgp
  fra1:
    - proxies/fra1
    - node/fra1/isis
  '*':
    - interfaces/tunnels
    - interfaces/ethernet
    - interfaces/loopback
    - firewall
    - policy
    - isis
    - bgp
