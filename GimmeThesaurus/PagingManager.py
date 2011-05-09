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
#$Id: PagingManager.py 11589 2008-08-20 13:26:00Z moregale $

__version__='$Revision: 1.2 $'[11:-2]

"""
    - nr_res - number of results per page
    - nbr_row - total number of items
    - cur_pos - current position in recordset
"""

# Note: the only function used outside this module is getPagingInformation; the
# PagingManager class should be removed.

def getPagingInformation(nr_res, nbr_row, cur_pos):
    return PagingManager(nr_res, nbr_row, cur_pos).getPagingInformation()

class PagingManager:

    def __init__(self, nr_res, nbr_row, cur_pos):
        """ """
        self.nr_res = nr_res
        self.nbr_row = nbr_row
        self.cur_pos = cur_pos

    def __get_nr_pages(self):
        """ """
        nr_pages, remainder = divmod(self.nbr_row, self.nr_res)
        if remainder != 0:
            nr_pages = nr_pages + 1
        return nr_pages

    def __get_curr_page(self):
        """ """
        curr_page, remainder = divmod(self.cur_pos * self.__get_nr_pages(), self.nbr_row)
        return curr_page

    def __get_pages_array(self):
        """ """
        pages = []
        curr_page = self.__get_curr_page()
        nr_pages = self.__get_nr_pages()
        for i in range(max(0, curr_page - 10 + 1), curr_page):
            pages.append(i)
        for i in range(curr_page, min(curr_page + 10, nr_pages)):
            pages.append(i)
        return pages

    def getPagingInformation(self):
        """ """
        start = self.cur_pos
        if self.cur_pos + self.nr_res >= self.nbr_row:
            stop = self.nbr_row
            next = -1
        else:
            stop = self.cur_pos + self.nr_res
            next = self.cur_pos + self.nr_res
        total = self.nbr_row
        if self.cur_pos != 0:
            prev = self.cur_pos - self.nr_res
        else:
            prev = -1
        pages = self.__get_pages_array()
        current_page = self.__get_curr_page()
        records_page = self.nr_res
        return (start, stop, total, prev, next, current_page, records_page, pages)
