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
WriteFile="/cgi-bin/writegraph.py"
# Redis "key"
RedisKey = "thermo:graph"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
if not MyDB.exists(RedisKey):
    MyDB.hmset(RedisKey,{"freqcheck":5,"outtemp":21})

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
            <li>Corrisponde alla frequenza di campionamento delle temperature
            </li>
            <li>E` il tempo fra una memorizzazione temperatura ed il successivo
            </li>
        </ul>
    </li>
    <li>"outtemp"
        <ul>
            <li>Valore in gradi centigradi
            </li>
            <li>Temperatura assegnata alla rappresentazione del comando uscita nel grafico delle temperature
            </li>
            <li>Puo` essere un qualsiasi valore, meglio se diverso da uno qualsiasi dei set poin impostato.
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
    elif flt.Decode(i) == "outtemp":
        print (mhl.MyNumberForm(flt.Decode(i),flt.Decode(MyDB.hget(RedisKey,i)),"2","2","5","30","1","required",""))
    else:
        print ("Qualcosa e` andato storto")
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