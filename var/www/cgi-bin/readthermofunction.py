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
TestoPagina="Configurazione/Selezione funzionamento"
ConfigFile="../conf/thermo.json"
WriteFile="/cgi-bin/writethermofunction.py"
# Redis "key"
RedisKey = "thermo:function"

Values = [ "on","manuale","antigelo","off" ]

# Apro il database Redis con l'istruzione della mia libreria
MyDB = flt.OpenDBFile(ConfigFile)

# Genero chiave/valori se non esiste
# Assegno dei valori piu` o meno standard
if not MyDB.exists(RedisKey):
    MyDB.set(RedisKey,"off")

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
<ul>
    <li>on = Acceso
    </li>
    <li>manuale = Manuale (funzionamento con temperatura manuale)
    </li>
    <li>antigelo = Antigelo (funzionamento antigelo)
    </li>
    <li>off = Spento
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

# Questa volta i valori ho deciso di inserirli "a mano", cioe`
# sono prefissati, non volevo complicarmi la vita, tanto l'impianto
# dovra` avere solo tre modalita` di funzionamento.
Selected = flt.Decode(MyDB.get(RedisKey))
print ("<tr>")
print ("<td>")
print ("Selezione: ",sep="")
print ("</td>")
print ("<td>")
print (mhl.MyDropDown(RedisKey,Values,Selected))
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