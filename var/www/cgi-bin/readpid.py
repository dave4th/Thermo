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
TestoPagina="Configurazione PID"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writepid.py"
# Redis "key"
RedisKey = "thermo:pid"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
if not MyDB.exists(RedisKey):
    MyDB.hmset(RedisKey,{"freqcheck":5,"sensor":"bella domanda","out":11,"tempadd":0,"tempsub":0})

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
Non ho rinominato i campi e non sono stato a riordinare le voci.<br/>
<ul>
    <li>"freqcheck"
        <ul>
            <li>Il valore e` in minuti
            </li>
            <li>Corrisponde alla frequenza di aggiornamento dell'uscita di comando
            </li>
            <li>E` il tempo fra un controllo temperatura ed il successivo
            </li>
        </ul>
    </li>
    <li>"tempadd"
        <ul>
            <li>Il valore e` in gradi
            </li>
            <li>Corrisponde alla maggiorazione della temperatura positiva
            </li>
            <li>Serve per riscaldare di "n,n" gradi in piu` della soglia preimpostata
            </li>
        </ul>
    </li>
    <li>"tempsub"
        <ul>
            <li>Il valore e` in gradi
            </li>
            <li>Corrisponde alla sottrazione di temperatura negativa
            </li>
            <li>Serve per attendere che il riscaldamento si attivi "n,n" gradi sotto alla soglia preimpostata
            </li>
        </ul>
    </li>
    <li>"sensor"
        <ul>
            <li>Sonda di temperatura
            </li>
            <li>Sonda di riferimento per l'accensione/spegnimento del riscaldamento
            </li>
            <li>E` necessario selezionare una fra le sonde collegate (Vedi 'readsensors')
            </li>
            <li>Se e` cambiata: <b>ricorda di eliminare/archiviare "temperature.csv" fer forzare la riscrittura dell'intestazione.</b>
            </li>
        </ul>
    </li>
    <li>"out"
        <ul>
            <li>Uscita termostato
            </li>
            <li>Pin di collegamento del rele` di uscita per comando riscaldamento
            </li>
            <li>Questo dipendera` dal programma, nel nostro caso il pin 11 del connettore (GPIO 17).
            </li>
        </ul>
    </li>
</ul>
<hr/>
<br/>
""")

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
    print ("Nome \"",flt.Decode(i),"\": ",sep="")
    print ("</td>")
    print ("<td>")
    if flt.Decode(i) == "freqcheck":
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"2","2","1","60","1","required",""))
    elif flt.Decode(i) == "out":
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"2","2","11","22","1","required",""))
    elif flt.Decode(i) == "sensor":
        Values=[]
        for j in MyDB.keys("sensore:temperatura:*"):
            Sensore = MyDB.get(flt.Decode(j))
            Values.append(flt.Decode(Sensore))
        #Values = MyDB.keys("sensore:temperatura:*")
        Selected = flt.Decode(MyDB.hget(RedisKey,"sensor"))
        print (mhl.MyDropDown(flt.Decode(i),Values,Selected))
    else:
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"1","1","0","1","0.1","required",""))
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