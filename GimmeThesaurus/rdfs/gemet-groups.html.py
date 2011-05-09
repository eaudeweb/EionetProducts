## Script (Python) "gemet-groups.html"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=langcode='en'
##title=Supergroups, groups and themes as simple HTML tables
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
from Products.PythonScripts.standard import html_quote
groups, supergroups, themes, errors = container.GetGroupsAndThemes(langcode)

#set content type
RESPONSE.setHeader('content-type', 'text/html;charset=utf-8')

#start generating html content
print '''<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">\n'''
print '''<html xmlns="http://www.w3.org/1999/xhtml" xml:lang="%s">\n'''  % langcode
print '''<head>\n'''
print '''<meta http-equiv="content-type" content="text/html; charset=utf-8" />\n'''
print '''<title>%s</title>\n''' % script.title
print '''<style type="text/css">'''
print '''table { border-collapse:collapse; margin: 1em 0; }\ntd,th {border: 1px solid black}\n'''
print '''</style>\n'''
print '''</head>\n<body>\n'''
print '''<table>'''
print '''<caption>Super groups</caption>'''
print '''<col style="width:4em"/><col style="width:6em"/><col style="width:4em"/><col style="width:30em"/>'''
print '''<thead><tr><th>Id</th><th>Type</th><th>SubGroupOf</th><th>Label</th></tr></thead><tbody>'''

#start generating HTML content
for sgroup in supergroups:
    print '<tr><td>%s</td><td>SuperGroup</td><td></td><td>%s</td></tr>' % (container.mp_group_id(sgroup),html_quote(container.mp_group_descr(sgroup)))
print '''</tbody></table>'''

print '''<table>'''
print '''<caption>Groups</caption>'''
print '''<col style="width:4em"/><col style="width:6em"/><col style="width:4em"/><col style="width:30em"/>'''
print '''<thead><tr><th>Id</th><th>Type</th><th>SubGroupOf</th><th>Label</th></tr></thead><tbody>'''
for group in groups:
    print '<tr><td>%s</td><td>Group</td>' % container.mp_group_id(group)
    print '<td>%s</td>' % container.mp_supergroup_id(group)
    print '<td>%s</td>' % html_quote(container.mp_group_descr(group))
    print '</tr>'
print '''</tbody></table>'''

print '''<table>'''
print '''<caption>Themes</caption>'''
print '''<col style="width:4em"/><col style="width:6em"/><col style="width:30em"/>'''
print '''<thead><tr><th>Id</th><th>Type</th><th>Label</th></tr></thead><tbody>'''
for theme in themes:
    print '<tr><td>%s</td><td>Theme</td><td>%s</td></tr>' % (container.mp_theme_id(theme),html_quote(container.mp_theme_descr(theme)))
print '''</tbody></table>'''
print '''</body></html>'''

#return stuff
return printed
