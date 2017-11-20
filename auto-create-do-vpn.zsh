#!/bin/zsh
# region is one of nyc1 sfo1 ams2 sgp1 lon1 nyc3 ams3 fra1 tor1 sfo2 blr1
regions=( $( doctl compute region list | sed '1d' | cut -f1 -d' ' ))
function inArray
{
  local e
  for e in "${@:2}"; do 
    [[ "$e" == "$1" ]] && return 0;
  done
  return 1
}
function getRegion
{
echo "select region from the following: $regions "; read REGION
inArray $REGION $regions
if [ $? -eq 0 ]; then return $REGION
else echo incorrect region selection
  getRegion
fi
}

CLIENTNAME=`hostname`

vpn_name="proxtest${RANDOM}"
echo -ne "entername vpnname [$vpn_name]: "; read VPNNAME
if [ ! $VPNNAME ]; then VPNNAME=$vpn_name; fi
getRegion

echo creating droplet $vpn_name in region $REGION

doctl compute droplet create $VPNNAME\
  --size=512mb \
  --image=docker-16-04 \
  --region=$REGION \
  --ssh-keys="e3:14:8c:27:76:83:ba:82:55:d5:37:7a:22:fd:11:49" \
  --wait
IP=$(doctl compute droplet list | grep $vpn_name | awk '{print $3}')
OVPN_DATA="ovpn-$vpn_name"
echo """
docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_genconfig -u udp://$IP
docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn ovpn_initpki
docker run -v $OVPN_DATA:/etc/openvpn -d -p 1194:1194/udp --cap-add=NET_ADMIN kylemanna/openvpn
docker run -v $OVPN_DATA:/etc/openvpn --rm -it kylemanna/openvpn easyrsa build-client-full $CLIENTNAME nopass
docker run -v $OVPN_DATA:/etc/openvpn --rm kylemanna/openvpn ovpn_getclient $CLIENTNAME > $CLIENTNAME.ovpn
""" > setup-$vpn_name.sh
scp setup-$vpn_name.sh root@${IP}:
rm -v setup-$vpn_name.sh

echo -ne 'continue into shell for remote set [hit enter]'
read _
ssh -t root@$IP sh ./setup-$vpn_name.sh

config=./$CLIENTNAME-$vpn_name.ovpn
scp root@${IP}:$CLIENTNAME.ovpn $config
echo '+++++++++++++++++++++++++++++++++'
echo '******** ALL READY TO GO ********'
echo " ()()() USE THE FILE ()()()()"
echo " >>> $config <<< "
