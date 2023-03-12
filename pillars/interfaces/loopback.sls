#!jinja|yaml

{#

#}

znsl_loopback:
  SIN1:
    dum23:
      address:
        "23.181.64.233/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: sin1-lo1.sin.as36198.net
        "23.181.64.234/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: sin1-lo2.sin.as36198.net
   
  SIN2:
    dum10:
      address: 
        "10.172.16.236/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::236/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp
    dum236:
      address: 
        "23.181.64.236/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: sin2-lo1.sin.as36198.net
        "2620:136:a009:af00::236/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: sin2-lo1.sin.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

  SIN3:
    dum10:
      address: 
        "10.172.16.237/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::237/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp
    dum237:
      address: 
        "23.181.64.237/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: sin3-lo1.sin.as36198.net
        "2620:136:a009:af00::237/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: sin3-lo1.sin.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

  FRA1:
    dum172:
      address: 
        "10.172.16.87/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::225/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp

    dum225:
      address: 
        "23.181.64.225/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: fra1-lo1.fra.as36198.net
        "2620:136:a009:af00::225/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: fra1-lo1.fra.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

