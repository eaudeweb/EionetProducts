Quick README on ZLDAP Filter Methods

 Current

  ZLDAP Filter Methods are a way of executing LDAP Searches according
  to RFC1558 'A String Representation of LDAP Search Filters'.  They
  can be used like ZSQL Methods and use DTML inside of them.  For
  example, one could do a Filter of 'uid=<dtml-var foo>'.  ZLDAP Filter 
  Methods return Entry objects.


 Future

  To do complex filters, especially with plain-vanilla DTML, the
  syntax can get ugly quick.  Some LDAP Filter specific DTML tags
  (similar to tags like dtml-sqlgroup and dtml-sqltest, etc...) should 
  be implemented to ease in writing complex and dynamic filters in a
  more Zope-ish fashion.  (As if the current package isn't Zope-ish
  enough).
