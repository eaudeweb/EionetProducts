# The contents of this file are subject to the Mozilla Public
# License Version 1.1 (the "License"); you may not use this file
# except in compliance with the License. You may obtain a copy of
# the License at http://www.mozilla.org/MPL/
#
# Software distributed under the License is distributed on an "AS
# IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
# implied. See the License for the specific language governing
# rights and limitations under the License.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Morega, Eau de Web

__version__='0.1'

# Python imports
from datetime import datetime, timedelta
import re

# Zope imports
from AccessControl import ClassSecurityInfo
from Globals import InitializeClass
from Products.PageTemplates.PageTemplateFile import PageTemplateFile
from OFS.SimpleItem import SimpleItem
from AccessControl import getSecurityManager
from AccessControl.SecurityManagement import noSecurityManager
from AccessControl.unauthorized import Unauthorized
from Products.MailHost.MailHost import MailHost

# Product imports
from Products.LDAPUserFolder import LDAPUserFolder, utils as ldap_utils

def random_sha_b64():
    from sha import sha
    from random import random
    from base64 import b64encode
    
    return b64encode(sha(str(random())).digest())[:-2].replace('/', '_').replace('+', '.')

class EionetLDAPConfigurationError(Exception):
    pass

manage_addEionetLDAP_html = PageTemplateFile('zpt/add', globals())
def manage_addEionetLDAP(self, id, REQUEST=None):
    """ Adds a new Eionet LDAP object """
    ob = EionetLDAP(id)
    self._setObject(id, ob)
    
    th = self._getOb(id)
    # check we have our dependencies installed (LDAPUserFolder, MailHost)
    # (if these fail, they will raise an error, and abort the ZODB transaction)
    th._get_ldapuserfolder()
    th._get_mailhost()
    
    if REQUEST is not None:
        return self.manage_main(self, REQUEST, update_menu=1)

