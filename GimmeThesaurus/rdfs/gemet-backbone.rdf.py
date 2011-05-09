## Script (Python) "gemet-backbone.rdf"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=Themes and groups relationships
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
records = container.GetBackbone()

#set content type
RESPONSE.setHeader('content-type', 'application/rdf+xml')

#start generating rdf content
print '<?xml version="1.0" encoding="UTF-8"?>'
print '''<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:skos="http://www.w3.org/2004/02/skos/core#"
            xmlns:gemet="http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#">'''

for record in records.keys():
    groups, themes = records[record]

    print '<rdf:Description rdf:about="%s/concept/%s">' % (l_container_url, record)

    for theme in themes:
        if theme != '':
            print '<gemet:theme rdf:resource="%s/theme/%s" />' % (l_container_url, theme)

    for group in groups:
        if group != '':
            print '<gemet:group rdf:resource="%s/group/%s" />' % (l_container_url, group)

    print '</rdf:Description>'
print '</rdf:RDF>'

#return stuff
return printed
