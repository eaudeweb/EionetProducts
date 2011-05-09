## Script (Python) "gemet-relations.html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Relations in simple HTML
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
records = container.GetAllRelations()

#set content type
RESPONSE.setHeader('content-type', 'text/html;charset=utf-8')

#start generating rdf content
print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
print '''<html xmlns="http://www.w3.org/1999/xhtml">'''
print '''<head>'''
print '''<meta http-equiv="content-type" content="text/html; charset=utf-8" />'''
print '''<title>%s</title>''' % script.title
print '''<style type="text/css">'''
print '''table { border-collapse:collapse }\ntd,th {border: 1px solid black}'''
print '''</style>'''
print '''</head>'''
print '''<body>'''
print '''<table>'''
print '''<caption>Concept to concept relations</caption>'''
print '''<col style="width:4em"/><col style="width:8em"/><col style="width:4em"/>'''
print '''<thead><tr><th>Id</th><th>Relation</th><th>Object</th></tr></thead><tbody>'''

for record_id, relations in records.items():
    for relation_type, relation_values in relations.items():
        for value in relation_values:
            print '<tr><td class="code">%s</td>' % record_id,
            print '<td>%s</td><td class="%s">%s</td></tr>' % (
                str(relation_type).title(), relation_type, value)
print '</tbody></table></body></html>'

#return stuff
return printed
