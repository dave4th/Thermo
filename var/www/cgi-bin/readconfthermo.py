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
TestoPagina="Leggi Configurazione NoSQL db REDIS"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writeconfthermo.py"

ConfigNow=mjl.ReadJsonFile(ConfigFile)

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
print ("Ho lasciato la possibilita` di lasciare vuota la password","<hr/>","<br/>")

# Estraggo i valori della configurazione redis
ConfigNow = mjl.SearchValueJsonVar(ConfigNow,"redis")


print (mhl.MyActionForm(WriteFile,"POST"))

print ("<table>")

# Cerco nell'array il valore
for i in range(len(ConfigNow)):
	if "hostname" == (ConfigNow[i]["name"]):
		# Appoggio a variabile
		KeyRead = ConfigNow[i]["value"]
print ("<tr>")
print ("<td>")
print ("Hostname: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("hostname",KeyRead,"40","required",""))
print ("</td>")
print ("</tr>")

# Cerco nell'array il valore
for i in range(len(ConfigNow)):
	if "port" == (ConfigNow[i]["name"]):
		# Appoggio a variabile
		KeyRead = ConfigNow[i]["value"]
print ("<tr>")
print ("<td>")
print ("Port: ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("port",KeyRead,"6","6","0","32767","1","required",""))
print ("</td>")
print ("</tr>")

# Cerco nell'array il valore
for i in range(len(ConfigNow)):
	if "db" == (ConfigNow[i]["name"]):
		# Appoggio a variabile
		KeyRead = ConfigNow[i]["value"]
print ("<tr>")
print ("<td>")
print ("db (database): ")
print ("</td>")
print ("<td>")
print (mhl.MyNumberForm("db",KeyRead,"2","2","0","99","1","required",""))
print ("</td>")
print ("</tr>")

# Cerco nell'array il valore
for i in range(len(ConfigNow)):
	if "password" == (ConfigNow[i]["name"]):
		# Appoggio a variabile
		KeyRead = ConfigNow[i]["value"]
print ("<tr>")
print ("<td>")
print ("Password: ")
print ("</td>")
print ("<td>")
print (mhl.MyPasswordForm("password","password",""))	# le due "" ci sono perche` non e` obbligatoria
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td colspan=\"4\">")
print ("<hr/>")
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("</td>")
print ("<td>")
print (mhl.MyButtonForm("submit","Submit"))
print ("</td>")
print ("</tr>")

print ("</table>")



# End form
print (mhl.MyEndForm())

# End web page
print (mhl.MyHtmlBottom())