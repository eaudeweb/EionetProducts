##parameters=b_start=0, member_id='', member_email='', password='', confirm='', send_password='', add='', cancel=''
##
from Products.CMFCore.utils import getToolByName
from Products.CMFDefault.permissions import ManageUsers

try:
    from Products.CMFDefault.utils import MessageID as _
except:
    # Zope 2.7/CMF 1.5
    _ = str

atool = getToolByName(script, 'portal_actions')
rtool = getToolByName(script, 'portal_registration')
mtool = getToolByName(script, 'portal_membership')
mdtool = getToolByName(script, 'portal_memberdata')
ptool = getToolByName(script, 'portal_properties')
utool = getToolByName(script, 'portal_url')
portal_url = utool()
validate_email = ptool.getProperty('validate_email')
is_anon = mtool.isAnonymousUser()
is_newmember = False
is_usermanager = mtool.checkPermission(ManageUsers, mtool)


form = context.REQUEST.form
if add and \
        context.validatePassword(**form) and \
        context.members_add_control(**form) and \
        context.setRedirect(atool, 'user/join', b_start=b_start):
    return
elif cancel and \
        context.setRedirect(atool, 'global/manage_members', b_start=b_start):
    return


options = {}

if context.REQUEST.get('portal_status_message', '') == _('Success!'):
    is_anon = False
    is_newmember = True

options['title'] = is_usermanager and _('Register Member') \
                                  or _('Become a Member')
options['member_id'] = member_id
options['member_email'] = member_email
options['password'] = is_newmember and context.REQUEST.get('password', '') or ''
options['send_password'] = send_password
options['portal_url'] = portal_url
options['isAnon'] = is_anon
options['isAnonOrUserManager'] = is_anon or is_usermanager
options['isNewMember'] = is_newmember
options['isOrdinaryMember'] = not (is_anon or is_newmember or is_usermanager)
options['validate_email'] = validate_email

added_properties = mdtool.getSortedMemberProperties()
options['added_properties'] = added_properties
for property_info in added_properties:
    p_name = property_info['ldap_name']
    options[p_name] = form.get(p_name, '')

buttons = []
if is_newmember:
    try:
        target = atool.getActionInfo('user/logged_in')['url']
    except ValueError:
        # In CMF 1.5.x we use old-style actions on separate providers
        target = mtool.getActionInfo('user/logged_in')['url']
    buttons.append( {'name': 'login', 'value': _('Log in')} )
else:
    try:
        target = atool.getActionInfo('user/join')['url']
    except ValueError:
        # In CMF 1.5.x we use old-style actions on separate providers
        target = rtool.getActionInfo('user/join')['url']
    buttons.append( {'name': 'add', 'value': _('Register')} )
    buttons.append( {'name': 'cancel', 'value': _('Cancel')} )
options['form'] = { 'action': target,
                    'listButtonInfos': tuple(buttons) }

return context.join_template(**options)
