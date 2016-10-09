#!/usr/bin/env python3

"""
My Json Library

Per ora la chiamo cosi` perche` la uso per i files json

Aggiornamenti: Sat 19 Mar 2016 08:32:13 AM CET

"""

import os,json,time


# Legge un file json, ritenta se non riesce, esce se non esiste
def ReadJsonFile(JsonFile):
	if os.path.exists(JsonFile):
		try:
			with open(JsonFile) as JsonFileOpen:
				JsonFileRead = json.load(JsonFileOpen)
				JsonFileOpen.close()
		except IOError:
			print ("Errore di I/O in lettura", JsonFile)
		except ValueError:
			print ("Errore dati", JsonFile," ritento ..")
			time.sleep(3)
			JsonFileRead = ReadJsonFile(JsonFile)	# Richiama se stessa
		else:
			return JsonFileRead
	else:
		print ("Arresto programma: manca il file", JsonFile)
		exit()

# Scrive un file json
def WriteJsonFile(JsonFileIn,JsonFileOut):
	with open(JsonFileOut, "w") as outfile:
		json.dump(JsonFileIn, outfile, indent=4)
		outfile.close()

# Cerca nella variabile Json, il valore di un "nome" specificato, restituisce il valore.
def SearchValueJsonVar(JsonVar,SearchName):
	for i in range(len(JsonVar)):
		if SearchName == JsonVar[i]["name"]:
			return JsonVar[i]["value"]

# Serve per cercare il risultato di un risultato
# utilizza la funzione SearchValueJsonVar(JsonVar,SearchName)
# Cerca il nome cha ha un valore array nella variabile Json,
# poi cerca il nome nell'array, restituisce il valore.
def SearchValue2JsonVar(JsonVar,SearchName1,SearchName2):
	for i in range(len(JsonVar)):
		if SearchName1 == JsonVar[i]["name"]:
			JsonVar2 = JsonVar[i]["value"]
			Results = SearchValueJsonVar(JsonVar2,SearchName2)
			return Results
