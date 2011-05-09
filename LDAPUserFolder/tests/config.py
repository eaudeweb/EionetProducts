#####################################################################
#
# config        Configuration constants for the LDAPUserFolder
#               package unit tests.
#
# This software is governed by a license. See
# LICENSE.txt for the terms of this license.
#
#####################################################################
__version__='$Revision: 1009 $'[11:-2]


defaults = { 'title'  : 'LDAP User Folder'
           , 'server' : 'localhost:389'
           , 'login_attr' : 'cn'
           , 'uid_attr': 'cn'
           , 'users_base' : 'ou=people,dc=dataflake,dc=org'
           , 'users_scope' : 2
           , 'roles' : 'Anonymous'
           , 'groups_base' : 'ou=groups,dc=dataflake,dc=org'
           , 'groups_scope' : 2
           , 'binduid' : 'cn=Manager,dc=dataflake,dc=org'
           , 'bindpwd' : 'mypass'
           , 'binduid_usage' : 1
           , 'rdn_attr' : 'cn'
           , 'local_groups' : 0
           , 'implicit_mapping' : 0
           , 'use_ssl' : 0
           , 'encryption' : 'SHA'
           , 'read_only' : 0
           }

alternates = { 'title'  : 'LDAPUserFolder'
             , 'server' : 'localhost:1389'
             , 'login_attr' : 'uid'
             , 'uid_attr': 'uid'
             , 'users_base' : 'ou=people,dc=type4,dc=org'
             , 'users_scope' : 0
             , 'roles' : 'Anonymous, SpecialRole'
             , 'groups_base' : 'ou=groups,dc=type4,dc=org'
             , 'groups_scope' : 0
             , 'binduid' : 'cn=Manager,dc=type4,dc=org'
             , 'bindpwd' : 'testpass'
             , 'binduid_usage' : 2
             , 'rdn_attr' : 'uid'
             , 'local_groups' : 1
             , 'implicit_mapping' : 0
             , 'use_ssl' : 1
             , 'encryption' : 'SSHA'
             , 'read_only' : 1
             , 'obj_classes' : 'top, person, inetOrgPerson'
             }

satellite_defaults= { 'title' : 'Satellite'
                    , 'luf' : '/luftest/acl_users'
                    , 'recurse' : 0
                    , 'groups_base' : 'ou=special,dc=dataflake,dc=org'
                    , 'groups_scope' : 2
                    }

user = { 'cn' : 'test'
       , 'sn' : 'User'
       , 'mail' : 'joe@blow.com'
       , 'givenName' : 'Test'
       , 'objectClasses' : ['top', 'person']
       , 'user_pw' : 'mypass'
       , 'confirm_pw' : 'mypass'
       , 'user_roles' : ['Manager']
       , 'mapped_attrs' : {'objectClasses' : 'Objektklassen'}
       , 'multivalued_attrs' : ['objectClasses']
       , 'ldap_groups' : ['Group1', 'Group2']
       }

manager_user = { 'cn' : 'mgr'
               , 'sn' : 'Manager'
               , 'givenName' : 'Test'
               , 'user_pw' : 'mypass'
               , 'confirm_pw' : 'mypass'
               , 'user_roles' : ['Manager']
               , 'ldap_groups' : ['Group3', 'Group4']
               }

user2 = { 'cn' : 'test2'
        , 'sn' : 'User2'
        , 'mail' : 'joe2@blow.com'
        , 'givenName' : 'Test2'
        , 'objectClasses' : ['top', 'posixAccount']
        , 'user_pw' : 'mypass'
        , 'confirm_pw' : 'mypass'
        , 'user_roles' : ['Manager']
        , 'mapped_attrs' : {'objectClasses' : 'Objektklassen'}
        , 'multivalued_attrs' : ['objectClasses']
        , 'ldap_groups' : ['Group1', 'Group2']
        }

