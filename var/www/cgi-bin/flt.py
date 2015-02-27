#!/usr/bin/env python3
"""
Function Library Thermo -> Redis

Libreria
Funzioni
Thermo

Conterra` funzioni specifiche, ma anche quelle generali,
per ora ho separato quelle della gestione json file e pagine html,
tutte le altre funzioni pensavo di metterle qua.
Appunto: pensavo ..  e invece ..

"""

import redis,os,socket

# Le mie librerie Json
import mjl

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
		print ("Errore, manca il file", Filename)
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

