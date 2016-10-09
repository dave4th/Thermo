# Thermo
Cronotermostato (derivato da [ThermoRed](https://github.com/raspibo/ThermoRed.git)).

Lo scopo e\` (era) realizzare sul Raspberry Pi un qualcosa di leggero e semplice,
che abbia un'interfaccia semplice (?) ed intuitiva (?) per il normale utilizzatore.

Contiene predisposizione per uso e configurazione della 
[centralina di messaggi e allarme](https://github.com/raspibo/CentRed.git).


## WebServer
Nginx

## CGI Script
Python

## Chart
http://dygraphs.com/

# Alcune note d'uso e installazione
http://www.raspibo.org/wiki/index.php/Thermo

# Appunti utili (?)
https://github.com/raspibo/Thermo/wiki


# Aggiornamenti
## 2016 10 06
Aggiunto invio temperatura alla centralina di livello 1 (https://github.com/raspibo/Livello1)
  apt-get install python3-pip
  pip-3.2 install paho-mqtt


MEMO:

Comandi usati per copia su repository git:
  cp -varpu --parents /etc/rc.local .
  cp -varpu --parents /etc/nginx/fcgiwrap.conf /etc/nginx/sites-available/thermo /etc/nginx/sites-enabled/thermo .
  cp -varpu --parents /var/www/ .
