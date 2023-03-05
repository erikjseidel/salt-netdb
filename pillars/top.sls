base:
  sin1-nm:
    - proxies/sin1-nm
  sin1-proxy:
    - proxies/sin1-proxy
    - node/sin1/firewall
    - node/sin1/policy
    - node/sin1/bgp
  sin2-proxy:
    - proxies/sin2-proxy
    - node/sin2/isis
    - node/sin2/bgp
  sin3-proxy:
    - proxies/sin3-proxy
    - node/sin3/isis
    - node/sin3/bgp
  '*-proxy':
    - interfaces/tunnels
    - firewall
    - policy
    - isis
    - bgp
