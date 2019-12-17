# PKN_Dance
V2 Dance Floor

PKNv2 dance floor (orriginally constructed for Nick Koshnick's 40th birthday party in 2019) 
uses three components.  
- gLEDiator for high level graphics
- a service that converts artnet_to_opc, maintained in this repository
- fadecandy opc software that couples with fadecandy hardware controlers in the four quadrants of the board.  The only part that we manage here is the configeration files. 

# gLEDiator:

Install V2.0.3 from here (or elsewhere)
https://oneguyoneblog.com/download/glediator-v2-0-3/

(install java JRE on mac)[https://apple.stackexchange.com/questions/372744/cannot-install-jdk-13-01-on-catalina]  Java 13 seems to work

In `dist/` folder run
`java -jar Glediator_V2.jar`

# pkn_artnet_to_opc.py

This runs on python 2.  Yuk!
```py
conda create --name py2 python=2.7
conda activate py2
pip install twisted
```

# fadecandy server

project repo is here:
https://github.com/scanlime/fadecandy/

Has an (issue with 64bit mac OS catelina)[https://github.com/scanlime/fadecandy/issues/132] but modifying the make file for m64 seems to work.


