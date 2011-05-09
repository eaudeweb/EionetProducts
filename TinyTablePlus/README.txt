
TinyTablePlus is a product designed to manage a small amount of
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

Shane's mods
      
        There are four new methods, a change in the specification
        of column names, and minor mods throughout.
        These changes make it possible to use
        TinyTablePlus as a small database table, which can be very
        useful in a variety of situations.  It is recommended, however,
        that TinyTablePlus only be used this way when accessed through
        a DatabaseConnector, so that a better implementation can
        be swapped in easily.

        1. setRow(columnName=value, ...):

            setRows allows you to set the data in the table.  If there
            are any "key" columns, it will try to match the key columns
            and update a row.  If there are no key columns or the
            values in the key are not matched by any row, a new row
            will be added.  See the explanation for key columns below.

        2. delRows(columnName=value, ...):

            Deletes all rows that match the filter.

        3. delAllRows():

            Deletes all rows.

        4. getRows(columnName=value, ...):

            A synonym for the query interface.  Using the getRows()
            method is sometimes easier to read in DTML or Python
            code.

  Key columns

        In a real database, key columns let you specify columns that
        can uniquely identify a record.  If you try to add a row with
        values in the key column that are the same as the corresponding
        values in a row that already exists, the database will reject
        the new row.

        TinyTablePlus takes a less formal approach and only pays
        attention to key columns in the 'setRow()' method.  'setRow()'
        is a combination of both "insert" and "update" operations.
        It tries to find a row with the specified values in the
        key columns, and if found will update that row.  It will
        ignore any other rows that happen to match.

        To specify which columns in the table are key columns,
        add an asterisk after the column name.  For example::

          login* name email birthdate

        A table that uses those column names might have the following
        data::

          "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
          "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "1/1/70"

        Because the 'login' column is a key column, the following call::

          setRow(login='eliza', birthdate='unknown')

        ...would change the table data to::

          "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
          "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "unknown"

        'setRow()' found a row that matched all specified key
        columns and changed that row rather than add a new row.
        Note that more than one key column is possible.
        The following call::

          setRow(login='harry', name='Harry Chaste', birthdate='1/1/00',
          email='unknown')

        ...would add to the table a new row since there is no
        row with the value of "harry" in the 'login' column.  The
        table would look like this::

          "joe", "Joe Brown", "jbrown@xyz.com", "10/12/66"
          "eliza", "Eliza Weizenbaum", "eliza@univ.edu", "unknown"
          "harry", "Harry Chaste", "unknown", "1/1/00"

        Please keep in mind that TinyTablePlus does *not* scale well.
        It is very useful for reference implementations of a database,
        but don't use it in the final version your new e-commerce product.
        I (Shane) have no intention of improving its scaleability
        because that is the need that DatabaseAPI / DatabaseConnector
        (a product which I wrote myself) is intended to address.
        


$Endicor: README.txt,v 1.2 1999/04/25 23:05:09 tsarna Exp $

TinyTable License

  Copyright (c) 1998-1999 Endicor Technologies, Inc.
  All rights reserved. Written by Ty Sarna &lt;tsarna@endicor.com&gt;
  Renamed from TinyTable to TinyTablePlus and modified by
  Shane Hathaway. (April 2000)

  Redistribution and use in source and binary forms, with or without
  modification, are permitted provided that the following conditions
  are met:

  1. Redistributions of source code must retain the above copyright
     notice, this list of conditions and the following disclaimer.

  2. Redistributions in binary form must reproduce the above copyright
     notice, this list of conditions and the following disclaimer in the
     documentation and/or other materials provided with the distribution.

  3. The name of the author may not be used to endorse or promote products
     derived from this software without specific prior written permission

  THIS SOFTWARE IS PROVIDED BY THE AUTHOR ``AS IS'' AND ANY EXPRESS OR
  IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE IMPLIED WARRANTIES
  OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED.
  IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR ANY DIRECT, INDIRECT,
  INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT
  NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
  DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
  THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
  (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF
  THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.


