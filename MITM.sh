#!/bin/bash
if [ "$#" -ne 4 ]
then
echo "Usage: container name & external IP"
exit 1
fi

# alter this so that the port is parameter

containername=$1
externalip=$2
date=$3
port_num=$4
containerip=`sudo lxc-info -n $containername -iH`

#sudo ip netns exec ${containername} sysctl -w net.ipv4.ip_forward=1
#ext_if=eth0
#sudo ip netns exec ${containername} ip addr add ${externalip}/32 dev ${ext_if}

sudo sysctl -w net.ipv4.conf.all.route_localnet=1

sudo ip addr add $2/24 brd + dev eth1

sudo iptables --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $externalip --jump DNAT --to-destination "$containerip"

#sudo iptables -t nat -A PREROUTING -p tcp --dport 22 -d ${externalip} -j DNAT --to-destination ${containerip}:22

sudo iptables --table nat --insert POSTROUTING --source "$containerip" --destination 0.0.0.0/0 --jump SNAT --to-source $externalip
sudo iptables --table nat --insert PREROUTING --source 0.0.0.0/0 --destination $externalip --protocol tcp --dport 22 --jump DNAT --to-destination 10.0.3.1:$port_num

sleep 10
sudo forever -a -l /home/student/data/logs/{$date}_{$containername} start /home/student/MITM/mitm.js -n $containername -i "$containerip" -p $port_num --auto-access --auto-access-fixed 1 --debug --mitm-ip 10.0.3.1
