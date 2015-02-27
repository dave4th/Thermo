#!/usr/bin/env python3

# Questo file legge il file di configurazione,
# trova e modifica il parametro eseguendo il rispettivo "write*.py"

# Serve per la parte di gestione html in python
import cgi
import cgitb

# Abilita gli errori al server web/http
cgitb.enable()

# Le mie librerie Json, Html, flt (Thermo(Redis))
import mjl, mhl, flt

import redis

# Parametri generali
TestoPagina="Configurazione sensori di temperatura"
ConfigFile="../conf/thermo.json"
#WriteFile="/cgi-bin/writesensors.py"
# Redis "key"
RedisKey = "sensore:temperatura"
# 1 wire
Dir1w = "/sys/bus/w1/devices/"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("......","<hr/>","<br/>")

form=cgi.FieldStorage()

for i in MyDB.keys(RedisKey+":*"):
    if flt.Decode(i) not in form:
        print ("<h3>Manca il valore: </h3>",i)
    else:
        MyDB.set(flt.Decode(i),cgi.escape(form[flt.Decode(i)].value))


print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
for i in MyDB.keys(RedisKey+":*"):
    print ("<tr>")
    print ("<td>")
    print (i)
    print ("</td>")
    print ("<td>")
    print (MyDB.get(flt.Decode(i)))
    print ("</td>")
    print ("</tr>")
print ("</table>")


# End web page
print (mhl.MyHtmlBottom())