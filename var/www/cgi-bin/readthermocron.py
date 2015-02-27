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
WriteFile="/cgi-bin/writethermocron.py"
WeekDays=["lunedi","martedi","mercoledi","giovedi","venerdi","sabato","domenica"]
# Redis "key"
RedisKey = "temperature:cron"

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esistono
for i in WeekDays:
    if not MyDB.exists(RedisKey+":"+i):
        for j in range(24):
            MyDB.hset(RedisKey+":"+i,j,"notte")


# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("""
#<ul>
#    <li>On = Acceso
#    </li>
#    <li>Off = Spento (funzionamento antigelo)
#    </li>
#    <li>Man = Manuale (funzionamento con temperatura manuale)
#    </li>
#</ul>
#<hr/>
#<br/>
#""")

# Inizio del form
print (mhl.MyActionForm(WriteFile,"POST"))

print ("<table>")

# La prima voce non e` modificabile ed e` la chiave Redis (solo visualizzazione)
print ("<tr>")
print ("<td>")
print ("Key: ")
print ("</td>")
print ("<td colspan=\"24\">")
print (mhl.MyTextForm("key",RedisKey,"40","required","readonly"))
print ("</td>")
print ("</tr>")

print ("<tr>")
#for i in MyDB.keys(RedisKey+":*"):       # giorni. per tutti i giorni ..
for i in WeekDays:       # giorni. per tutti i giorni ..
    print ("<tr>")
    print ("<td>")
    print ("Ora: ")
    print ("</td>")
    for j in range(24):
        print ("<td><center>")
        print (j)
        print ("</center></td>")
    print ("</tr>")
#    for k in MyDB.hkeys("temperature:setpoint"):     # per tutte le temperature // poi qua la sistemiamo
    for k in ["confort","giorno","notte","antigelo"]:     # per tutte le temperature // poi qua la sistemiamo
        print ("<tr>")
        print ("<td>")
        print ("Temperatura",k,":")
        print ("</td>")
        for l in range(24):
            print ("<td>")
            if flt.Decode(MyDB.hget(RedisKey+":"+i,l)) == k:
                Checked="checked"
            else:
                Checked=""
            print (mhl.MyRadioButton((RedisKey+":"+str(i)+str(l)),k,Checked))
            print ("</td>")
        print ("</tr>")
    #
    print ("<tr>")
    print ("<td>")
    print ("<b>",i,"</b>")
    print ("</td>")
    print ("<td colspan=\"24\">")
    print ("<hr/>")
    print ("</td>")
    print ("</tr>")

print ("</tr>")


print ("<tr>")
print ("<td colspan=\"25\">")
print ("<hr/>")
print ("</td>")
print ("</tr>")

print ("<tr>")
print ("<td>")
print ("</td>")
print ("<td colspan=\"24\">")
print (mhl.MyButtonForm("submit","Submit"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())

# End web page
print (mhl.MyHtmlBottom())