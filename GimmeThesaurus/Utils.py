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
# Agency (EEA).  Portions created by Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Ghica, Finsiel Romania
# Cornel Nitu, Finsiel Romania
#
#$Id: Utils.py 11754 2008-09-30 10:39:27Z moregale $
# -*- coding: utf-8 -*-

__version__='$Revision: 1.7 $'[11:-2]

# python imports

#python
from types import ListType
from types import UnicodeType

# Zope imports
import zlib
from ZTUtils.Tree import b2a, a2b

class Utils:

    def __init__(self):
        """."""
        pass

    def _safe_decompress(self, input, max_size=10240):
        decomp = zlib.decompressobj()
        output = ''
        while input:
            fragment_size = max(1, (max_size-len(output))/1000)
            fragment, input = input[:fragment_size], input[fragment_size:]
            output += decomp.decompress(fragment)
            if len(output) > max_size:
                raise ValueError('Compressed input too large')
        return output + decomp.flush()

    def encodeTreeExpansion(self, expanded_nodes):
        string1 = expanded_nodes
        string1 = zlib.compress(string1)
        return b2a(string1)

    def decodeTreeExpansion(self, tree_expansion):
        string1 = a2b(tree_expansion)
        string1 = self._safe_decompress(string1)
        return string1.split(",")

    def utSplitList(self, lst):
        if lst is not ListType:
            lst = list(lst)
        #commented to correctly sort data in any language
        #lst.sort()
        if len(lst)%2 == 1:  lst.append(None)
        piv = len(lst)/2
        first = lst[:piv]
        last= lst[piv:]
        return zip(last, first)

    def utConvertToList(self, something):
        """Convert to list"""
        ret = something
        if type(something) is not ListType:
            ret = [something]
        return ret

    def utIsUnicode(self, s):
        return type(s) is UnicodeType

    def utDBError(self, s):
        return s[0].split(',')

    def utRemoveFromList(self, list, value):
        """Return a new list, after removing value v"""
        from copy import deepcopy
        res = deepcopy(list)
        try:    res.remove(value)
        except: pass
        return res

    def utTreeExpand(self, expand, node):
        return self.utJoinToList(self.utAddToList(expand, str(node)))

    def utTreeCollapse(self, expand, node):
        return self.utJoinToList(self.utRemoveFromList(expand, str(node)))
       
    def utJoinToList(self, l):
        """Gets a list and returns a comma separated string"""
        return ','.join(l)

    def utAddToList(self, l, v):
        """Return a new list, after adding value v"""
        from copy import deepcopy
        res = deepcopy(l)
        try:
            res.append(v)
        except:
            pass
        return res

    def utXmlEncode(self, s):
        """Encode some special chars"""
        tmp = s
        tmp = tmp.replace('&', '&amp;')
        tmp = tmp.replace('<', '&lt;')
        tmp = tmp.replace('"', '&quot;')
        tmp = tmp.replace('\'', '&apos;')
        tmp = tmp.replace('>', '&gt;')
        return tmp
