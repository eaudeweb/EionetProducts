#
#	$Endicor: __init__.py,v 1.5 1999/01/10 23:09:51 tsarna Exp $
#
# Copyright (c) 1998-1999 Endicor Technologies, Inc.
# All rights reserved. Written by Ty Sarna <tsarna@endicor.com>
# Small mods by Shane Hathaway. (13 April 2000)
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
# 1. Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. The name of the author may not be used to endorse or promote products
#    derived from this software without specific prior written permission
#
# THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
# IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
# OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
# IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
# NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
# THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#

__doc__="""TinyTablePlus initialization

$Endicor: __init__.py,v 1.5 1999/01/10 23:09:51 tsarna Exp $"""

__version__="$Revision: 1.5 $"[11:-2]

######################### Imported Modules #########################

from ImageFile import ImageFile
import TinyTablePlus

######################### Metadata #########################

# Names of objects added by this product:
meta_types = (
    {
        "name":     "TinyTablePlus",            # The name of the object type
        "action":   "manage_addTinyTablePlusForm", # The method to add one.
    },
)

# Attributes (usually "methods") to be added to folders to support
# creating objects:
methods = {
    "manage_addTinyTablePlusForm":  TinyTablePlus.addItemForm,
    "manage_addTinyTablePlus":      TinyTablePlus.addItem,
}

# Permission to be added to folders:
__ac_permissions__ = (
    # To add items:
    ("Add TinyTablePlus",
    ("manage_addTinyTablePlusForm", "manage_addTinyTablePlus")),

    # To manipulate item permissions at a high level.  Note that the
    # list of objects is empty, since we are just providing a place
    # to put acquired settings:
    ("Change TinyTable", ()),
    ("Query TinyTable Data", ()),
)

# Define shared web objects that are used by products.
# This is usually (always ?) limited to images used 
# when displaying an object ub contents lists.
# These objects are accessed as:
#   <!--#var SCRIPT_NAME-->/misc_/Product/name
misc_ = {
    "icon":   ImageFile("icon.gif", globals()),
    "logo":   ImageFile("Endicor.gif", globals()),
}