class EionetLDAP(SimpleItem):
    """ Eionet LDAP """
    
    meta_type = 'Eionet LDAP'
    product_name = 'Eionet LDAP'
    manage_options = (
        {'label':'Properties', 'action':'manage_propertiesForm'},
        {'label':'View', 'action':'index_html'},
    ) + SimpleItem.manage_options
    
    security = ClassSecurityInfo()
    
    def __init__(self, id):
        """ constructor """
        
        self.id = id
        self._auto_expire_list = []
        self.noreply_mail_address = "noreply@eionet.europa.eu"
        self.password_reset_template = ("Hello ${NAME},\n\n"
                    "If you have requested a password reset of your Eionet "
                    "account \"${UID}\",\nplease click the link below, or "
                    "copy and paste it in your browser:\n\n"
                    "    ${LINK}\n\n"
                    "Otherwise you can ignore this message.\n")
        self.account_confirmation_template = ("Hello ${NAME},\n\n"
                    "If you have requested an Eionet account using the ${EMAIL}\n"
                    "e-mail address and \"${UID}\" username, please click "
                    "the link below, or\ncopy and paste it in your browser:\n\n"
                    "    ${LINK}\n\n"
                    "Otherwise you can ignore this message.\n")
    
    _result_page = PageTemplateFile('zpt/result_page', globals())
    
    security.declarePublic('index_html')
    index_html = PageTemplateFile('zpt/index', globals())
    
    security.declareProtected('View management screens', 'manage_propertiesForm')
    manage_propertiesForm = PageTemplateFile('zpt/properties', globals())
    
    security.declareProtected('View management screens', 'manageProperties')
    def manageProperties(self, noreply_mail_address, password_reset_template,
            account_confirmation_template, REQUEST=None, RESPONSE=None):
        """ manage basic properties """
        
        self.noreply_mail_address = noreply_mail_address
        self.password_reset_template = password_reset_template
        self.account_confirmation_template = account_confirmation_template
        
        if REQUEST is not None:
            return RESPONSE.redirect('manage_propertiesForm')
    
    def _add_to_auto_expire_list(self, key, kind, data, expire=timedelta(days=1)):
        self._auto_expire_list.append( (key, kind, datetime.now() + expire, data) )
        self._p_changed = 1
    
    def _clean_auto_expire_list(self):
        now = datetime.now()
        for item in self._auto_expire_list:
            if now > item[2]:
                self._auto_expire_list.remove(item)
                self._p_changed = 1
    
    def _search_auto_expire_list(self, key, kind):
        self._clean_auto_expire_list()
        
        for item in self._auto_expire_list:
            if item[0] == key and item[1] == kind:
                data = item[3]
                self._auto_expire_list.remove(item)
                self._p_changed = 1
                return data
        
        return None
    
    def _get_ldapuserfolder(self):
        # ldapuserfolder is cached, so we don't waste time with checks
        if not hasattr(self, '_v_ldapuserfolder'):
            ob = self.acl_users
            
            # check that we have a LDAPUserFolder instance, and that it's
            # properly configured
            if not isinstance(ob, LDAPUserFolder):
                raise EionetLDAPConfigurationError('Expected LDAPUserFolder '
                    'object at "acl_users"')
            
            for ldap_class in ['top', 'person', 'organizationalPerson', 'inetOrgPerson']:
                if ldap_class not in ob._user_objclasses:
                    raise EionetLDAPConfigurationError('LDAPUserFolder configuration '
                        'parameter "User object classes" needs value "%s"' % ldap_class)
            for attr in ['mail', 'cn', 'givenName', 'sn', 'o', 'postalAddress',
                    'telephoneNumber', 'labeledURI', 'uid']:
                if attr not in ob._ldapschema:
                    raise EionetLDAPConfigurationError('Schema of LDAPUserFolder '
                        'instance has no attribute named %s' % attr)
            
            self._v_ldapuserfolder = ob
        
        return self._v_ldapuserfolder
    
    def _get_mailhost(self):
        try:
            ob = self.MailHost
            if isinstance(ob, MailHost):
                return ob
        except:
            pass
        raise EionetLDAPConfigurationError('Expected a MailHost object named '
            '"MailHost". Please create one.')
    
    def _send_mail(self, msg_to, msg_subject, msg_body):
        mailhost = self._get_mailhost()
        
        from email.MIMEText import MIMEText
        from email.MIMEMessage import MIMEMessage
        
        msg = MIMEMessage(MIMEText(msg_body.encode('utf-8'), _charset='utf-8'))
        msg['Subject'] = msg_subject
        msg['From'] = self.noreply_mail_address
        msg['To'] = msg_to
        
        mailhost.send(msg.as_string())
    
    def _build_dn(self, uid):
        return 'uid=%s,%s' % (uid, self._get_ldapuserfolder().users_base)
    
    def _check_user_password(self, uid, password):
        ldapuserfolder = self._get_ldapuserfolder()
        if ldapuserfolder.getUserByAttr('uid', uid, password):
            return True
        return False
    
    def _change_account_password(self, uid, new_password):
        dn=self._build_dn(uid)
        
        # the following code is taken from LDAPUserFolder, because
        # LDAPUserFolder.manage_editUserPassword does not return error messages
        ldapuserfolder = self._get_ldapuserfolder()
        ldap_pw = ldap_utils._createLDAPPassword(new_password, ldapuserfolder._pwd_encryption)
        err_msg = ldapuserfolder._delegate.modify(dn=dn, attrs={'userPassword':[ldap_pw]})
        
        if err_msg:
            return err_msg
        
        ldapuserfolder._expireUser(ldapuserfolder.getUserByDN(ldap_utils.to_utf8(dn)))
        return None # no error
    
    def _get_logged_in_user(self):
        uid = self.get_current_user()
        if uid is None:
            raise Unauthorized() # force logout
        
        ldapuserfolder = self._get_ldapuserfolder()
        user = ldapuserfolder.getUserByDN(ldap_utils.to_utf8(self._build_dn(uid)))
        if user == None:
            raise ValueError('User with uid "%s" does not exist' % uid)
        
        return user
    
    security.declarePublic('get_current_user')
    def get_current_user(self):
        return getSecurityManager().getUser().getId()
    
    security.declarePublic('force_logout')
    def force_logout(self):
        """ Force the browser to log out """
        raise Unauthorized()
    
    security.declarePublic('force_login')
    def force_login(self):
        """ Force the browser to log in """
        if not self.get_current_user():
            raise Unauthorized()
    
    security.declarePublic('must_be_user')
    def must_be_user(self, uid):
        """ Make sure the current user is 'uid'. """
        # NOTE: this is a non-standard way of enforcing user security
        if self.get_current_user() != uid:
            raise Unauthorized()
    
    # create account
    _create_account = PageTemplateFile('zpt/create_account', globals())
    
    def _generate_uid(self, first_name, last_name):
        ldapuserfolder = self._get_ldapuserfolder()
        uid = re.sub(r'[^a-z0-9]', '', last_name.lower())
        if len(uid) > 5:
            uid = uid[:5]
        uid += re.sub(r'[^a-z0-9]', '', first_name.lower())
        if len(uid) > 8:
            uid = uid[:8]
        if len(uid) < 4:
            return None
        
        # make sure uid is unique
        def find_duplicate(uid_):
            if ldapuserfolder.findUser('uid', uid_, exact_match=True):
                return True
            for item in self._auto_expire_list:
                if item[1] == 'newuser' and item[3]['uid'] == uid_:
                    return True
            return False
        
        if ldapuserfolder.findUser('uid', uid, exact_match=True):
            n = 1
            while(find_duplicate(uid + str(n))):
                n += 1
            # found a unique id
            uid = uid + str(n)
        
        return uid
    
    security.declarePublic('do_create_account')
    def create_account(self, REQUEST=None):
        """ Create an LDAP account """
        if REQUEST:
            REQUEST.response.setHeader('content-type', 'text/html;charset=utf-8')
        
        form_data = dict(REQUEST.form)
        for key in ['first_name', 'last_name', 'uid', 'email', 'organisation']:
            if key not in form_data:
                form_data[key] = ''
        
        if REQUEST and REQUEST.REQUEST_METHOD == 'GET':
            return self._create_account(form_data=form_data)
        
        if REQUEST and 'generate' in form_data:
            uid = self._generate_uid(form_data['first_name'], form_data['last_name'])
            if not uid:
                return self._create_account(error='Cannot generate username: too '
                        'few latin characters.', form_data=form_data)
            
            form_data['uid'] = uid
            return self._create_account(form_data=form_data)
        
        # do some sanity checks on data
        def error_response(err):
            if REQUEST:
                return self._create_account(error=err, form_data=form_data)
            else:
                return err
        
        if not form_data['first_name']:
            return error_response('First name is mandatory.')
        
        if not form_data['last_name']:
            return error_response('Last name is mandatory.')
        
        if not re.match(r'^[a-z0-9]+$', form_data['uid']) or len(form_data['uid']) < 4:
            return error_response('Username must be made up of lowercase latin '
                    'letters and digits with a minimum length of 4.')
        
        if not re.match(r'^[\w \-]+$', form_data['first_name'], re.UNICODE):
            return error_response('First name is invalid. Only letters, numbers, '
                    'spaces and dashes are allowed.')
        
        if not re.match(r'^[\w \-]+$', form_data['last_name'], re.UNICODE):
            return error_response('Last name is invalid. Only letters, numbers, '
                    'spaces and dashes are allowed.')
        
        if not re.match(r'^([\w_\.\-\+])+\@(([\w\-])+\.)+([\w]{2,4})+$', form_data['email']):
            return error_response('Email address is invalid.')
        
        # stash the information and send a verification email
        key = random_sha_b64()
        reset_url = "%s/confirm_account?key=%s" % (self.absolute_url(), key)
        
        subject = 'Confirm your Eionet account "%s"' % form_data['uid']
        body = unicode(self.account_confirmation_template) \
                    .replace('${NAME}', ("%s %s" % (
                            form_data['first_name'],
                            form_data['last_name']
                    ))) \
                    .replace('${UID}', form_data['uid']) \
                    .replace('${LINK}', reset_url) \
                    .replace('${EMAIL}', form_data['email'])
        
        try:
            self._send_mail(msg_to=form_data['email'], msg_subject=subject, msg_body=body)
        except Exception, e:
            error = 'Error sending email: %s' % str(e)
            if REQUEST:
                return self._result_page(errors=[error])
            else:
                return error
        
        self._add_to_auto_expire_list(key, 'newuser', form_data, expire=timedelta(days=3))
        
        if REQUEST:
            return self._result_page(messages=[
                    'An e-mail has been sent to your address (%s). Follow the '
                    'instructions in that message to confirm your account.'
                    % form_data['email']])
    
    def confirm_account(self, key, REQUEST=None):
        """ create an account, if the key matches """
        data = self._search_auto_expire_list(key, 'newuser')
        
        if not data:
            if REQUEST:
                return self._result_page(errors=[
                        ('The account confirmation key did not verify. '
                        'Please <a href="%s/create_account">try again</a> '
                        'or contact the administrator.') % self.absolute_url()
                    ])
            else:
                return 'error verifying key'
        
        password = random_sha_b64()[:8]
        ldapuserfolder = self._get_ldapuserfolder()
        result = ldapuserfolder.manage_addUser(kwargs={
            'uid': data['uid'],
            'cn': '%s %s' % (data['first_name'], data['last_name']),
            'sn': data['last_name'],
            'givenName': data['first_name'],
            'user_pw': password,
            'confirm_pw': password,
            'mail': data['email'],
            'o': data['organisation'],
        })
        
        if REQUEST:
            if result:
                return self._result_page(errors=['Error: %s' % result])
            else:
                return self._result_page(messages=[
                    'Your account has been confirmed. The initial password is "%s", '
                    'you may <a href="%s/change_password">change it</a> at any time.'
                    % (password, self.absolute_url()) ])
        else:
            return result
    
    # edit personal information
    _edit_account = PageTemplateFile('zpt/edit_account', globals())
    
    security.declarePublic('edit_account')
    def edit_account(self, uid=None, REQUEST=None):
        """ Change personal information in an LDAP account """
        if REQUEST:
            REQUEST.response.setHeader('content-type', 'text/html;charset=utf-8')
        
        ldapuserfolder = self._get_ldapuserfolder()
        
        form_data = dict(REQUEST.form)
        
        if REQUEST.REQUEST_METHOD == 'GET':
            user = self._get_logged_in_user()
            
            attr_mapping = {
                'uid': 'uid',
                'email': 'mail',
                'uri': 'labeledURI',
                'organisation': 'o',
                'postal_address': 'postalAddress',
                'telephone_number': 'telephoneNumber',
            }
            for form_key, attr_name in attr_mapping.iteritems():
                form_data[form_key] = user.getProperty(attr_name)
            return self._edit_account(form_data=form_data)
        
        self.must_be_user(uid)
        
        # do some sanity checks on data
        def error_response(err):
            if REQUEST:
                return self._edit_account(error=err, form_data=form_data)
            else:
                return err
        
        if form_data['uri'] and not re.match(r'^http\://', form_data['uri']):
            return error_response('URL is invalid (must be empty or start '
                    'with "http://").')
        
        ldapuserfolder = self._get_ldapuserfolder()
        result = ldapuserfolder.manage_editUser(self._build_dn(uid), kwargs={
            'mail': form_data['email'],
            'labeledURI': form_data['uri'],
            'o': form_data['organisation'],
            'postalAddress': form_data['postal_address'],
            'telephoneNumber': form_data['telephone_number'],
        })
        
        if result:
            if REQUEST:
                return self._result_page(errors=['Error: %s' % result])
            else:
                return 'error: %s' % result
        
        if REQUEST:
            return self._edit_account(message='Personal information successfully'
                    ' updated for user "%s".' % uid, form_data=form_data)
    
    # change password
    _change_password = PageTemplateFile('zpt/change_password', globals())
    
    security.declarePublic('change_password')
    def change_password(self, uid=None, old_password=None, new_password=None, new_password_confirm=None, REQUEST=None):
        """ Change the password of an LDAP account """
        if REQUEST.REQUEST_METHOD == 'GET':
            uid = self._get_logged_in_user().getProperty('uid')
            return self._change_password(form_data={'uid': uid})
        
        if not self._check_user_password(uid, old_password):
            error = 'old password is wrong'
            if REQUEST:
                return self._change_password(error=error, form_data={'uid': uid})
            else:
                return error
        
        if REQUEST and new_password != new_password_confirm:
            return self._change_password(error='passwords must match!',
                    form_data={'uid': uid})
        
        err_msg = self._change_account_password(uid, new_password)
        
        if err_msg:
            error = 'Password change failed: %s' % err_msg
            if REQUEST:
                return self._result_page(errors=[error])
            return error
        if REQUEST:
            return self._change_password(message='Password successfully '
                    'changed for account "%s".' % uid, form_data={'uid': uid})
    
    # forgot password
    _recover_password = PageTemplateFile('zpt/recover_password', globals())
    
    security.declarePublic('do_recover_password')
    def recover_password(self, uid=None, email=None, REQUEST=None):
        """ Recover the password of an LDAP account """
        if REQUEST.REQUEST_METHOD == 'GET':
            return self._recover_password()
        
        ldapuserfolder = self._get_ldapuserfolder()
        
        error = None
        if uid:
            result = ldapuserfolder.findUser('uid', uid, exact_match=True)
            if not result:
                error = 'Username "%s" not in database' % uid
        
        elif email:
            result = ldapuserfolder.findUser('mail', email, exact_match=True)
            if not result:
                error = 'E-mail address "%s" not in database' % email
        
        else:
            error = 'Please enter username or email'
        
        if error:
            if REQUEST:
                return self._recover_password(error=error)
            else:
                return error
        
        self._clean_auto_expire_list()
        for account in result:
            key = random_sha_b64()
            reset_url = "%s/reset_password?key=%s" % (self.absolute_url(), key)
            
            subject = 'Reset password for Eionet account "%s"' % account['uid']
            body = unicode(self.password_reset_template) \
                        .replace('${NAME}', account['cn'].decode('utf-8')) \
                        .replace('${UID}', account['uid']) \
                        .replace('${LINK}', reset_url) \
                        .replace('${EMAIL}', account['mail'])
            
            try:
                self._send_mail(msg_to=account['mail'], msg_subject=subject, msg_body=body)
            except Exception, e:
                error = 'Error sending email: %s' % str(e)
                if REQUEST:
                    return self._result_page(errors=[error])
                else:
                    return error
            
            self._add_to_auto_expire_list(key, 'pwreset', account['uid'])
        
        if REQUEST:
            return self._result_page(messages=[
                    'An e-mail has been sent to your address. Follow the '
                    'instructions in that message to recover your password'])
    
    # reset password
    security.declarePublic('reset_password')
    def reset_password(self, key, REQUEST=None):
        """ Reset a password, if the key matches """
        uid = self._search_auto_expire_list(key, 'pwreset')
        
        if not uid:
            if REQUEST:
                return self._result_page(errors=[
                        ('The reset key did not verify. '
                        'Please <a href="%s/recover_password">try again</a> '
                        'or contact the administrator.') % self.absolute_url()
                    ])
            else:
                return 'error verifying key'
        
        new_password = random_sha_b64()[:8]
        result = self._change_account_password(uid, new_password)
        
        if REQUEST:
            if result:
                return self._result_page(errors=['Error: %s' % result])
            else:
                return self._result_page(messages=[
                    'the password has been reset; your new password is "%s"' % new_password])
        else:
            return result

InitializeClass(EionetLDAP)
