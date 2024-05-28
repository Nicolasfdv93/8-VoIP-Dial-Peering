Project 8 – VoIP & Dial-Peering	- Devs Config

### ROUTERS ###

## ALL ROUTERS ##

En
Conf t
Int se0/3/0
No shut
Int se0/3/1
No shut
Int fa0/0
No shut
Exit

Enable password cisco
No ip domain lookup
Line console 0
Password cisco
Login
Exit
Service password-encryption
Ip domain-name cisco.net
Username admin password cisco
Crypto key generate rsa
1024
Line vty 0 15
Login local
Transport input ssh
Ip ssh version 2
Exit

## FIN ROUTER ##

En
Conf t
Hostname FIN-Router
Int fa0/0
No shut
Int se0/3/0
Ip address 10.10.10.5 255.255.255.252
Exit
Int se0/3/1
Ip address 10.10.10.1 255.255.255.252
Exit

//DHCP for Voice – Exclude Default GW for Voice 172.16.100.1

Int f0/0
Service dhcp
Ip dhcp excluded-address 172.16.100.1
Ip dhcp pool FIN-Voice 
Network 172.16.100.0 255.255.255.224
Default-router 172.16.100.1
Option 150 ip 172.16.100.1
Exit

//Inter-Vlan Routing & DHCP-helper (DHCP Server’s IP)

Int f0/0.10
Encapsulation dot1q 10
Ip address 192.168.100.1 255.255.255.224
Ip helper-address 192.168.100.130
Exit

Int f0/0.100
Encapsulation dot1q 100
Ip address 172.16.100.1 255.255.255.224
Exit

//OSPF Configuration

Router ospf 10
Auto-cost reference-bandwidth 1000000
Network 10.10.10.4 0.0.0.3 area 0
Network 10.10.10.0 0.0.0.3 area 0
Network 192.168.100.0 0.0.0.31 area 0
Network 172.16.100.0 0.0.0.31 area 0
Exit 

//VoIP Confguration & assignment of phone numbers

Telephony-service
Max-dn 20
Max-ephones 20
Ip source-address 172.16.100.1 port 2000
Auto assign 1 to 20
Exit

//Configure one for each VLAN existing

Ephone-dn 1
Number 101
Ephone-dn 2
Number 102
Ephone-dn 3
Number 103
Ephone-dn 4
Number 104
Ephone-dn 5
Number 105
Ephone-dn 6
Number 106
Ephone-dn 7
Number 107
Ephone-dn 8
Number 108
Ephone-dn 9
Number 109
Ephone-dn 10
Number 110

Exit
Do wr

// Dial Peering – keep in mind that the peering follows the
// pattern of the destination numbers (1xx, 2xx, 3xx, 4xx)
// Groups must match between dial-peering on each router.


// Peering-Voice FIN-HR
Dial-peer voice 1 voip
Destination-pattern 2..
Session target ipv4:10.10.10.2
Exit

//Peering-Voice FIN-ICT
Dial-peer voice 2 voip
Destination-pattern 4..
Session target ipv4:10.10.10.6
Exit

//Peering-Voice FIN-SALES
Dial-peer voice 3 voip
Destination-pattern 4..
Session target ipv4:10.10.10.10
Exit
Do wr

## HR ROUTER ##

En
Conf t
Hostname HR-Router

Int fa0/0
No shut
Int se0/3/1
Ip address 10.10.10.2 255.255.255.252
Clock rate 64000
Int se0/3/0
Ip address 10.10.10.9 255.255.255.252
Exit 

// Router as DHCP Server for Voice
// Exclude Default GW 172.16.100.33

Int f0/0
Service dhcp
Ip dhcp exclude-address 172.16.100.33
Ip dhcp pool HR-Voice 
Network 172.16.100.32 255.255.255.224
Default-router 172.16.100.33
Option 150 ip 172.16.100.33
Exit

// Inter-Vlan Routing & DHCP-helper (DHCP Server’s IP)
Int f0/0.20
Encapsulation dot1q 20
Ip address 192.168.100.33 255.255.255.224
Ip helper-address 192.168.100.130
Exit

Int f0/0.100
Encapsulation dot1q 100
Ip address 172.16.100.33 255.255.255.224
Exit


