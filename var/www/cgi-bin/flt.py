#!/usr/bin/env python3
"""
Function Library T w/ Redis

Libreria
Funzioni
T

Conterra` funzioni specifiche, ma anche quelle generali,
per ora ho separato quelle della gestione json file e pagine html,
tutte le altre funzioni pensavo di metterle qua.
Appunto: pensavo ..  e invece ..

Aggiornamenti: Sat 19 Mar 2016 08:30:53 AM CET
Aggiornamento: Sun 09 Oct 2016 10:33:55 AM CEST
"""

import redis,os,socket,time

# La mia libreria Json
import mjl

# MQTT (copio dall'esempio)
import sys
try:
    import paho.mqtt.publish as publish
except ImportError:
    # This part is only required to run the example from within the examples
    # directory when the module itself is not installed.
    #
    # If you have the module installed, just use "import paho.mqtt.publish"
    import os
    import inspect
    cmd_subfolder = os.path.realpath(os.path.abspath(os.path.join(os.path.split(inspect.getfile( inspect.currentframe() ))[0],"../src")))
    if cmd_subfolder not in sys.path:
        sys.path.insert(0, cmd_subfolder)
    import paho.mqtt.publish as publish


# Ho forse personalizzato troppo questa libreria/funzione,
# Purtroppo credo che la utilizzero` spesso, e mantenere il file di configurazione
# staccato sarebbe costato troppo.
def OpenDBFile(ConfigFile):
	# Leggo il file di configurazione
	ConfigNow=mjl.ReadJsonFile(ConfigFile)
	for i in range(len(ConfigNow)):
		if "redis" == ConfigNow[i]["name"]:
			ConfigNow = ConfigNow[i]["value"]
	DB = redis.StrictRedis(host=mjl.SearchValueJsonVar(ConfigNow,"hostname"), port=mjl.SearchValueJsonVar(ConfigNow,"port"), db=mjl.SearchValueJsonVar(ConfigNow,"db"), password=mjl.SearchValueJsonVar(ConfigNow,"password"))
	return DB

# Apre un database Redis con parametri
def OpenDB(Host,Port,Database,Password):
    DB = redis.StrictRedis(host=Host, port=Port, db=Database, password=Password)
    return DB

# Faccio una funzione per la decodifica bytes -> str
def Decode(TxT):
    return TxT.decode('unicode_escape')

# Decodifica una lista
def DecodeList(List):
    return [x.decode('unicode_escape') for x in List]

# Controlla se esiste un "field" di una "key" tipo "hash"
# e restituisce il contenuto, altrimenti restituisce 'none'
def CheckKeyHashField(DB,Hash,Field):
	FieldValue="none"
	if DB.hexists(Hash,Field):
		FieldValue=DB.hget(Hash,Field)
	return FieldValue

# Apre/legge un file e restituisce il contenuto
def ReadFile(Filename):
    if os.path.exists(Filename):
        FileTemp = open(Filename,"r")
        DataFile = FileTemp.read()
        FileTemp.close()
        return DataFile
    else:
        print ("Errore, manca il file", Filename)
        #exit()
        return "errore"

# Scrive un file
def WriteFileData(Filename,Dato):
	if not os.path.exists(Filename):
		FileTemp = open(Filename,"w")
		FileTemp.write(Dato)
		FileTemp.close()
	else:
		# Funzionano entrambe
		print ("Errore, il file \"{}\" esiste gia`!".format(Filename))
		#print ("Errore, il file \"%s\" esiste gia`!" % Filename)
		exit()

# Aggiunge dati ad un file, aprendolo e richiudendolo
def AddFileData(Filename,Dato):
	if os.path.exists(Filename):
		FileTemp = open(Filename,"a")
		FileTemp.write(Dato)
		FileTemp.close()
	else:
		print ("Errore, manca il file", Filename)
		exit()

# Controlla una connessione di rete
def NetCheck(Hostname,Port):
	s = socket.socket()
	try:
		s.connect((Hostname,Port))
	except socket.error as msg:
		print("Non ho trovato/non mi collego a %s:%d.\nIl messaggio d\'errore e`: %s" % (Hostname, Port, msg))
		return False
	else:
		return True

## Funzione invio avvisi al database (Redis) server dei messaggi
## E` presa da thermo, ma siccome qua e` uguale ... (ho deciso di metterla in libreria)
# database,messaggio,tipo,descrizione,valore,unita`dimisura,data
# DB,msg:{pc}:{id}:<data&ora>,<alert/alarm>,Descrizione,Valore,Unita` di misura,Data
def InviaAvviso(DB,MsgID,Type,Desc,Value,UM,Date):
    Hostname=Decode(DB.hget("redis:server:message","hostname"))
    Port=Decode(DB.hget("redis:server:message","port"))
    Database=Decode(DB.hget("redis:server:message","database"))
    Password=Decode(DB.hget("redis:server:message","password"))
    if NetCheck(Host,int(Port)):
        MyMsgDB = OpenDB(Hostname,Port,Database,Password)
        MyMsgDB.hmset(MsgID, {"type": Type, "desc": Desc, "value": Value, "um": UM, "date": Date})
    else:
        print ("Non posso inviare l\'avviso a \"%s:%d\".\n" % (Hostname,Port))

# Aiuto personalizzazione dei messagi di avviso per risparmiare qualche digitazione
# Data+ora [0], Data [1]
def AlertsID():
    MsgIDate=time.strftime("%Y%m%d%H%M%S",time.localtime())
    #MsgType="alert"
    MsgDate=time.strftime("%Y/%m/%d %H:%M:%S",time.localtime())
    return MsgIDate,MsgDate

## Funzione invio dati al broker MQTT (Mosquitto)
# Questa e` la definizione nella libreria paho-mqtt:
# def single(topic, payload=None, qos=0, retain=False, hostname="localhost",
#     port=1883, client_id="", keepalive=60, will=None, auth=None,
#     tls=None, protocol=paho.MQTTv311, transport="tcp"):
# Questa sarebbe la riga completa, al momento uso solo il topic ed il messaggio,
# il resto e` preso dalla configurazione inserita in redis:
#def InviaMqttData(Topic,Payload,QOS,Retain,Hostname,Port,CleintID,Keepalive,Will,Auth,TLS,Protocol,Transport):
# C'e` un problema, la definzione l'ho presa dalla "level1", dove DB era definito, qua, glielo devo passare !!!
def InviaMqttData(DB,Topic,Payload):
    Hostname=Decode(DB.hget("mqttbroker:server:message","hostname"))
    Port=int(Decode(DB.hget("mqttbroker:server:message","port")))
    User=Decode(DB.hget("mqttbroker:server:message","user")) 
    Password=Decode(DB.hget("mqttbroker:server:message","password"))
    if User == "" or Password == "":
        Auth= {'username':'none', 'password':'none'}
    else:
        Auth= { 'username' : User , 'password' : Password } # Questa e` da verificare ***
    if NetCheck(Hostname,Port):
        publish.single(Topic, Payload, hostname=Hostname, port=Port, auth=Auth)
    else:
        print ("Non posso trasmettere a \"%s:%s\".\n" % (Hostname,Port))
