#/bin/bash

sudo /etc/init.d/ntp stop
#until ping -nq -c3 8.8.8.8; do
#   echo "Waiting for network..."
#done
#If ping is blocked
sleep 5
sudo ntpdate -s time.nist.gov
sudo /etc/init.d/ntp start

cd /home/pi/pinchon
source ../ENV/bin/activate
./serve.py &
./user.py &
./hose.py &
./fswebcam.sh
./fswebcam.sh
./fswebcam.sh