//OSPF
Router ospf 10
Auto-cost reference-bandwidth 1000000
Network 10.10.10.0 0.0.0.3 area 0
Network 10.10.10.8 0.0.0.3 area 0
Network 192.168.100.32 0.0.0.31 area 0
Network 172.16.100.32 0.0.0.31 area 0
Exit

//VoIP Confguration & assignment of phone numbers
Telephony-service
Max-dn 20
Max-ephones 20
Ip source-address 172.16.100.33 port 2000
Auto assign 1 to 20
Exit

Ephone-dn 1
Number 201
Ephone-dn 2
Number 202
Ephone-dn 3
Number 203
Ephone-dn 4
Number 204
Ephone-dn 5
Number 205
Ephone-dn 6
Number 206
Ephone-dn 7
Number 207
Ephone-dn 8
Number 208
Ephone-dn 9
Number 209
Ephone-dn 10
Number 210
Exit
Do wr

// Dial Peering – keep in mind that the peering follows the
// pattern of the destination numbers (1xx, 2xx, 3xx, 4xx)
// Groups must match between dial-peering on each router

//Peering-Voice HR-FIN -> Group 1
Dial-peer voice 1 voip
Destination-pattern 1..
Session target ipv4:10.10.10.1
Exit

//Peering-Voice HR-SALES -> Group 4
Dial-peer voice 4 voip
Destination-pattern 3..
Session target ipv4:10.10.10.10
Exit

//Peering-Voice HR-ICT -> Group 5
Dial-peer voice 5 voip
Destination-pattern 4..
Session target ipv4:10.10.10.6

Exit
Do wr

## SALES ROUTER ##

En
Conf t
Hostname SALES-Router

Int fa0/0
No shut
Int se0/3/0
Ip address 10.10.10.10 255.255.255.252
Clock rate 64000

Int se0/3/1
Ip address 10.10.10.13 255.255.255.252
Clock rate 64000
Exit

// DHCP for Voice – Exclude Default GW for Voice 172.16.100.65

Int f0/0
Service dhcp
Ip dhcp excluded-address 172.16.100.65
Ip dhcp pool SALES-Voice 
Network 172.16.100.64 255.255.255.224
Default-router 172.16.100.65
Option 150 ip 172.16.100.65
Exit

// Inter-Vlan Routing & DHCP-helper (DHCP Server’s IP)

Int f0/0.30
Encapsulation dot1q 30
Ip address 192.168.100.65 255.255.255.224
Ip helper-address 192.168.100.130
Exit
Int f0/0.100
Encapsulation dot1q 100
Ip address 172.16.100.65 255.255.255.224
Exit

//OSPF 
Router ospf 10
Auto-cost reference-bandwidth 1000000
Network 10.10.10.12 0.0.0.3 area 0
Network 10.10.10.8 0.0.0.3 area 0
Network 192.168.100.64 0.0.0.31 area 0
Network 172.16.100.64 0.0.0.31 area 0
Exit

//VoIP Confguration & assignment of phone numbers
Telephony-service
Max-dn 20
Max-ephones 20
Ip source-address 172.16.100.65 port 2000
Auto assign 1 to 20
Exit
Ephone-dn 1
Number 301
Ephone-dn 2
Number 302
Ephone-dn 3
Number 303
Ephone-dn 4
Number 304
Ephone-dn 5
Number 305
Ephone-dn 6
Number 306
Ephone-dn 7
Number 307
Ephone-dn 8
Number 308
Ephone-dn 9
Number 309
Ephone-dn 10
Number 310
Exit
Do wr

// Dial Peering – keep in mind that the peering follows the
// pattern of the destination numbers (1xx, 2xx, 3xx, 4xx)
// Groups must match between dial-peering on each router

// Peering-Voice SALES-FIN -> Group 3
Dial-peer voice 3 voip
Destination-pattern 1..
Session target ipv4:10.10.10.1
Exit

// Peering-Voice SALES-HR -> Group 4
Dial-peer voice 4 voip
Destination-pattern 2..
Session target ipv4:10.10.10.9
Exit

// Peering-Voice SALES-ICT -> Group 5
Dial-peer voice 5 voip
Destination-pattern 4..
Session target ipv4:10.10.10.14
Exit
Do wr

## ICT ROUTER ##

En
Conf t
Hostname ICT-ROUTER

Int fa0/0
No shut
Int fa0/1
No shut

Int se0/3/0
Ip address 10.10.10.6 255.255.255.252
Clock rate 64000
Exit

