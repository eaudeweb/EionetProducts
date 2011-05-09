##parameters=member_id, password, member_email, send_password=False, **kw
##title=Add a member
##
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.permissions import ManageUsers
try:
    from Products.CMFDefault.utils import MessageID as _
except:
    # BBB Zope 2.7
    _ = str

mtool = getToolByName(script, 'portal_membership')
mdtool = getToolByName(script, 'portal_memberdata')
ptool = getToolByName(script, 'portal_properties')
rtool = getToolByName(script, 'portal_registration')

properties = { 'username' : member_id
             , 'email' : member_email
             }
for prop_info in mdtool.getSortedMemberProperties():
    key = prop_info['ldap_name']
    value = kw.get(key, None)

    if value is not None:
        properties[key] = value

try:
    rtool.addMember( id=member_id
                   , password=password
                   , properties=properties
                   )

except ValueError, errmsg:
    return context.setStatus(False, errmsg)
else:
    if ptool.getProperty('validate_email') or send_password:
        rtool.registeredNotify(member_id)
    if mtool.checkPermission(ManageUsers, mtool):
        return context.setStatus(True, _('Member registered.'))
    else:
        return context.setStatus(False, _('Success!'))
