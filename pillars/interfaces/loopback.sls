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

  AUS4:
    dum23:
      address:
        "23.181.64.235/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: aus4-lo1.sin.as36198.net

  DFW2:
    dum10:
      address: 
        "10.172.16.66/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::224/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp

    dum224:
      address: 
        "23.181.64.224/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw2-lo1.dfw.as36198.net
        "2620:136:a009:af00::224/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw2-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

  DFW3:
    dum10:
      address: 
        "10.172.16.67/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::231/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp

    dum231:
      address: 
        "23.181.64.231/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw3-lo1.dfw.as36198.net
        "2620:136:a009:af00::231/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw3-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

  DFW4:
    dum172:
      address: 
        "10.172.16.86/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::227/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp
      description: iBGP Loopbacks

    dum227:
      address: 
        "23.181.64.227/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw4-lo1.dfw.as36198.net
        "2620:136:a009:af00::227/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: dfw4-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL
      description: Public Loopbacks

    dum200:
      address: 
        "172.16.64.4/32":
          meta:
            role:
              - ipv4_address
              - loopback
      description: IPSEC and MT Loopbacks

  MCI2:
    dum10:
      address: 
        "10.172.16.81/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::228/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp

    dum228:
      address: 
        "23.181.64.228/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: mci2-lo1.dfw.as36198.net
        "2620:136:a009:af00::228/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: mci2-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

  MCI3:
    dum172:
      address: 
        "10.172.16.85/32":
          meta:
            role:
              - ipv4_address
              - znsl_private
              - loopback
              - ipv4_bgp
        "fd00:136:a009:af00::229/128":
          meta:
            role:
              - ipv6_address
              - znsl_private
              - loopback
              - ipv6_bgp
      description: iBGP and ZNSL Loopbacks

    dum229:
      address: 
        "23.181.64.229/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: mci2-lo1.dfw.as36198.net
        "2620:136:a009:af00::229/128":
          meta:
            role:
              - ipv6_address
              - znsl_public
              - loopback
            dns:
              ptr: mci2-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
          ipv6: 6-LOOPBACK-LOCAL

    dum230:
      address: 
        "23.181.64.230/32":
          meta:
            role:
              - ipv4_address
              - znsl_public
              - loopback
            dns:
              ptr: mci2-lo1.dfw.as36198.net
      firewall:
        local:
          ipv4: LOOPBACK-LOCAL