Int se0/3/1
Ip address 10.10.10.14 255.255.255.252
Exit

//DHCP for Voice – Exclude Default GW for Voice 172.16.100.97
Int f0/0
Service dhcp
Ip dhcp excluded-address 172.16.100.97
Ip dhcp pool ICT-Voice 
Network 172.16.100.96 255.255.255.224
Default-router 172.16.100.97
Option 150 ip 172.16.100.97
Exit

// Inter-Vlan Routing & DHCP-helper (DHCP Server’s IP)

Int f0/0.40
Encapsulation dot1q 40
Ip address 192.168.100.97 255.255.255.224
Ip helper-address 192.168.100.130
Exit
Int f0/0.100
Encapsulation dot1q 100
Ip address 172.16.100.97 255.255.255.224
Exit
Int f0/1.50
Encapsulation dot1q 50
Ip address 192.168.100.129 255.255.255.248
Exit

//OSPF
Router ospf 10
Auto-cost reference-bandwidth 1000000
Network 192.168.100.128 0.0.0.7 area 0
Network 192.168.100.96 0.0.0.31 area 0
Network 172.16.100.96 0.0.0.31 area 0
Network 10.10.10.4 0.0.0.3 area 0
Network 10.10.10.12 0.0.0.3 area 0
Exit 

//VoIP Confguration & assignment of phone numbers
Telephony-service
Max-dn 20
Max-ephones 20
Ip source-address 172.16.100.97 port 2000
Auto assign 1 to 20
Exit

Ephone-dn 1
Number 401
Ephone-dn 2
Number 402
Ephone-dn 3
Number 403
Ephone-dn 4
Number 404
Ephone-dn 5
Number 405
Ephone-dn 6
Number 406
Ephone-dn 7
Number 407
Ephone-dn 8
Number 408
Ephone-dn 9
Number 409
Ephone-dn 10
Number 410
Exit
Do wr

//Dial Peering – keep in mind that the peering follows the pattern of the destination numbers (1xx, 2xx, 3xx, 4xx)
//Peering-Voice ICT-FIN -> Group 2
Dial-peer voice 2 voip
Destination-pattern 1..
Session target ipv4:10.10.10.5
Exit

//Peering-Voice ICT-SALES -> Group 5
Dial-peer voice 5 voip
Destination-pattern 3..
Session target ipv4:10.10.10.13
Exit

//Peering-Voice to HR -> Group 6
Dial-peer voice 6 voip
Destination-pattern 2..
Session target ipv4:10.10.10.9
Exit
Do wr

### SWITCHES ###
## ALL SWITCHES ##

En
Conf t
Enable password cisco
No ip domain lookup
Banner motd !*! NO AUTHORIZED ACCES !*!
Line console 0
Password cisco
Login
Service password-encryption
Ip domain-name cisco.net
Username admin password cisco
Crypto key generate rsa
1024
Line vty 0 15
Login local
Transport input ssh
Ip ssh version 2

Vlan 10
Name FINANCE
Vlan 20
Name HR
Vlan 30
Name SALES
Vlan 40
Name ICT
Vlan 50
Name SSS
Vlan 100
Name Voice
Vlan 99
Name Native
Exit

Int g0/1
No shut
Switchport mode trunk
Switchport trunk native vlan 99
Exit

Int g0/2
Shut
Int ran fa0/1-10
Switchport mode access
Exit

Int ran fa0/11-24
Shut
exit
Do wr

## FIN-SW ##

En
Conf t
Hostname FIN-SW
Int ran fa0/1-10
Switchport access vlan 10
Switchport voice vlan 100
Exit
Do wr

## HR-SW ##
En
Conf t
Hostname HR-SW
Int ran fa0/1-10
Switchport access vlan 20
Switchport voice vlan 100
Exit 
Do wr

## SALES SW ##
En
Conf t
Hostname SALES-SW
Int ran fa0/1-10
No shut
Switchport access vlan 30
Switchport voice vlan 100
Exit 
Do wr

## ICT-SW ##
En
Conf t
Hostname ICT-SW
Int ran fa0/1-10
Switchport access vlan 40
Switchport voice vlan 100
Exit 
Do wr

## SSS-SW ##
En
Conf t
Hostname SSS-SW
Int ran fa0/1-10
Switchport access vlan 50
Switchport voice vlan 100
Exit 
Do wr

