: '
Move config files and python script into correct folders!
'
echo -e "exit the script NOW by pressing Ctrl-C if you do not want your asterisk config to be erased by this script!!!!!!!!!"
read 
echo "removing old config"
rm /etc/asterisk/extensions.conf
rm /etc/asterisk/pjsip.conf
rm /etc/asterisk/resfax.conf
echo "copying new config"
cp asterisk-configs/* /etc/asterisk/
echo "copying print script"
cp imageprinter.py /opt/faxotron/imageprinter.py
cp pipsta_constants.py /opt/faxotron/pipsta_constants.py
echo "installing python modules"
pip3 install python-escpos pillow bitarray