base:
  '*':
    - bgp
#    - isis
#    - policy
    - firewall
    - tunnels
    - ethernet
    - loopback
  'sin*':
    - policy
  'G@cvars:iso':
    - isis
