#!/bin/bash
# configure the bot
python3 -m simplebot init deltahelp@disroot.org Francy82+
python3 -m simplebot -a deltahelp@disroot.org set_name UploaderFREE
python3 -m simplebot -a deltahelp@disroot.org set_avatar bot.jpeg
#Uploader Free
python3 -m simplebot -a deltahelp@disroot.org plugin --add ./bot.py
#Error al Desencriptar y Comandos
python3 -m simplebot -a deltahelp@disroot.org plugin --add ./derror.py

# add admin plugin
   # python3 -m simplebot -a deltahelp@disroot.org plugin --add ./admin.py
python3 -m simplebot -a deltahelp@disroot.org admin --add frankramiro.martinez@nauta.cu

# start the bot
python3 -m simplebot -a deltahelp@disroot.org serve
