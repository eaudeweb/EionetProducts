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
#$Id: Mappings.py 21090 2011-05-03 09:55:18Z plugaale $

__version__='$Revision: 1.10 $'[11:-2]


class Mappings:
    """ """

    def _convert(self, s):
        """ convert strings from None to empty """
        if s is None:   return ''
        else:   return s

    #------------- themes -------------------#
    def mp_theme_descr(self, rec):
        """ """
        return self._convert(rec.get('theme_description', ''))

    def mp_theme_accr(self, rec):
        """ """
        return self._convert(rec.get('theme_accronym', ''))

    def mp_theme_id(self, rec):
        """ """
        return self._convert(rec.get('theme_id', ''))

    def mp_theme_definition(self, rec):
        """ """
        return self._convert(rec.get('theme_definition', ''))

    #------------- concepts -------------------#
    def mp_concept_id(self, rec):
        """ """
        return self._convert(rec.get('concept_id', ''))

    def mp_concept_scope(self, rec):
        return self._convert(rec.get('scope_id', ''))

    def mp_concept_name(self, rec):
        return self._convert(rec.get('concept_name', ''))

    def mp_concept_alt(self, rec):
        alt_names = rec.get('alt_names', [])
        return map(self._convert, alt_names)

    def mp_concept_alt_concat(self, rec):
        alt_names = rec.get('concept_alt_name', [])
        if alt_names is None:
            return []
        if isinstance(alt_names, basestring):
            alt_names = alt_names.split("; ")
        return map(self._convert, alt_names)

    def mp_concept_definition(self, rec):
        return self._convert(rec.get('scope_definition', ''))

    def mp_concept_note(self, rec):
        return self._convert(rec.get('scope_note', ''))


    #------------- language -------------------#
    def mp_langcode(self, rec):
        return self._convert(rec.get('langcode', ''))

    def mp_language(self, rec):
        return self._convert(rec.get('language', ''))

    def mp_direction(self, rec):
        return self._convert(rec.get('direction', ''))

    def mp_charset(self, rec):
        return self._convert(rec.get('charset', ''))


    #------------- relation -------------------#
    def mp_relation_id(self, rec):
        return self._convert(rec.get('relation_id', ''))

    def mp_relation_name(self, rec):
        return self._convert(rec.get('relation_name', ''))

    def mp_relation_descr(self, rec):
        return self._convert(rec.get('relation_description', ''))


    #------------- groups -------------------#
    def mp_group_id(self, rec):
        return self._convert(rec.get('group_id', ''))

    def mp_group_descr(self, rec):
        return self._convert(rec.get('group_description', ''))

    def mp_supergroup_id(self, rec):
        return self._convert(rec.get('super_group_id', ''))

    #------------ definition sources --------#
    def mp_def_source_abbr(self, rec):
        return self._convert(rec.get('abbr', ''))

    def mp_def_source_author(self, rec):
        return self._convert(rec.get('author', ''))

    def mp_def_source_title(self, rec):
        return self._convert(rec.get('title', ''))

    def mp_def_source_url(self, rec):
        return self._convert(rec.get('url', ''))

    def mp_def_source_publication(self, rec):
        return self._convert(rec.get('publication', ''))

    def mp_def_source_place(self, rec):
        return self._convert(rec.get('place', ''))

    def mp_def_source_year(self, rec):
        return self._convert(rec.get('year', ''))

