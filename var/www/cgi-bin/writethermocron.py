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
TestoPagina="Programmazione settimanale"
ConfigFile="../conf/thermo.json"
#WriteFile="/cgi-bin/writethermocron.py"
WeekDays=["lunedi","martedi","mercoledi","giovedi","venerdi","sabato","domenica"]
# Redis "key"
RedisKey = "temperature:cron"

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

for i in WeekDays:       # giorni. per tutti i giorni ..
    for j in range(24):
        if RedisKey+":"+str(i)+str(j) not in form:
            print ("<h3>Manca il valore: </h3>",RedisKey+":"+str(i)+str(j))
        else:
            MyDB.hset(RedisKey+":"+str(i),str(j),cgi.escape(form[RedisKey+":"+str(i)+str(j)].value))


print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
for i in WeekDays:       # giorni. per tutti i giorni ..
    for j in range(24):
        print ("<tr>")
        print ("<td>")
        print (RedisKey+":"+str(i),str(j))
        print ("</td>")
        print ("<td>")
        print (MyDB.hget(RedisKey+":"+str(i),str(j)))
        print ("</td>")
        print ("</tr>")
print ("</table>")


# End web page
print (mhl.MyHtmlBottom())