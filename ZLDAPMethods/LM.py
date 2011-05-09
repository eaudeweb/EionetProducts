# core of LDAP Filter Methods.


__version__ = "$Revision: 1.10 $"[11:-2]

try:
    import ldap              # see if it's on a regular path
except ImportError:
    from Products.ZLDAPConnection import ldap

from Shared.DC.ZRDB import Aqueduct
from Shared.DC.ZRDB.Aqueduct import parse, default_input_form
import Acquisition, Globals, AccessControl.Role, OFS.SimpleItem
from Globals import HTMLFile, MessageDialog
import DocumentTemplate
import sys
try:
    from AccessControl import getSecurityManager
except ImportError:
    getSecurityManager = None

class Filter(DocumentTemplate.HTML):
    """
    Subclass of DocumentTemplate.HTML for Variable Interpolation.
    Special LDAP Specific tags would go here.  Since there aren't
    any (like ldapvar or ldaptest or whatever), we don't have to worry.
    It's just nice to have a nice name that reflects what this is. :)
    """#"
    pass


def LDAPConnectionIDs(self):
    """find LDAP connections in the current folder and parents
    Returns list of ids.
    """
    ids={}
    StringType = type('')
    have_key = ids.has_key
    while self is not None:
        if hasattr(self, 'objectValues'):
            for o in self.objectValues():
                if (hasattr(o,'_isAnLDAPConnection')
                    and o._isAnLDAPConnection() and hasattr(o,'id')):
                    id=o.id
                    if type(id) is not StringType: id=id()
                    if not ids.has_key(id):
                        if hasattr(o,'title_and_id'): o=o.title_and_id()
                        else: o=id
                        ids[id]=id
        if hasattr(self, 'aq_parent'): self=self.aq_parent
        else: self=None
    ids=map(lambda item: (item[1], item[0]), ids.items())
    ids.sort()
    return ids

manage_addZLDAPMethodForm = HTMLFile('add', globals())

def manage_addZLDAPMethod(self, id, title, connection_id, scope, basedn,
                          filters, arguments, getfromconnection=0,
                          REQUEST=None, submit=None):
    """Add an LDAP Method """
    l=LDAPFilter(id, title, connection_id, scope, basedn,
                 arguments, filters)
    self._setObject(id, l)
    if getfromconnection:
        getattr(self,id).recomputeBaseDN()

    if REQUEST is not None:
        u=REQUEST['URL1']
        if submit==" Add and Edit ":
            u="%s/%s/manage_main" % (u,id)
        elif submit==" Add and Test ":
            u="%s/%s/manage_testForm" % (u,id)
        else:
            u=u+'/manage_main'

        REQUEST.RESPONSE.redirect(u)
    return ''

_ldapScopes = { "ONELEVEL": ldap.SCOPE_ONELEVEL,
                "SUBTREE": ldap.SCOPE_SUBTREE,
                "BASE": ldap.SCOPE_BASE }

