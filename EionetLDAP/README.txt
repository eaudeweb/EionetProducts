Eionet LDAP tools
=================

This package provides web forms for user interaction with the Eionet LDAP
account system. Users can self-register, recover lost passwords and modify
personal information.


Installation
------------

The EionetLDAP package needs to be installed in the Products folder of a Zope
instance. You can create an EionetLDAP object anywhere, with any name; it
should find acl_users and MailHost (see Dependencies below) by itself. You can
customize the noreply e-mail address and e-mail templates from the Properties
tab.


Dependencies
------------

LDAPUserFolder: the acl_users object needs to be an LDAPUserFolder. EionetLDAP
makes use of LDAPUserFolder to talk to the LDAP server. LDAPUserFolder needs to
be properly configured:

 * "User object classes" must have the following value:
    "top,person,organizationalPerson,inetOrgPerson".
 * "LDAP schema" must contain the following names: uid, cn, sn, givenName,
    mail, labeledURI, o, postalAddress, telephoneNumber.
 * The administration DN and password must be entered properly.
 * You should be able to browse user records from the Users tab.

MailHost: EionetLDAP looks for a MailHost object named "MailHost" to send
e-mails for account confirmation and password recovery.


Functionality
-------------

EionetLDAP has the following workflows:

 * Self-registration: the user enters basic account information; this
    information is stored in the EionetLDAP object and a confirmation e-mail
    is sent to the user, with a keyed URL inside. When the user accesses the
    URL, the account is created in LDAP and a random password is generated and
    displayed to the user.
 * Change password / personal information: two simple forms that modify entries
    in the LDAP database.
 * Recover lost password: the user enters either an uid (username) or e-mail
    address. If a match is found, an e-mail message is sent to the user,
    containing a keyed URL. When the URL is accessed, a new random password is
    generated and displayed to the user.

Keys associated with account confirmation and password recovery are randomly
generated and cryptographically secure. They are stored inside the EionetLDAP
Zope object and expire: 3 days for account confirmation, 1 day for password
recovery.
