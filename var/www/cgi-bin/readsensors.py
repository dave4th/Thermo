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

import redis,os # Questa volta servira` anche os ?

# Parametri generali
TestoPagina="Configurazione sensori di temperatura"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writesensors.py"
# Redis "key"
RedisKey = "sensore:temperatura"
# 1 wire
Dir1w = "/sys/bus/w1/devices/"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Cerco i sensori
List1wire = os.listdir(Dir1w)
List1wire.remove("w1_bus_master1")

# Genero le chiavi se non esistono
for i in List1wire:
    if not MyDB.exists(RedisKey+":"+i):
        MyDB.set(RedisKey+":"+i,"Sensore"+i)

# Elimino quelle che non esistono piu`
for i in MyDB.keys(RedisKey+":*"):
    Esiste=""
    for j in List1wire:
        if flt.Decode(i) == RedisKey+":"+j:
            Esiste="True"
    if not Esiste:
        MyDB.delete(i)

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
Questo cerca le sonde di temperatura, genera automaticamente le chiavi redis, eliminando eventuali sonde che non sono piu` collegate.
<br/>
L'inserimento e` possibile per la sola descrizione, che servira` al riconoscimento del sensore, nel caso ve ne fosse piu` di uno collegato.
<br/>
<br/>
<i>Inserire una descrizione di riconoscimento, la piu` breve possibile.</i>
<br/>
<br/>
<b>Ricorda di riconfigurare il PID ed eliminare/archiviare "temperature.csv" fer forzare la riscrittura dell'intestazione.</b>
<hr/>
<br/>
""")

# Inizio del form
print (mhl.MyActionForm(WriteFile,"POST"))

print ("<table>")

# Questa volta ho tante chiavi ..
for i in List1wire:
    # La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
    print ("<tr>")
    print ("<td>")
    print ("Key: ")
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm("key",i,"40","required","readonly"))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("Descrizione sensore: ")
    print ("</td>")
    print ("<td>")
    print (mhl.MyTextForm(RedisKey+":"+i,flt.Decode(MyDB.get(RedisKey+":"+i)),"40","required",""))
    print ("</td>")
    print ("</tr>")
    
    print ("<tr>")
    print ("<td>")
    print ("")
    print ("</td>")
    print ("<td>")
    print ("<hr/>")
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
print ("<td colspan=\"2\">")
print (mhl.MyButtonForm("submit","Submit"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())

# End web page
print (mhl.MyHtmlBottom())