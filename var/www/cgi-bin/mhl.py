#!/usr/bin/env python3

## My HTML Library
#

""" ATTENZIONE: Non tutte le funzioni sono state testate/usate
    alcune neanche fatte
    Mon 23 Feb 2015 17:28:26 CET - Qualcosa e` stato fatto
"""

"""
Aggiornamenti: Sat 19 Mar 2016 08:31:19 AM CET

"""

## Blocchi per la costruzione della pagina web
# Html page
def MyHtml():
    return "Content-type: text/html\n\n"

def MyHtmlHead():
    return ("""
<html>

<head>
  <title>My HTML Library</title>
  <meta name="GENERATOR" content="Midnight Commander (mcedit)">
  <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
  <meta name="Keywords" content="mydynamicpage">
  <meta name="Author" content="Davide">
</head>

<body>
""")

# Qui nel mezzo il codice html

def MyHtmlBottom():
    return ("""
</body>
</html>
""")

# Fine blocchi html


## Forms # Non tutte fatte

def MyActionForm(Action,Post):
    return("<form action=\""+Action+"\" method=\""+Post+"\">")

def MyTextForm(Name,Value,Size,Required,Readonly):
    return("<input type=\"text\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" "+Required+" "+Readonly+">")

def MyMailForm(Name,Value,Size,Required,Readonly):
    return("<input type=\"email\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" "+Required+" "+Readonly+">")

def MyTextAreaForm(Name,Value,Cols,Rows,Required,Readonly):
    return("<textarea name=\""+Name+"\" value=\""+Value+"\" cols=\""+Cols+"\" rows=\""+Rows+"\" "+Required+" "+Readonly+">")

def MyNumberForm(Name,Value,Size,Maxlenght,Min,Max,Step,Required,Readonly):
    return("<input type=\"number\" name=\""+Name+"\" value=\""+Value+"\" size=\""+Size+"\" maxlenght=\""+Maxlenght+"\" min=\""+Min+"\" max=\""+Max+"\" step=\""+Step+"\" "+Required+" "+Readonly+">")

def MyCheckboxForm(Name,Value,Checked=""):
    return("<input type=\"checkbox\" name=\""+Name+"\" value=\""+Value+"\" "+Checked+">")

def MyRadioButton(Name,Value,Checked):
    return("<input type=\"radio\" name=\""+Name+"\" value=\""+Value+"\" "+Checked+">")

def MyDropDown(Name,Values,SelectedValue):	# SelectedValue deve contenere uno dei Values
    Select="<select name=\""+Name+"\">"
    for i in Values:
        if i == SelectedValue:
            Selected="selected"
        else:
            Selected=""
        Option="<option value=\""+i+"\" "+Selected+">"+i+"</option>"
        Select=Select+Option
    Select=Select+"</select>"
    return(Select)

def MyPasswordForm(Type,Name,Required):
    return("<input type=\""+Type+"\" name=\""+Name+"\" "+Required+">")

def MyButtonForm(Type,Value):
    return("<input type=\""+Type+"\" value=\""+Value+"\">")

def MyEndForm():
    return("</form>")
