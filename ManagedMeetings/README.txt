<h3>Introduction</h3>

The ManagedMeetings product lets you administer meetings.
You can announce meetings based on different criteria, let
people sign up and send email to all participants.
The event is available as <a href="http://www.imc.org">vCalendar</a>
so people can just click on a link to import it into their PIM.

<h3>Installation</h3>

This is a Python Product.
Installation is very simple. Download the tgz file. Put it in the
Products directory and do tar xzvf ManagedMeetings-x.x.tgz. If you
haven't done already, create a MailHost and read the README file in the
product. Restart zope and you will now be able to create objects of the
"Meeting" type.  If you want to use the authenticated registration
you must be prepared to do some moderate programming as I have no way
of knowing how your directory of users is set up.  Beware that it was
developed on Zope 2.3.x and probably doesn't run on Zope versions older
than that.

If you also install the MessageBoard product produced by EEA, then
ManagedMeetings will automatically create a discussion list for the
participants when you create new meetings. If you don't want a
discussion list, you simply remove it afterwards.

<h3>How to Use</h3>

Create a 'Folder for Meetings' for your meetings/training
courses/conferences or use a folder you already have. Set the mail_enconding property 
to reflect your website's pages encoding. If empty iso-8859-1 is consider. To list your
meetings, you can use the created <i>index_html</i> or roll your own list.
Then you create objects of the type 'Meeting' in the folder.  It will
ask you to fill out some fields, and then you have a meeting folder.
If you have material to share you can put it in the folder.  You will
also notice that you can now create attendees inside the meeting folder.

<h3>Features</h3>

There are three ways a person can be added the participant list.

<ol><li>The meeting administrator can add him/her. This mainly occurs
when the person phones or faxes his request to attend to the
administrator. This is usually considered verified.</li>
<li>The person can registrer through a form on the meeting
information page. Since anybody can do this for anybody,
the administrator should normally verify the person's intent
by called him back.</li>
<li>This person can do an authenticated sign up, if he exists in
the acl_users folder. The benefit is that all the details are
filled out for the user and all he has to do is submit the form.
Since the person is authenticated we can consider him verified.</li>
</ol>

For details about allowing users to register for meetings, see the 
'Security Issues' section.

If you need to ask more questions of each attendee, such as which
hotel they want to stay in, you can add a "Default Attendee Properties"
object to the meeting. Then these questions will get asked when the user
registers.

<h3>Authenticated Sign Up</h3>

The product allows authenticated sign up by querying our site directory,
which is LDAP-based. It is not likely that you have the same configuration,
so I will show you how to modify the code.

First of all, all interaction with the sitedirectory is through a method
called <i>sitedir_lookup</i>. (not supplied). It expects one argument,
the variable <tt>userid</tt>. That matches the name the user enters in
the login dialog.  You can quite easily replace that with a Z SQL method
if you so desire.

There are two methods that call <i>sitedir_lookup</i>.
One is <i>authenticatedsignup.dtml</i>. It expects the fields returned from
sitedir_lookup to have certain names. For instance, the surname is called
<i>sn</i>. It is pretty obvious what is what. If your table doesn't use
the same names then you must modify the source of <i>ManagedMeetings</i>.
Alternatively you can replace <i>authenticatedsignup.html</i> with
<i>authenticatedregister.html</i>. That methods doesn't look in
the site directory, so the user must enter all fields. But it does
require login and hence the registration is considered verified.

The other method is <i>SendEmail</i>. It requires you to log in and then
looks up your email address in the site directory. You can change the
form to ask for the sender address if you can't get it from a database.

<h3>Security Issues</h3>

The security for this product is a bit tricky. You want people to
be able to sign up unauthenticated, but you also want to request
a username and password from people that use the authenticated
registration.
The way to do it is to let anybody with the View-permission create
an Attendee instance. Then require the 'Authenticated Registration' attribute
of a Meeting abject for authenticated registration.

Then you create a role that everybody you want to be able to register and let that
role have the 'Register for Meetings' permission (of course, you can use an existing 
role or give this permission to Anonymous in the case you want to allow public 
registration).

<h3>Something to do Some Time Later</h3>

 Provide a way to send out invitations. This would require more integration
with the site directory so the administrator can search the potential
participants on several criteria.<br>
 Negotiation of meeting time between the participants.<br>
 It should be possible to delegate the upload of background material to all
meeting participants.<br>
 Send out automatic notification to everybody if meeting date changes.<br>
 Email the vCalendar entry to all attendees.<br>
<i>For more ideas, read this <a href="http://www.zope.org/Members/EIONET/ManagedMeetings/specs.html">Specifications</a>
document...</i>

<h3>License</h3>

The contents of this file are subject to the Mozilla Public
License Version 1.1 (the "License"); you may not use this file
except in compliance with the License. You may obtain a copy of
the License at http://www.mozilla.org/MPL/

Software distributed under the License is distributed on an "AS
IS" basis, WITHOUT WARRANTY OF ANY KIND, either express or
implied. See the License for the specific language governing
rights and limitations under the License.

The Original Code is ManagedMeetings version 1.0.

The Initial Owner of the Original Code is European Environment
Agency (EEA).  Portions created by CMG and Finsiel Romania are
Copyright (C) European Environment Agency.  All
Rights Reserved.
