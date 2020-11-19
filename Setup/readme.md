## Setup New Raspberry by:

1. Setup WIFI: copy wpa_supplicant to boot via sudo cp /home/surya/AWS/pi-0/Scripts/Setup/wpa_supplicant.conf /media/surya/boot
2. Enable SSH: copy ssh empty file or touch ssh
3. ssh-copy-id pi@pi-0.local && ssh-add ~/.ssh/id_pi
4. Use VNC to set locale and raspi-config
5. sudo apt update && sudo apt install neovim
6. Install syncthing: https://apt.syncthing.net/ sudo systemctl enable syncthing@pi.service
7. sudo -H pip3 install -r /home/pi/AWS/Scripts/Setup/requirements3.txt && sudo -H pip install -r /home/pi/AWS/Scripts/Setup/requirements2.txt
8. Create Backup

## Restore Raspberry:

1. sudo vim /etc/hostname
2. sudo vim /etc/hosts
3. sudo rm -rfv ~/.config/syncthing/
4. sudo cp /home/pi/Setup/config.txt /boot
5. sudo cp /home/pi/Setup/rc.local /etc
6. sudo cp /home/pi/Setup/crontab /etc
7. sudo i2cdetect -y 1
8. sudo apt-get -y remove fake-hwclock && sudo update-rc.d -f fake-hwclock remove && sudo systemctl disable fake-hwclock
9. sudo cp /home/pi/Setup/hwclock-set /lib/udev
10. sudo hwclock -w && sudo hwclock -r
