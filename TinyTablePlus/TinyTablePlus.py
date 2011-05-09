#
# $Endicor: TinyTablePlus.py,v 1.28 1999/04/26 22:06:55 tsarna Exp $
#
# Copyright (c) 1998-1999 Endicor Technologies, Inc.
# All rights reserved. Written by Ty Sarna <tsarna@endicor.com>
#
# Mods and change of name from "TinyTable" to "TinyTablePlus"
# by Shane Hathaway. (13 April 2000)
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
__doc__='''Tiny Table data manager product

$Endicor: TinyTablePlus.py,v 1.28 1999/04/26 22:06:55 tsarna Exp $'''

__version__='$Revision: 1.28 $'[11:-2]

######################### Imported Modules #########################

from Globals import HTMLFile, MessageDialog, Persistent
from Shared.DC.ZRDB.Results import Results
from persistent.mapping import PersistentMapping
from DateTime import DateTime
from App.Extensions import getBrain
import OFS.ObjectManager, OFS.SimpleItem, Acquisition, AccessControl.Role
import Record, Missing, string, types
import ImportExport

######################### Folder Methods #########################

addItemForm=HTMLFile('Add', globals())
def addItem(self, id, title='', columns='', REQUEST=None):
    """Add a TinyTablePlus to a folder

    The argument 'self' will be bound to a folder.

    The arguments, 'id' and 'title' are minimal, and most applications
    will have additional needed arguments.
    """
    self._setObject(id, TinyTablePlus(id, title, columns))
    if REQUEST is not None: return self.manage_main(self,REQUEST)

######################### Helper Functions #########################

IntValued = 'i'
LongValued = 'l'
FloatValued = 'n'
StringValued = 's'
DateTimeValued = 'd'
DateValued = 'D'

TypeNames = {
    IntValued : ':int',
    LongValued : ':long',
    FloatValued : ':float',
    StringValued : '',
    DateTimeValued : ':datetime',
    DateValued : ':date'
}

def TypeCode(t):
    if t == LongValued:
        return 'i'
    elif t == DateValued:
        return 'd'
    else:
        return t

def CoerceType(x, t):
    if x is Missing.Value:
        return x
    elif t == IntValued:
        if type(x) == type(0.0):
            return int(x)
        if type(x) != type(0):
            if (type(x) != type('')):
                x = str(x)

            try:
                x = string.atoi(x)
            except:
                x = 0
        return x
    elif t == LongValued:
        if type(x) != type(0L):
            if (type(x) != type('')):
                x = str(x)

            try:
                x = string.atol(x)
            except:
                x = 0L
        return x
    elif t == FloatValued:
        if type(x) != type(0.0):
            if (type(x) != type('')):
                x = str(x)

            try:
                x = string.atof(x)
            except:
                x = 0.0
        return x
    elif t == DateTimeValued:
        if not (type(x) == types.InstanceType and x.__class__ == DateTime):
            try:
                x = DateTime(x)
            except:
                x = Missing.Value
        return x
    elif t == DateValued:
        if not (type(x) == types.InstanceType and x.__class__ == DateTime):
            try:
                # force date-only
                x = DateTime(x)
            except:
                x = Missing.Value
        return DateTime(x.Date())
    else:
        return str(x)

######################### TinyTablePlus Class #########################

