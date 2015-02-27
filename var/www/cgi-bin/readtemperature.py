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
TestoPagina="Configurazione temperature"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writetemperature.py"
# Redis "key"
RedisKey = "temperature:setpoint"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
if not MyDB.exists(RedisKey):
    MyDB.hmset(RedisKey,{"confort":19,"giorno":17,"notte":15,"antigelo":5,"manuale":18})

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("Ho lasciato la possibilita` di lasciare vuota la password","<hr/>","<br/>")

# Inizio del form
print (mhl.MyActionForm(WriteFile,"POST"))

print ("<table>")

# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td>")
print (mhl.MyTextForm("key",RedisKey,"40","required","readonly"))
print ("</td>")
print ("</tr>")

# Per ogni campo ... stampo il campo ed il suo valore. (la funzione "Decode()" serve per trasformare "bin->str")
for i in MyDB.hkeys(RedisKey):
    print ("<tr>")
    print ("<td>")
    print ("Temperatura ",flt.Decode(i),": ",sep="")
    print ("</td>")
    print ("<td>")
    print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"2","2","5","30","0.1","required",""))
    print ("</td>")
    print ("</tr>")

print ("<tr>")
print ("<td colspan=\"2\">")
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