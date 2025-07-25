# ChromeOS-VPN
This is a simple VPN for ChromeOS and ChromeOS Flex to install this you will need a few things.

1. You need linux terminal beta enabled (for older computers that don't support it I managed to bypass by turning on legacy boot support and if that doesn't work try putting it first on boot priority)

2. You will need chromeos autostart repository (https://github.com/supechicken/ChromeOS-AutoStart)

3. You will need to turn on developer mode for extensions

4. You will finally need this github repository

# How to setup VPN
1. Download this GitHub repository as a ZIP. Click the green Code button above → select Download ZIP and unzip the folder

2. Move the folder into your Linux container. Open the ChromeOS Files app → Right-click the folder → Select Move to Linux

3. mv ChromeOS-VPN-main ~/ChromeOS-VPN

5. cd ~/ChromeOS-VPN

6. Then install openvpn:
sudo apt update
sudo apt install openvpn

7. Add the autostart to extensions

8. Make sure autostart_test.sh and VPN.py are excutible and if not make them excutible

9. Use this command to turn it on bash ~/ChromeOS-VPN/autostart_test.sh

10. Add a new entry in the extension and select developer mode and paste in sleep 10 && bash ~/ChromeOS-VPN/autostart_test.sh

11. Save that entry and configure a bash profile using:
nano ~/.bash_profile
or
vim ~/.bash_profile

12. Paste in this:
if [ ! -f /tmp/vpn_autostart.log ]; then
    python3 ~/ChromeOS-VPN/VPN.py start ~/ChromeOS-VPN/dummy.ovpn >> /tmp/vpn_autostart.log 2>&1
fi

13. Restart your computer

14. To test that it is working paste in this
cat /tmp/vpn_autostart.log

# Tips & Notes
You can customize the VPN config by replacing dummy.ovpn with your own .ovpn file.

Make sure VPN.py uses shutil.which("openvpn") to dynamically find the binary (already done).

Logs are stored at /tmp/vpn_autostart.log for debugging VPN launch behavior.

For legacy devices, a delay (sleep 10) before autostart helps ensure the Linux container is ready.

You can verify that your tunnel is active by running:
ps aux | grep openvpn
