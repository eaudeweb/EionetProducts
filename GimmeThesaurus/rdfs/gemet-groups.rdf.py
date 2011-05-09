## Script (Python) "gemet-groups.rdf"
##bind container=container
##bind context=context
##bind namespace=
##bind script=script
##bind subpath=traverse_subpath
##parameters=langcode='en'
##title=Supergroups, groups and themes
##
#get the HTML request and response objects.
request = container.REQUEST
RESPONSE =  request.RESPONSE

#load data
l_container_url = container.absolute_url()
alias_container_utXmlEncode = container.utXmlEncode
groups, supergroups, themes, errors = container.GetGroupsAndThemes(langcode)

#set content type
RESPONSE.setHeader('content-type', 'application/rdf+xml')

#start generating rdf content
print '<?xml version="1.0" encoding="UTF-8"?>'
print '''<rdf:RDF xml:lang="%s"
            xmlns:rdf='http://www.w3.org/1999/02/22-rdf-syntax-ns#'
            xmlns:rdfs='http://www.w3.org/2000/01/rdf-schema#'
            xmlns:skos="http://www.w3.org/2004/02/skos/core#"
            xmlns="http://www.eionet.europa.eu/gemet/2004/06/gemet-schema.rdf#">''' % langcode
for sgroup in supergroups:
    print '<SuperGroup rdf:about="%s/supergroup/%s">' % (l_container_url, container.mp_group_id(sgroup))
    print '<rdfs:label>%s</rdfs:label>' % alias_container_utXmlEncode(container.mp_group_descr(sgroup))
    print '</SuperGroup>'
for group in groups:
    print '<Group rdf:about="%s/group/%s">' % (l_container_url, container.mp_group_id(group))
    print '<subGroupOf rdf:resource="%s/supergroup/%s" />' % (l_container_url, container.mp_supergroup_id(group))
    print '<rdfs:label>%s</rdfs:label>' % alias_container_utXmlEncode(container.mp_group_descr(group))
    print '</Group>'
for theme in themes:
    print '<Theme rdfs:label="%s" rdf:about="%s/theme/%s" />' % (alias_container_utXmlEncode(container.mp_theme_descr(theme)), l_container_url, container.mp_theme_id(theme))
print '</rdf:RDF>'

#return stuff
return printed