class TinyTablePlus(
    OFS.SimpleItem.Item,
    Persistent,
    Acquisition.Implicit,
    AccessControl.Role.RoleManager,
    ):
    """TinyTablePlus is a product designed to manage a small amount of
tabular data.  It's intended to fill the gap between a Z Table or an Z
SQL Methods accessed SQL table, which are overkill for many tasks, and
folder token properties, which allow only a single "column".  TinyTablePlus
also makes it possible to look up an item within the list, or to return
a subset of the list rows where columns equal particular values.

TinyTablePlus Properties

  Columns

    *Columns* is a list of one or more column names separated by
    spaces. Columns are string-typed by default, but may optionally
    be integers, long integers, floating-point, or DateTime if the
    column name is suffixed with ':int', ':long', ':float', or ':date'
    or ':datetime' respectively.  ':date' and ':datetime' both store
    Zope DateTime values, but ':date' values are forced to be date-only,
    with no time-of-day information.

    The first column is special. An index will be built on this
    column for "lookup" use (see below). The index built is unique.
    That is, if there are multiple rows with the same first-column
    value, only one row will appear in the index, and only one row
    will be returned from an index query. If this is a problem, use
    a filter on the first row instead (see below).

  Data

    The data consists of newline-separated rows containing columns
    separated by commas.  Any input data will be adjusted to conform to
    the column specification.  If the row contains too many columns the
    excess will be trimmed.  If the row contains to few columns, columns
    containing NULL will be added.  String values in a column specified
    to take a number will be replaced by 0.
    
    The form of values is similar to Python syntax. Strings are enclosed
    in single or double quotes, and backslash escapes are possible.
    Numbers may be entered just as in Python.  Full Python syntax for
    floating point numbers is supported, including exponent notation. 
    Dates and Date-Times are represented by strings in any of the
    formats thet the Zope DateTime class understands.  Missing (NULL)
    may also be given as a value for a cell, by using 'NULL' or 'None',
    or by simply omitting the value (for example, 1,,3' is treated as
    '1,NULL,3')

    Python comments ('#') and line continuations may also be used.
    Note, however, that once TinyTablePlus extracts the data from the input
    text, the text is thrown away.  When visiting the management edit
    interface again, the text will be regenerated from the stored data.
    Comments, blank lines, line continuations, and such will all be lost
    since they don't alter the data itself.
    
  Querying a TinyTablePlus

    Assume you have a table named MyTable. It has these properties:

    Columns::

      last first middle n:int x:long

    and the following data::

      "smith", "john", "x", 0, 0L
      "smith", "bob", "x", 0, 0L
      "smith", "bob", "z", 0, 0L
      "jones", "bob", "y", 0, 0L
      "jones", "john", "y", 0, 0L
      "jones", "john", "z", 0, 0L 

    The data can be queried from DTML in several ways:

      Full Query::

        <!--#in MyTable-->

        Iterates through all rows of the TinyTablePlus. Within the
        region contained by 'in' tag, the column names will be
        available as variables and so can be insterted. For
        example on the first iteration, '<!--#var first-->' will
        be replaced with 'john'.

      Index Query::

        <!--#in "MyTable('jones')"-->

        The passed argument will be looked up in the table's
        index of the first column. Because the index is unique,
        either zero (if no matching rows) or one (if any
        matching rows) rows will be iterated through. In this
        case, any *one* of the three rows with a last name of
        'jones' could be returned. The choice of which row is
        returned when multiple rows have the same index value is
        unspecified.

      Filter Query::

        <!--#in "MyTable(last='jones')"-->
        <!--#in "MyTable(first='john')"-->
        <!--#in "MyTable(last='jones', middle='y')"-->

        When one or more named arguments is given, a filter
        query is performed. Each argument name must be the name
        of a column, and the corresponding value is compared
        against that column in each row. Only matching rows are
        returned. The first example above, in contrast with the
        index query example, returns *all three* rows where the
        last name is 'jones'.

        While an Index Query operates only on the first column,
        a filter query can operate on any column. In the second
        exmple above, all three rows with the first name 'john'
        are returned.

        Finally, multiple filters may be specified. In this
        case only rows matching all contraints are iterated
        through. In the third example above, only the two rows
        where the last name is 'jones' and the middle initial is
        'y' will be returned.

      Shane's mods:
      
        There are four new methods, a change in the specification
        of column names, and minor mods throughout.
        These changes make it possible to use
        TinyTablePlus as a small database table, which can be very
        useful in a variety of situations.  It is recommended, however,
        that TinyTablePlus only be used this way when accessed through
        a DatabaseConnector, so that a better implementation can
        be swapped in easily.

        1. setRow(columnName=value, ...)

            setRows allows you to set the data in the table.  If there
            are any 'key' columns, it will try to match the key columns
            and update a row.  If there are no key columns or the
            values in the key are not matched by any row, a new row
            will be added.  See the explanation for key columns below.

        2. delRows(columnName=value, ...)

            Deletes all rows that match the filter.

        3. delAllRows()

            Deletes all rows.

        4. getRows(columnName=value, ...)

            A synonym for the query interface.  Using the getRows()
            method is sometimes easier to read in DTML or Python
            code.

        Key columns:

        In a real database, key columns let you specify columns that
        can uniquely identify a record.  If you try to add a row with
        values in the key column that are the same as the corresponding
        values in a row that already exists, the database will reject
        the new row.

        TinyTablePlus takes a less formal approach and only pays
        attention to key columns in the setRow() method.  setRow()
        is a combination of both 'insert' and 'update' operations.
        It tries to find a row with the specified values in the
        key columns, and if found will update that row.  It will
        ignore any other rows that happen to match.

        To specify which columns in the table are key columns,
        add an asterisk after the column name.  For example:

        login* name email birthdate

        A table that uses those column names might have the following
        data:

        "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
        "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "1/1/70"

        Because the login column is a key column, the following call:

        setRow(login='eliza', birthdate='unknown')

        ...would change the table data to:

        "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
        "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "unknown"

        setRow() found a row that matched all specified key
        columns and changed that row rather than add a new row.
        More than one key column is possible.
        The following call:

        setRow(login='harry', name='Harry Chaste', birthdate='1/1/00',
               email='unknown')

        ...would add to the table a new row since there is no
        row with the value of 'harry' in the login column.  The
        table would look like this:

        "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
        "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "unknown"
        "harry", "Harry Chaste", "unknown", "1/1/00"

        Please keep in mind that TinyTablePlus does *not* scale well.
        It is very useful for reference implementations of a database,
        but don't use it in the final version your new e-commerce product.
        I (Shane) have no intention of improving its scaleability
        because that is the need that DatabaseAPI / DatabaseConnector
        (a product which I wrote myself) is intended to address.
        
        """

    # Specify a name for the item type:
    meta_type = 'TinyTablePlus'

    # Specify a relative URL for the icon used to display icons:
    icon = 'misc_/TinyTablePlus/icon'

    # Specify definitions for tabs:
    manage_options=(
	{"label":"Properties",  "action":"manage_main"},
	{"label":"Advanced",    "action":"manage_advancedForm"},
        {"label":"View",        "action":"manage_view"},
	{"label":"Security",    "action":"manage_access"},
	{"label":"About",       "action":"manage_about"},
	)

    # Specify how individual operations add up to "permissions":
    __ac_permissions__=(
	('View management screens', ('manage_tabs','manage_main',
	                             'manage_about','manage_advancedForm')),
	('Change permissions',      ('manage_access',)           ),
	('Change TinyTable',        ('manage_edit','manage_editData',
	                             'manage_advanced',
                                     # Added by Shane:
                                     'delRows','delAllRows','setRow',)),
	('Query TinyTable Data',    ('','index_html','manage_view','getRows')),
	)

    def __init__(self, id, title='', columns=''):
	self.id = id
        self._dataver = 1
	self._SetState(title, columns)

        self._rows = []
        self._index = PersistentMapping()
        # self._n_rows removed by Shane.  Not needed.

        self.class_name_ = self.class_file_ = ""
        self._v_brain = None

    # Provide a "View" interface:
    manage_view = HTMLFile("View", globals())

    # Provide a "About..." interface:
    manage_about = HTMLFile("About", globals())

    # Provide interface for changing properties:
    manage_main=HTMLFile('Edit', globals())
    def manage_edit(self, title, columns, REQUEST=None):
	"""Change item properties

	Note that we return people to our own interface, not to
	the folder we were in before.
	"""
        self._SetState(title, columns)

        # make existing data conform to new column specification
        self._rows = map(self._FixRow, self._rows)

        # and regenerte the index, incase the above changed any data
        self._GenerateIndex()

        return self.manage_editedDialog(REQUEST)

    def _SetState(self, title, columns):
	self.title = title

        if self._dataver < 1:
            del self.__dict__['delim_char_']

        self._DigestColumns(columns)
        self._dataver = 1

    manage_advancedForm = HTMLFile("Advanced", globals())
    def manage_advanced(self, class_name, class_file, REQUEST=None):
        """Change Advanced Settings"""
        self.class_name_, self.class_file_ = class_name, class_file
        self._v_brain = getBrain(self.class_file_, self.class_name_, 1)
        return self.manage_editedDialog(REQUEST)

    def manage_editData(self, data, REQUEST=None):
	"""Change item data"""
        newRows = ImportExport.ImportData(data)
        self._rows = map(self._FixRow, newRows)

        self._GenerateIndex()
        
        return self.manage_editedDialog(REQUEST)

    def _DigestColumns(self, column_list):
        self._col_index = PersistentMapping()
        self._col_names = []
        self._types = []
        self._items = []
        cols = string.split(column_list)
        # self._key_cols added to facilitate the setRows() method.
        self._key_cols = []

        for col in cols:
            item = PersistentMapping()
            x = string.split(col, ':')
            # Addition by SDH for specification of key_cols.
            x0 = x[0]
            if x0[-1] == '*':
                x0 = x0[0:-1]
                self._key_cols.append(x0)

            self._col_names.append(x0)
            item['name'] = x0
            t = StringValued
            if len(x) > 1:
                if x[1] == 'int':
                    t = IntValued
                elif x[1] == 'long':
                    t = LongValued
                elif x[1] == 'float':
                    t = FloatValued
                elif x[1] == 'datetime':
                    t = DateTimeValued
                elif x[1] == 'date':
                    t = DateValued
            self._types.append(t)
            item['type'] = TypeCode(t)
            self._items.append(item)

        self.n_cols = len(self._col_names)
        self.index_column = self._col_names[0]

        col_num = 0
        for col in self._col_names:
            self._col_index[col] = col_num
            col_num = col_num + 1

    def _FixRow(self, row):
        # force row to match specified number of columns
        if len(row) > self.n_cols:
            row = row[:self.n_cols]
        elif len(row) < self.n_cols:
            row = row + (self.n_cols - len(row)) * [Missing.Value]

        # Ensure correct types
        newrow = []
        for i in range(0, self.n_cols):
            newrow.append(CoerceType(row[i], self._types[i]))

        return newrow

    def _GenerateIndex(self):
        index = PersistentMapping()
        for i in range(0, len(self._rows)):
            index[self._rows[i][0]] = i
        self._index = index

    def cols_text(self):
        l = []

        for i in range(0, self.n_cols):
            # Modified by SDH for key_cols.
            name = self._col_names[i] + TypeNames[self._types[i]]
            if hasattr(self, '_key_cols') and name in self._key_cols:
                name = name + '*'
            l.append(name)

        return string.join(l, ' ')
        
    def data_text(self):
        return ImportExport.ExportData(self._rows)

    def index_html(self):
        """Returns an HTML representation of the TinyTablePlus's data"""

        s = "<table border=1><tr><th>"
        s = s + string.join(self._col_names, "</th>\n<th>") + "</th></tr>\n"
        for row in self._rows:
            s = s + "<tr><td>" + \
                string.join(map(str, row), "</td>\n<td>") + "</td></tr>\n"
        return s + "</table>"

    def _results(self, rows):
        if hasattr(self, '_v_brain'):
            brain = self._v_brain
        else:
            brain = self._v_brain = getBrain(self.class_file_, self.class_name_)
        return Results((self._items, rows), brains=brain, parent=None)

    def __call__(self, *args, **kargs):
        # print self.id, args, kargs.keys()
        if len(args) == 1:
            if self._index.has_key(args[0]):
                return self._results([self._rows[self._index[args[0]]]])
            else:
                return None
        elif len(kargs):
            rf = RowFilter(self, kargs)
            l = []

            for i in range(0, len(self._rows)):
                if rf(self._rows[i]):
                    l.append(self._rows[i])
            return self._results(l)
        else:
            return self._results(self._rows)

    # Convenience method added by Shane.
    getRows = __call__

    # The added methods by Shane Hathaway permit programatic
    # changes of the table contents.
    def delRows(self, *args, **kargs):
        '''Returns the number of rows deleted.
        '''
        if len(args) == 1:
            if self._index.has_key(args[0]):
                i = self._index[args[0]]
                if i >= 0:
                    del self._rows[i]
                    self._GenerateIndex()
                    return 1
            else:
                return 0
        elif len(kargs):
            rf = RowFilter(self, kargs)
            count = 0

            i = 0
            while i < len(self._rows):
                if rf(self._rows[i]):
                    del self._rows[i]
                    count = count + 1
                else:
                    i = i + 1
            self._GenerateIndex()
            return count
        else:
            return 0  # Don't default to deleting all rows.

    def delAllRows(self):
        '''Deletes all rows.
        '''
        count = len(self._rows)
        del self._rows[:]
        return count

    def setRow(self, *args, **kw):
        '''Adds or modifies one row.
        '''
        row = None
        willAdd = 0
        if hasattr(self, '_key_cols'):
            key_cols = self._key_cols
            if len(key_cols) > 0:
                # If key_cols is specified, we will try to
                # modify a record that matches the values of
                # the key columns.
                # First create a filter to find the specified
                # row.
                filter = {}
                for key_col in key_cols:
                    index = self._col_index[key_col]
                    if kw.has_key(key_col):
                        # Value specified in keyword args.
                        filter[index] = kw[key_col]
                    elif index < len(args):
                        # Value specified in ordered args.
                        filter[index] = args[index]
                    else:
                        filter[index] = ''
                # Now find a row that matches the filter.
                for r in self._rows:
                    found = 1
                    for index, val in filter.items():
                        if r[index] != val:
                            found = 0
                            break
                    if found:
                        # Modify this row.
                        row = r
                        break
        if row is None:
            # Create a new row.
            row = self.n_cols * [Missing.Value]
            willAdd = 1
        # Fill in the ordered arguments.
        for index in range(0, len(args)):
            row[index] = args[index]
        # Fill in the keyword arguments.
        for col_name, val in kw.items():
            if self._col_index.has_key(col_name):
                index = self._col_index[col_name]
                row[index] = val
        if willAdd:
            # Add a new row to the table.
            self._rows.append(row)
        self._GenerateIndex()
                
    
######################### Helper Classes #########################

class RowFilter:
    def __init__(self, table, rules):
        self.cols = []
        self.vals = []
        self.n_rules = 0

        for col in rules.keys():
            if table._col_index.has_key(col):
                self.cols.append(table._col_index[col])
                self.vals.append(rules[col])
                self.n_rules = self.n_rules + 1

    def __call__(self, row):
        for i in range(0, self.n_rules):
            if row[self.cols[i]] != self.vals[i]:
                return 0
        return 1
