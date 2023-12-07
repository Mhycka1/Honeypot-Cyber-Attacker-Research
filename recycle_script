#!/bin/bash
sudo /home/student/DIT_firewall_rules
# Get a list of containers with the specified format
containers=$(sudo lxc-ls)

valid_prefixes=("mp3_files" "mp4_files" "no_files" "text_files")

echo "RECYCLE SCRIPT STARTED"
echo "******************************************************"

for container in $containers; do

  # Extract the container name prefix (e.g., mp3_files, mp4_files, etc.)
  container_prefix=$(echo "$container" | cut -d '_' -f1,2)

  # Check if the prefix is in the list of valid prefixes
  if [[ " ${valid_prefixes[*]} " == *" $container_prefix "* ]]; then
    # Do whatever you need to do with these containers
    echo "Found a matching container: $container"

    scenario=$(echo $container | cut -d '_' -f1,2)
    ext_ip=$(echo $container | cut -d '_' -f3)
    cont_ip=$(sudo lxc-info -n $container -iH)
    net_mask=24
    port=$(sudo cat /home/student/data/ports/${ext_ip}_port.txt)
    echo "Processing container: $container"

    # Delete the iptables rules
    sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $ext_ip --jump DNAT --to-destination $cont_ip
    sudo iptables -w --table nat --delete POSTROUTING --source $cont_ip --destination 0.0.0.0/0 --jump SNAT --to-source $ext_ip
    sudo iptables -w --table nat --delete PREROUTING --source 0.0.0.0/0 --destination $ext_ip --protocol tcp --dport 22 --jump DNAT --to-destination 10.0.3.1:$port
    sudo ip addr delete $ext_ip/$net_mask brd + dev

    # Destroy the container
    sudo lxc-stop -n $container --kill
    sudo lxc-destroy -n $container

    # Deletes file with port number in it
    sudo rm /home/student/data/ports/${ext_ip}_port.txt
    echo "y"

    echo "Finished processing container: $container"
    echo "------------------------------------------------------"
  else
    echo "Not the desired container"
    echo "------------------------------------------------------"
  fi
done

sudo pkill -f node
echo "All forever processes killed"
