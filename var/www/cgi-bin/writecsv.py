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

import shutil,time

# Parametri generali
TestoPagina="Sposta \"temperature.csv\" in archivio"
WriteFile="/cgi-bin/writecsv.py"
FileCSV="../temperature.csv"
NewFileCSV="../archive/temperature.csv."+time.strftime("%y%m%d%H%M")

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("..........","<hr/>","<br/>")

#form=cgi.FieldStorage()
#cgi.escape(form[i].value)

print("Spostamento del file in corso ...<br/>")

shutil.move(FileCSV,NewFileCSV)

print("<br/>... completato.<br/><hr/>")

print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print (FileCSV)
print ("</td>")
print ("<td>")
print (NewFileCSV)
print ("</td>")
print ("</tr>")
print ("</table>")


# End web page
print (mhl.MyHtmlBottom())