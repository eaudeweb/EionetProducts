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
# The Original Code is MessageBoard version 1.0.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Cornel Nitu, Rares Vernica Finsiel Romania
#

__doc__="""MessageBoard initialization module"""
__version__= '$Revision: 1.7 $'

import Message
import MessageBoard
from ImageFile import ImageFile

def initialize(context):
    """initialize: Message and Message Board"""

    context.registerClass(
            Message.Message,
            permission='Add Message',
            constructors = (
                    Message.manage_addMessageForm,
                    Message.manage_addMessage,
            ),
            icon='icons/message.gif',
    )

    context.registerClass(
            MessageBoard.MessageBoard,
            permission='Add MessageBoard',
            constructors = (
                    MessageBoard.manage_addMessageBoardForm,
                    MessageBoard.manage_addMessageBoard,
                    MessageBoard.getMailHostList
            ),
            icon='icons/board.gif',
    )

    context.registerHelp()
    context.registerHelpTitle('MessageBoard')

misc_={
    "message.gif": ImageFile("icons/message.gif",globals()),
    "attachment.gif": ImageFile("icons/attachment.gif",globals()),
    "spacer.gif": ImageFile("icons/spacer.gif",globals()),
    "line_leaf.gif": ImageFile("icons/line_leaf.gif",globals()),
    "blackline.gif": ImageFile("icons/blackline.gif",globals()),
    "previous.gif": ImageFile("icons/previous.gif",globals()),
    "next.gif": ImageFile("icons/next.gif",globals()),
}
