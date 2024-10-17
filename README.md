# Fax-O-Tron

This repository contains files that will allow you to configure asterisk to recieve faxes, and print them out on a thermal printer. (Specifically the Pipsta/AP1400 printers, if you want to use this code with a standard ESC/POS printer, make an issue and I'll fix the code! )

There is also an install script provided to help you install and configure a working system.

The config assumes a few things that you may wish to change:
 - That the python modules required by the script are installed for the user running asterisk
 - That you want the fax images stored in /tmp/faxes
 - And finally, that you want a preconfigured PJSIP extention so that you can dial into the fax server locally.

If you want to be able to call into the server from PSTN you will need to configure a trunk in pjsip.conf.

Instructions for Andrews & Arnold are [here](https://support.aa.net.uk/VoIP_Phones_-_Asterisk)

Please read through `extensions.conf` and `pjsip.conf` fully, as there will be sections you wish to change!

To install, install asterisk from source, then run `install.sh`

## Installing Asterisk
[Read on Asterisk Docs](https://docs.asterisk.org/Getting-Started/Installing-Asterisk/Installing-Asterisk-From-Source/Building-and-Installing-Asterisk/)
