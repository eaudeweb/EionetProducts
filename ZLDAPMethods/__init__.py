"""LDAP Filter Methods Package """

import LM

def initialize(context):

    context.registerClass(
        LM.LDAPFilter,
        constructors = (LM.manage_addZLDAPMethodForm,
                        LM.manage_addZLDAPMethod),
        icon = "LDAP_Method_icon.gif",
        legacy = (LM.LDAPConnectionIDs,), #special baby to add to ObjectManagers
        )

