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
#WriteFile="/cgi-bin/writegrapharchive.py"
# Redis "key"
#RedisKey = ""
# Archive
DirArchive = "/var/www/archive/"

# Apro il database Redis con l'istruzione della mia libreria
#MyDB = flt.OpenDBFile(ConfigFile)

# Cerco i sensori
#ListArchive = sorted(os.listdir(DirArchive), reverse=True)
#ListArchive.remove("???")

# Start web page - Uso l'intestazione "web" della mia libreria
print (mhl.MyHtml())
#print (mhl.MyHtmlHead())

# Scrivo il Titolo/Testo della pagina
#print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
#print ("<hr/>","<br/>")
# Eventuale help/annotazione
#print ("......","<hr/>","<br/>")


form=cgi.FieldStorage()

FileName=cgi.escape(form["archive"].value)

""" Usato solo per prove
print ("<h2>Dati inseriti/modificati:</h2>")
print ("<br>")
print ("<table border=\"1\" cellspacing=\"0\" cellpadding=\"3\">")
print ("<tr>")
print ("<td>")
print ("FileName")
print ("</td>")
print ("<td>")
print (FileName)
print ("</td>")
print ("</tr>")
print ("</table>")
"""

# Devo "stampare" una pagina identica a quella del grafico ..
print ("""
<!DOCTYPE html>
<html>

<head>
  <title>ThermoRed</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="termoregolatore, thermo, temperatura, python">
  <meta name="Author" content="Davide">

<script type="text/javascript"
  src="../dygraph-combined.js"></script>
</head>


<body>
<title>Temperature Graphic</title>
""")

print ("<h1>","<center>",TestoPagina,"</center>","</h1>")
print ("<hr/>","<br/>")

print ("""
<p>
Questa "chart" e` interattiva.
Muovi il mouse per evidenziare i singoli valori.
Clicca e trascina per selezionare ed effettuare uno zoom sull'area selezionata.
Doppio click del mouse per ritornare alla visualizzazione globale.
Con il tasto "Shift" premuto, usa il click del mouse per trascinare l'area di visualizzazione.
</p>

<div id="graphdiv" style="position:absolute; left:20px; right:20px; top:250px; bottom:20px;"></div>
<script type="text/javascript">
  g = new Dygraph(

    // containing div
    document.getElementById("graphdiv"),

    // CSV or path to a CSV file.
""")

print ("    \"../archive/"+FileName+"\",")

print ("""
    {
    showRoller: false,
    //title: 'Grafico temperature',
    ylabel: 'Temperature (C)',
    xlabel: 'Time',
    //legend: 'always',
    labelDivStyles: {'textalign':'right'}
    }
  );
</script>

</body>
</html>

""")


# End web page
#print (mhl.MyHtmlBottom())