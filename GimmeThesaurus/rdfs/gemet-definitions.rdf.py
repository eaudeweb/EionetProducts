## Script (Python) "gemet-definitions.rdf"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=langcode='en'
##title=Labels and definitions
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
alias_container_utXmlEncode = container.utXmlEncode

#set content type
RESPONSE.setHeader('content-type', 'application/rdf+xml')

#start generating rdf content
print '<?xml version="1.0" encoding="UTF-8"?>'
print '''<rdf:RDF xmlns:rdf="http://www.w3.org/1999/02/22-rdf-syntax-ns#"
            xmlns:rdfs="http://www.w3.org/2000/01/rdf-schema#"
            xmlns:skos="http://www.w3.org/2004/02/skos/core#"
            xmlns:gemet="http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#"
   xml:lang="%s" xml:base="%s/">''' % ( langcode, l_container_url )
print
for record in container.GetConceptsInfo(langcode=langcode):
    print '<rdf:Description rdf:about="concept/%s">' % container.mp_concept_id(record)
    print '<skos:prefLabel>%s</skos:prefLabel>' % alias_container_utXmlEncode(container.mp_concept_name(record))
    if container.mp_concept_alt_concat(record) != '':
        for alt_label in container.mp_concept_alt_concat(record):
            print '<skos:altLabel>%s</skos:altLabel>' % alias_container_utXmlEncode(alt_label)
    if container.mp_concept_definition(record) != '':
        print '<skos:definition>%s</skos:definition>' % alias_container_utXmlEncode(container.mp_concept_definition(record))
    if container.mp_concept_note(record) != '':
        print '<skos:scopeNote>%s</skos:scopeNote>' % alias_container_utXmlEncode(container.mp_concept_note(record))
    print '</rdf:Description>'
print '</rdf:RDF>'

#return stuff
return printed
