#PyBelt
####The hackers tool belt

PyBelt is a open source, hackers multi-tool much like a Gerber, it can be used for multiple purposes. No it does not come with a screw driver. but it does come with a port scanner! No it does not come with a knife, but it does come with a SQLi error based scanner! No it does not come with a can opener, it does however, come with a Dork Checker!
Why use PyBelt? Well for one, it's written in Python, everybody likes Python. For two, you have multiple tools now at your finger tips, SQLi scanning, Dork checking, and port scanning all available in a free range quick motion with simple flags. 

##ScreenShots
SQL Injection scanning made easy, just provide a URL and watch it work
![sqli](https://s23.postimg.org/3y1ljjl57/sqli_scan.png)

Dork checker, have some Dorks you're not sure of? Go ahead and run the Dork check with the Dork as an argument, it will pull 100 URLs and give you success rate for the Dork
![dork](https://s23.postimg.org/ut71kpcqz/dork_scan.png)

Simple port scanning, provide a host to scan and find the open ports to forward too
![port](https://s23.postimg.org/9xpcn75xn/port_scan.png)

##Usage

###Installation
You can either clone the repository 
`git clone https://github.com/ekultek/pybelt.git`
or download the latest release as a zip/tar ball [here](https://github.com/Ekultek/PyBelt/releases/tag/1.0)


Once you have the program installed cd into the directory and run the following command:
`pip install -r requirements.txt`
This will install all of the programs needed libraries and should be able to be run from there.
 
###Functionality
`python pybelt.py -p 127.0.0.1` Will run a port scan on your local host

`python pybelt.py -s http://example.com/php?id=2` Will run a SQLi scan on the given URL

`python pybelt.py -d idea?id=55` Will run a Dork check on the given Google Dork

##Misc info you probably don't care about
 
###License
This program is licensed under the MIT license, you can the license in the DOCS folder

###Current version
This program is currently in version 1.0, first release, this will be updated as the program grows