class LDAPFilter(Aqueduct.BaseQuery,
    Acquisition.Implicit,
    Globals.Persistent,
    AccessControl.Role.RoleManager,
    OFS.SimpleItem.Item,
    ):
    'LDAP Filter Method'

    meta_type = 'LDAP Filter'

    manage_main = HTMLFile('edit', globals())
    manage_options = (
        {'label':'Edit', 'action':'manage_main'},
        {'label':'Test', 'action':'manage_testForm'},
        {'label':'Security', 'action':'manage_access'},
        )

    __ac_permissions__=(
        ('View management screens', ('manage_tabs','manage_main',),),
        ('Change LDAP Methods', ('manage_edit',
                                 'manage_testForm','manage_test')),
        ('Use LDAP Methods',    ('__call__',''), ('Anonymous','Manager')),
        )


    #manage_testForm = HTMLFile("testForm", globals())

    def manage_testForm(self, REQUEST):
        " "
        input_src=default_input_form(self.title_or_id(),
                                     self._arg, 'manage_test',
                                     '<!--#var manage_tabs-->')
        return DocumentTemplate.HTML(input_src)(self,REQUEST,HTTP_REFERER='')

    def __init__(self, id, title, connection_id, scope, basedn,
                 arguments, filters):
        """ init method """
        self.id = id
        self.title = title
        self.connection_id = connection_id
        self._scope = _ldapScopes[scope]
        self.scope = scope
        self.basedn = basedn
        self.arguments_src=self.arguments=arguments
        self._arg=parse(arguments)
        self.filters = filters


    def recomputeBaseDN(self):
        ' recompute base DN based on connection '
        cdn=self._connection().dn
        if self.basedn:
            self.basedn='%s, %s' % (self.basedn, cdn)
        else:
            self.basedn=cdn
        return self.basedn

    def manage_edit(self, title, connection_id, scope, basedn,
                    arguments, filters, REQUEST=None):
        """ commit changes """
        self.title = title
        self.connection_id = connection_id
        self._scope = _ldapScopes[scope]
        self.scope = scope
        self.basedn = basedn
        self.arguments_src=self.arguments=arguments
        self._arg=parse(arguments)
        self.filters = filters
        if REQUEST is not None:
            return MessageDialog(
                title='Edited',
                message='<strong>%s</strong> has been changed.' % self.id,
                action ='./manage_main', )

    def cleanse(self,s):
        import string
        # kill line breaks &c.
        s = string.join(string.split(s))
        return s

    def _connection(self):
        ' return actual ZLDAP Connection Object '
        if hasattr(self,'connection_id') and hasattr(self,self.connection_id):
            return getattr(self, self.connection_id)

    def _getConn(self):
        return self._connection().GetConnection()

    # Hacky, Hacky
    GetConnection=_getConn


    def manage_test(self, REQUEST):
        """ do the test query """
        src="Could not render the filter template!"
        res=()
        t=v=tb=None
        try:
            try:
                src=self(REQUEST, src__=1)
                res=self(REQUEST, tst__=1)
                r=self.prettyResults(res)
            except:
                t, v, tb = sys.exc_info()
                r='<strong>Error, <em>%s</em>:</strong> %s' % (t,v)

            report=DocumentTemplate.HTML(
                '<html><body bgcolor="#ffffff">\n'
                '<!--#var manage_tabs-->\n<hr>%s\n\n'
                '<hr><strong>Filter used:</strong><br>\n<pre>\n%s\n</pre>\n<hr>\n'
                '</body></html>' % (r, src)
                )
            report=apply(report,(self,REQUEST),{self.id:res})

            if tb is not None:
                self.raise_standardErrorMessage(
                    None, REQUEST, t, v, tb, None, report)

            return report

        finally: tb=None

    def prettyResults(self, res):
        s = ""
        if not res or not len(res):
            s = "no results"
        else:
            for dn,attrs in res:
                s = s + ('<ul><li><b>DN: %s</b></li>\n<ul>' % dn)
                s = s + str(pretty_results(attrs=attrs.items()))
                s = s + '</ul></ul>'
        return s

    def __call__(self, REQUEST=None, src__=0, tst__=0, **kw):
        """ call the object """
        if REQUEST is None:
            if kw: REQUEST = kw
            else:
                if hasattr(self, 'REQUEST'): REQUEST=self.REQUEST
                else: REQUEST={}

        c = self._getConn()
        if not c:
            raise "LDAPError", "LDAP Connection not open"

        if hasattr(self, 'aq_parent'):
            p = self.aq_parent
        else: p = None

        argdata = self._argdata(REQUEST)  #use our BaseQuery's magic.  :)

        # Also need the authenticated user.
        auth_user = REQUEST.get('AUTHENTICATED_USER', None)
        if auth_user is None:
            auth_user = getattr(self, 'REQUEST', None)
            if auth_user is not None:
                try: auth_user = auth_user.get('AUTHENTICATED_USER', None)
                except: auth_user = None

        if auth_user is not None:
            if getSecurityManager is None:
                # working in a pre-Zope 2.2.x instance
                from AccessControl.User import verify_watermark
                verify_watermark(auth_user)
                argdata['AUTHENTICATED_USER'] = auth_user


        f = Filter(self.filters)        # make a FilterTemplate
        f.cook()
        if getSecurityManager is None:
            # working in a pre-Zope 2.2 instance
            f = apply(f, (p,argdata))       #apply the template
        else:
            # Working with the new security manager (Zope 2.2.x ++)
            security = getSecurityManager()
            security.addContext(self)
            try:     f = apply(f, (p,), argdata)  # apply the template
            finally: security.removeContext(self)

        f = str(f)                      #ensure it's a string
        if src__: return f              #return the rendered source
        f = self.cleanse(f)

        ### run the search
        res = c.search_s(self.basedn, self._scope, f)
        if tst__: return res            #return test-friendly data

        ### instantiate Entry objects based on results
        l = []                          #list of entries to return
        conn=self._connection()         #ZLDAPConnection
        Entry = conn._EntryFactory()
        for dn, attrdict in res:
            e = Entry(dn, attrdict, conn).__of__(self)
            l.append(e)

        return l


class LDAP(LDAPFilter):
    "backwards compatibility.  blech. XXX Delete Me!"

pretty_results=DocumentTemplate.HTML("""\
  <table border="1" cellpadding="2" cellspacing="0" rules="rows" frame="void">
   <dtml-in attrs>
    <tr valign="top">
     <th align="left">&dtml-sequence-key;</th>
     <td><dtml-in name="sequence-item">&dtml-sequence-item;<br /></dtml-in></td>
    </tr>
   </dtml-in>
  </table>""")


#import Globals
#Globals.default__class_init__(LDAPFilter)
