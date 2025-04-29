# Wireshark Logger

### Hourly logs from Wireshark and Netstat output to .pcapng and text files

* **netstat.py:** saves netstat output to text file, runs solo doesn't depend on any 3rd party software except Windows netstat shell command.
* **tshark.py:** saves tshark output from 4 interfaces ( localhost, WiFi, ProtonVPN, ProtonVPN TUN), depends on woof.py and tshark.
* **woof.py:** saves tshark output from a single interface, uses tshark.
* **netstat.bat & tshark.bat:** script to run netstat.py and tshark.py, sets time of execution in title.

Example use: `tshark.bat <time to run in seconds, default 1hour(3600)>`

`tshark.bat 3600`

`netstat.bat`
