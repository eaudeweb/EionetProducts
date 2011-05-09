## Script (Python) "gemet-backbone.html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Themes and groups relationships as simple HTML
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
records = container.GetBackbone()

#set content type
RESPONSE.setHeader('content-type', 'text/html;charset=utf-8')

#start generating html content
print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">'''
print '''<html xmlns="http://www.w3.org/1999/xhtml">'''
print '''<head>'''
print '''<meta http-equiv="content-type" content="text/html; charset=utf-8" />'''
print '''<title>%s</title>''' % script.title
print '''<style type="text/css">'''
print '''table { border-collapse:collapse; margin: 1em; }\ntd,th {border: 1px solid black}'''
print '''</style>'''
print '''</head>\n<body>'''
print '''<table>'''
print '''<caption>Relations</caption>'''
print '''<col style="width:4em"/><col style="width:6em"/><col style="width:4em"/>'''
print '''<thead><tr><th>Id</th><th>Relation</th><th>Object</th></tr></thead><tbody>'''

for record in records.keys():
    groups, themes = records[record]

    for theme in themes:
        if theme != '':
            print '<tr><td>%s</td><td>Theme</td><td>%s</td></tr>' % ( record, theme )

    for group in groups:
        if group != '':
            print '<tr><td>%s</td><td>Group</td><td>%s</td></tr>' % ( record, group )

print '</tbody></table></body></html>'


#return stuff
return printed
