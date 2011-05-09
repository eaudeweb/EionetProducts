## Script (Python) "gemet-skoscore.rdf"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=
##title=SKOS broader and narrower relations
##

#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
records = container.GetAllRelations()

#set content type
RESPONSE.setHeader('content-type', 'application/rdf+xml')

#start generating rdf content
print '<?xml version="1.0" encoding="UTF-8"?>'
print '''<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:skos="http://www.w3.org/2004/02/skos/core#">'''

for record_id, relations in records.items():
    print '<skos:Concept rdf:about="%s/concept/%s">' % (l_container_url, record_id)
    for relation_type, relation_values in relations.items():
        for value in relation_values:
            if 'http:' in str(value):
                print '<skos:%s rdf:resource="%s" />' % (relation_type, value)
            else:
                print '<skos:%s rdf:resource="%s/concept/%s" />' % (relation_type, l_container_url, value)
    print '</skos:Concept>'
print '</rdf:RDF>'

#return stuff
return printed
