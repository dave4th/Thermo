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

import redis,os # Questa volta servira` solo os, ma lascio anche redis

# Parametri generali
TestoPagina="Consultazione archivi grafici delle temperature"
#ConfigFile=""
WriteFile="/cgi-bin/writegrapharchive.py"
# Redis "key"
#RedisKey = ""
# Archive
DirArchive = "/var/www/archive/"

# Apro il database Redis con l'istruzione della mia libreria
#MyDB = flt.OpenDBFile(ConfigFile)

# Cerco i sensori
ListArchive = sorted(os.listdir(DirArchive), reverse=True)
#ListArchive.remove("???")

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
print ("""
Questo elenca i files in archivio dal piu` recente e permette di selezionarne uno per visualizarlo.
<br/>
<br/>
""")

# Inizio del form
print (mhl.MyActionForm(WriteFile,"POST"))

print ("<table>")

print ("<tr>")
print ("<td>")
print (mhl.MyDropDown("archive",ListArchive,""))
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print ("<hr/>")
print ("</td>")
print ("</tr>")
print ("<tr>")
print ("<td>")
print (mhl.MyButtonForm("submit","Submit"))
print ("</td>")
print ("</tr>")

print ("</table>")


# End form
print (mhl.MyEndForm())

# End web page
print (mhl.MyHtmlBottom())