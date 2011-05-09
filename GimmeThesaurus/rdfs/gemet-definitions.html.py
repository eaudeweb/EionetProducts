## Script (Python) "gemet-definitions.html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=langcode='en'
##title=Labels and definitions in simple HTML table
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE
from Products.PythonScripts.standard import html_quote, newline_to_br
#load data
l_container_url = container.absolute_url()
alias_container_utXmlEncode = container.utXmlEncode

#set content type
RESPONSE.setHeader('content-type', 'text/html;charset=utf-8')

#start generating rdf content
print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
print '''<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%s">'''  % langcode
print '''<head>'''
print '''<meta http-equiv="content-type" content="text/html; charset=utf-8" />'''
print '''<title>%s</title>''' % script.title
print '''<style type="text/css">'''
print '''table { border-collapse:collapse; margin: 1em; }'''
print '''td,th {border: 1px solid black}'''
print '''.definition, .scopenote {
white-space: pre; /* CSS2 */
white-space: -moz-pre-wrap; /* Mozilla */
white-space: pre-wrap; /* CSS 2.1 */
white-space: pre-line; /* CSS 3 (and 2.1 as well, actually) */
word-wrap: break-word; /* IE */
}'''
print '''</style>'''
print '''</head>'''
print '''<body>'''
print '''<table>'''
print '''<caption>Concept definitions</caption>'''
print '''<col style="width:4em"/><col style="width:12em"/><col style="width:40em"/><col style="width:4em"/>'''
print '''<thead><tr><th>Id</th><th>Concept</th><th>Definition</th><th>Scope note</th></tr></thead><tbody>'''
for record in container.GetConceptsInfo(langcode=langcode):
    print '<tr class="code"><td>%s</td>' % container.mp_concept_id(record)
    print '<td class="name">%s</td>' % html_quote(container.mp_concept_name(record))
    print '<td class="definition">%s</td>' % html_quote(container.mp_concept_definition(record),'\r','\n')
    print '<td class="scopenote">%s</td>' % html_quote(container.mp_concept_note(record))
    print '</tr>'
print '</tbody></table></body></html>'

#return stuff
return printed
