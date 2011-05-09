#
#	$Endicor: ImportExport.py,v 1.3 1999/04/27 17:25:44 tsarna Exp $
#
# Copyright (c) 1998-1999 Endicor Technologies, Inc.
# All rights reserved. Written by Ty Sarna <tsarna@endicor.com>
# Modified by Shane Hathaway. (April 2000)
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

"""Import and Export data from TinyTablePlus to human readable CSV-type text"""

import string, token, tokenize, cStringIO, Missing
from types import *

FormatError = "Invalid Data Format"

class ImportDataState:
    def __init__(self):
        self.rows = []
        self.row = []
        self.value = Missing.Value
        self.seenvalue = self.sign = 0
        self.lasttok = tokenize.ENDMARKER

    def token(self, t, s, src, erc, l):
        estr = "at line %d column %d" % src
        signerr = "<strong>Already have sign %s</strong>" % estr
        invtok = "<strong>invalid token %s %s</strong>" % (`s`, estr)
        
        if t == token.OP:
            if  s == ',':
                self.row.append(self.value)
                self.value = Missing.Value
                self.seenvalue = self.sign = 0
            elif s == '+':
                if self.seenvalue or self.sign:
                    raise FormatError, signerr
                self.sign = 1
            elif s == '-':
                if self.seenvalue or self.sign:
                    raise FormatError, signerr
                self.sign = -1                
            else:
                raise FormatError, invtok

        elif t == token.NAME:
            if string.upper(s) in ('NONE', 'NULL'):
                if self.seenvalue or self.sign:
                    raise FormatError, invtok

                self.value = Missing.Value
                self.seenvalue = 1
            else:
                if self.seenvalue:
                    if type(self.value) == StringType:
                        self.value = self.value + ' ' + s
                    else:
                        raise FormatError, invtok
                else:
                    self.value = s
                    self.seenvalue = 1

        elif t == token.STRING:
            if self.seenvalue or self.sign:
                raise FormatError, invtok
            
            self.value = eval(s)
            self.seenvalue = 1

        elif t == token.NUMBER:
            if self.seenvalue:
                raise FormatError, invtok
            
            self.value = eval(s)
            if self.sign < 0:
                self.value = -self.value
            self.seenvalue = 1

        elif t in (token.NEWLINE, tokenize.ENDMARKER):
            if t == tokenize.NEWLINE or self.lasttok != token.NEWLINE:
                self.row.append(self.value)
                self.seenvalue = self.sign = 0
                self.value = Missing.Value
                self.rows.append(self.row)
                self.row = []

        elif t in (tokenize.COMMENT, tokenize.NL):
            pass
            
        else:
            raise FormatError, invtok

        self.lasttok = t


def ImportData(s):
    if len(s) < 1:
        # Patch by Shane, April 2000 - Check for empty data set.
        return []
    f = cStringIO.StringIO(s)
    i = ImportDataState()
    tokenize.tokenize(f.readline, i.token)
    return i.rows


# translate specialcharacter to escaped form
cval = {
    '\\'    :   '\\\\',
    '\"'    :   '\\\"',
    '\a'    :   '\\a',
    '\b'    :   '\\b',
    '\f'    :   '\\f',
    '\n'    :   '\\n',
    '\r'    :   '\\r',
    '\t'    :   '\\t',
    '\v'    :   '\\v'
}

    
def ExportVal(data):
    t = type(data)
    
    if data is Missing.Value:
        return "NULL"
    elif data is Missing.Value:
        return "NULL"
    elif t in (IntType, FloatType, LongType):
        return str(data)
    elif t is StringType:
        s = '"'
        for c in data:
            if cval.has_key(c):
                s = s + cval[c]
            elif ord(c) <= 31 or ord(c) >= 127:
                s = s + '\\%03o' % ord(c)
            else:
                s = s + c
        return s + '"'
    else:
        return '"' + str(data) + '"'


def ExportData(data):
    return string.join(
        map(
            lambda row: string.join(
                map(ExportVal, row),
                ', '
            ),
            data
        ),
        '\n'
    )
