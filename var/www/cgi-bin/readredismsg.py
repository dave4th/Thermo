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
TestoPagina="Configurazione server dei messaggi (Redis)"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writeredismsg.py"
# Redis "key"
RedisKey = "redis:server:message"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
if not MyDB.exists(RedisKey):
    MyDB.hmset(RedisKey,{"hostname":"nessuno","port":6379,"database":0,"password":""})

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("Non ho rinominato i campi e non sono stato a riordinare le voci.<hr/><br/>")


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
    print (flt.Decode(i),": ",sep="")
    print ("</td>")
    print ("<td>")
    if flt.Decode(i) == "hostname":
        print (mhl.MyTextForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"40","required",""))
    elif flt.Decode(i) == "port":
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"5","5","1","32767","1","required",""))
    elif flt.Decode(i) == "database":
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"2","2","0","99","1","required",""))
    else:
        print (mhl.MyPasswordForm("password","password",""))
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