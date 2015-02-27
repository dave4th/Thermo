#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguendo il rispettivo "write*.py"

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie Json, Html
import mjl, mhl

# Parametri generali
# Ci provo, ma ogniuno avra` di sicuro le sue differenze
TestoPagina="Scrive configurazione NoSQL db REDIS"
ConfigFile="../conf/thermo.json"
#WriteFile="/cgi-bin/writeconfthermo.py"

ConfigNow=mjl.ReadJsonFile(ConfigFile)

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

print ("<h1>","<center>",TestoPagina,"</center>","</h1>","<hr/>","<br/>")

# Estraggo i valori della configurazione redis
ConfigNow = mjl.SearchValueJsonVar(ConfigNow,"redis")


form=cgi.FieldStorage()

# Praticamente il controllo di presenza nella form serve solo al campo "password"
# perche` ho lasciato al possibilita` che sia vuoto (nessuna password)
Error = ""
for i in range(len(ConfigNow)):
	if ConfigNow[i]["name"] not in form:
		if ConfigNow[i]["name"] == "password":
			ConfigNow[i]["value"] = ""
		else:
			print("<br/>Errore:", ConfigNow[i]["name"])
			Error = ConfigNow[i]["name"]
	else:
		ConfigNow[i]["value"] = cgi.escape(form[ConfigNow[i]["name"]].value)

if Error == "":
	ConfigNew=mjl.ReadJsonFile(ConfigFile)
	# Mi serve il puntatore a "value", e non ho trovato/pensati di meglio
	# Devo scrivere il valore solo alla parte "value" di "redis"
	for i in range(len(ConfigNew)):
		if "redis" == ConfigNew[i]["name"]:
			ConfigNew[i]["value"] = ConfigNow
	# Scrivo qualcosa nella pagina per conferma dell'operazione, ma eseguo anche la scrittura del file
	print("Error:",mjl.WriteJsonFile(ConfigNew,ConfigFile))
else:
	# Teoricamente non saranno MAI errori, dovrebbero essere gia` stati eliminati a monte
	print("<h2>Errore</h2>")
	print("<p>",Error,"</p>")

# End web page
print (mhl.MyHtmlBottom())