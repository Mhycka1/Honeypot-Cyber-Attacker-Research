#!/bin/bash
#sudo ./DIT_firewall_rules

ips=( "128.8.238.199" "128.8.238.31" "128.8.238.50" "128.8.238.180")
ips=( $(shuf -e "${ips[@]}"))
scenarios=( "mp4_files" "mp3_files" "text_files" "no_files" )
ports=( "5000" "5184" "5660" "5713" )
ports=( $(shuf -e "${ports[@]}"))

sudo sysctl -w net.ipv4.conf.all.route_localnet=1
sudo sysctl -w net.ipv4.ip_forward=1

#  creates a base template

# checks if the template container isn't created
# if not it gets created and everything relevant
# is created inside it
if  ! sudo lxc-ls | grep -q "template" ;
then
  sudo lxc-create -n template -t download -- -d ubuntu -r focal -a amd64
  sudo lxc-start -n template


  # Installs ssh in container
  sudo lxc-attach -n template -- bash -c "sudo apt-get update"
  sleep 10
  sudo lxc-attach -n template -- bash -c "sudo apt-get install openssh-server -y"
  sleep 10
  sudo lxc-attach -n template -- bash -c "sudo systemctl enable ssh --now"
  # allow root ssh
  #sudo lxc-attach -n template -- bash -c "echo 'PermitRootLogin yes' >> /etc/ssh/sshd_config"
  #sudo lxc-attach -n template -- bash -c "systemctl restart sshd"

  sudo lxc-stop -n template

  # Create configuration templates #

  LENGTH=4
  for ((j = 0 ; j < $LENGTH; j++));
  do
          scenario=${scenarios[$j]}
          n="template_${scenario}"


          # Creates a copy of the base tempate
          sudo lxc-copy -n template -N $n
          sleep 10;

    #Grab the correct directory based on the scenario and
    #copy it into the template

    correct_directory=$(echo "$scenario" | cut -d '_' -f1)

    sudo cp -r /home/student/$correct_directory /var/lib/lxc/$n/rootfs/home

          sudo lxc-stop -n $n
  done

  # Calls scheduling script within this if
  # statement so it will only be called once
  # and just run forever in theor

fi

LENGTH=4

# Creates the actual honeypots #
for ((j = 0 ; j < $LENGTH; j++));
do
  #shuffles the scenarios everytime so it's not guranteed which configuration it gets
  scenarios=( $(shuf -e "${scenarios[@]}") )
        ext_ip=${ips[$j]}
        scenario=${scenarios[$j]}
        template="template_${scenario}"
        n="${scenario}_${ext_ip}" # name of the honeypot being deployed
        mask=24
        date=$(date "+%F-%H-%M-%S")

  # Picks one of the 4 port numbers
  port_num=${ports[$j]}

  echo "__________________________"
  echo "this is your external ip for this honeypot: $ext_ip"
  echo "--------------------------"

        # Copie over the template and  starts it
        sudo lxc-copy -n $template -N $n
        sudo lxc-start -n $n

        sudo sleep 10

        container_ip=$(sudo lxc-info -n $n -iH)
        echo "container: $n, container_ip: $container_ip, external_ip: $ext_ip"

  # calls the MITM script to set up the server and the iptables rules
  /home/student/MITM_script "$n" "$ext_ip" "$date" "$port_num"

  #changes honeypot configs so only one attacker can come in
  echo "root        hard    maxsyslogins            1" >> /var/lib/lxc/$n/rootfs/etc/security/limits.conf
  echo "*        hard    maxsyslogins           1" >> /var/lib/lxc/$n/rootfs/etc/security/limits.conf

  # create the file with the port number in it
  sudo touch /home/student/data/ports/${ext_ip}_port.txt
  sudo echo "$port_num" | sudo tee /home/student/data/ports/${ext_ip}_port.txt
done
