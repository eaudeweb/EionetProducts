Gimme Thesaurus readme file.

Hint:
If you use Apache as a reverse proxy to Zope, comment out the
AddDefaultCharset ISO-8859-1 line in httpd.conf. GimmeThesaurus is a
UTF-8 product, and some of the languages won't work otherwise.

This product is meant to integrate with standard_template.pt


Bellow are the meanings of the "statusCode":
      0 -> "OK"
    204 -> "Invalid level"
    205 -> "Invalid direction"
    206 -> "Invalid depth"
    209 -> "No matches found"
    210 -> "Invalid parameters"
    211 -> "No query"
    212 -> "No REQUEST"
    213 -> "No REQUEST[REMOTE_ADDR]"
    217 -> "Database error"