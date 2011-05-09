# -*- coding: utf-8 -*-
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
# Agency (EEA).  Portions created by Finsiel Romania and Eau de Web are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Authors:
#
# Alex Ghica, Eau de Web
# Alex Morega, Eau de Web
# Cornel Nitu, Eau de Web
# Søren Roug
#

from Collation_charts import unicode_character_map


def _convertdb(s):
    """ return a string used to build an sql statement """
    return '\'%s\'' % unicode(s).replace("'", "''").encode('utf-8')

def unicode_langs():
    """ temporary list of implemented languages """
    return unicode_character_map.keys()

def unicode_map(lang):
    """ return unicode set of characters for a given language """
    return unicode_character_map[lang]

def _letters_set(lang, letter):
    """ return set of letters in given language """
    try:  return unicode_map(lang)[letter]
    except:  return unicode_map(lang)[0]

def _sql_letter(p_lang, p_letter):
    """ creates the SQL stamenent based on letters set of a given language """
    l_letter = int(p_letter)
    if p_lang not in unicode_langs():  return " (1=1)"
    if l_letter == 0:  return " (1=1)"

    if l_letter == 99:
        l_ret = " ("
        j = 1
        letter_list_len = len(unicode_map(p_lang))
        for letter_list in unicode_map(p_lang):
            i = 1
            char_list_len = len(letter_list)
            for char in letter_list:
                l_ret += "(term.value NOT LIKE CONVERT(_utf8'"
                l_ret += char.encode('utf-8')
                l_ret += "%' USING utf8))"
                if (i == char_list_len) and (j == letter_list_len):  l_ret += ") "
                else:  l_ret += " AND "
                i += 1
            j += 1
        return l_ret

    else:
        l_ret = " ("
        l_len = len(_letters_set(p_lang, l_letter-1))
        i = 1
        for char in _letters_set(p_lang, l_letter-1):
            l_ret += "(term.value LIKE CONVERT(_utf8'"
            l_ret += char.encode('utf-8')
            l_ret += "%' USING utf8))"
            if i == l_len:  l_ret += ") "
            else:  l_ret += " OR "
            i += 1
        return l_ret

#------------ Concept -----------------------------------------------------#

def sql_get_namespaces():
    """ returns a list of namespaces available in the database """
    return """
        SELECT
            id_ns as namespace_id,
            ns_url as namespace_uri,
            heading as namespace_name,
            version as namespace_version,
            type_url as namespace_type
        FROM namespace"""

def sql_get_namespace_languages(namespace_id):
    """ returns a list of languages for which the selected namespace has translations """
    return """
        SELECT DISTINCT
            langcode
        FROM property
        WHERE ns = %s""" % _convertdb(namespace_id)

def sql_get_concept_languages(concept_ns, concept_id):
    """ returns a list of languages for which the selected concept has translations """
    return """
        SELECT DISTINCT
            langcode
        FROM property
        WHERE ns = %s AND id_concept = %s""" % (_convertdb(concept_ns), _convertdb(concept_id))

def sql_get_concept_by_regex(namespace_id, regex, language):
    """ returns a list of concepts whose name matches a regular expression from the given namespace """

    # MySQL will un-escape our backslashes once when parsing the SQL statement,
    # so any backslashes in the regexp need escaping
    backslash = '\\'
    regex = regex.replace(backslash, backslash*2)

    return ("""
        SELECT
            id_concept AS concept_id
        FROM property
        WHERE ns = %s AND langcode = %s AND name = "prefLabel" AND
            value RLIKE CONVERT(_utf8%s USING utf8)""" % \
                (_convertdb(namespace_id), _convertdb(language), _convertdb(regex)))

def sql_get_concept(cp_id, cp_ns, lang):
    """ returns a concept from the given namespace in a language """
    return """
        SELECT
            term.value AS concept_name,
            definition.value AS concept_definition
        FROM concept
            JOIN property AS term ON (term.name = "prefLabel" AND term.id_concept = concept.id_concept AND term.ns = concept.ns)
            LEFT JOIN property AS definition ON (definition.name = "definition" AND definition.id_concept = concept.id_concept AND
                            definition.ns = concept.ns AND term.langcode = definition.langcode)
        WHERE concept.id_concept = %s
            AND concept.ns = %s
            AND term.langcode = %s""" % (_convertdb(cp_id), _convertdb(cp_ns), _convertdb(lang))

def sql_get_concept_name(cp_ns, cp_id, lang):
    """ returns a concept's name in a language """
    return """
        SELECT
            property.value AS concept_name,
            language.langcode AS langcode,
            language.language AS language
        FROM language
            INNER JOIN property ON (property.langcode = language.langcode AND property.name = "prefLabel")
        WHERE (property.ns = %s) AND
              (property.id_concept = %s) AND
              (property.langcode = %s)""" % (_convertdb(cp_ns), _convertdb(cp_id), _convertdb(lang))

def sql_get_concept_names(cp_ns, cp_id):
    """ returns a concept's name in all languages """
    return sql_get_concept_property(cp_ns, cp_id, "prefLabel", "concept_name")

def sql_get_concept_alt_names(cp_ns, cp_id):
    """ returns a altLabel in all languages for a concept"""
    return sql_get_concept_property(cp_ns, cp_id, "altLabel", "concept_alt_name")

def sql_get_concept_property(cp_ns, cp_id, prop_name, val_name="value"):
    """ returns the requested concept's property in all languages """
    return """
        SELECT
            property.value AS %s,
            language.langcode AS langcode,
            language.language AS language
        FROM language
            INNER JOIN property ON (property.langcode = language.langcode AND property.name = %s)
        WHERE (property.ns = %s) AND
              (property.id_concept = %s)
        ORDER BY language.language ASC""" % (val_name, _convertdb(prop_name), _convertdb(cp_ns), _convertdb(cp_id))

def sql_get_concept_property_lang(val_name, cp_ns, cp_id, prop_name, lang):
    """ returns a concept's property in the specified language """
    return """
        SELECT
            property.value AS %s
        FROM property
        WHERE property.ns = %s AND
              property.id_concept = %s AND
              property.name = %s AND
              property.langcode = %s""" % (val_name, _convertdb(cp_ns), _convertdb(cp_id), _convertdb(prop_name), _convertdb(lang))

def sql_get_concept_definition(cp_ns, cp_id, lang):
    """ returns a concept's definition in the specified language """
    return sql_get_concept_property_lang("scope_definition", cp_ns, cp_id, "definition", lang)

def sql_get_concept_note(cp_ns, cp_id, lang):
    """ returns a concept's scope note in the specified language"""
    return sql_get_concept_property_lang("scope_note", cp_ns, cp_id, "scopeNote", lang)

def sql_get_concept_note_definition(cp_ns, cp_id, lang):
    """ returns a concept's scope note and definition"""
    return """
        SELECT
             s.value as scope_note,
             d.value AS scope_definition
        FROM concept AS c
            LEFT JOIN property AS d ON
                c.ns = d.ns AND
                c.id_concept = d.id_concept AND
                d.langcode = %s AND
                d.name = "definition"
            LEFT JOIN property AS s ON
                c.ns = s.ns AND
                c.id_concept = s.id_concept AND
                s.langcode = %s AND
                s.name = "scopeNote"
        WHERE c.ns = %s AND
            c.id_concept = %s AND
            c.id_status = 'n'""" % (_convertdb(lang), _convertdb(lang), _convertdb(cp_ns), _convertdb(cp_id))


def sql_get_concept_narrower(cp_id, lang, collation):
    """ return all narrower terms for a concept in the specified language"""
    return """SELECT
                relation.id_relation AS concept_id,
                term.value AS concept_name
            FROM relation
            INNER JOIN property AS term
                ON (relation.target_ns = term.ns AND relation.id_relation = term.id_concept AND term.name = "prefLabel")
            WHERE relation.id_concept = %s AND
                relation.source_ns = 1 AND
                relation.id_type ='narrower' AND
                term.langcode=%s
            ORDER BY term.value COLLATE %s ASC""" % (_convertdb(cp_id), _convertdb(lang), collation)

def sql_get_concept_relations(cp_ns, cp_id, lang, collation):
    """ returns concept's relations in the specified language"""
    return """
        SELECT
            term.value AS concept_name,
            term.ns AS concept_ns_id,
            namespace.heading AS concept_ns_name
        FROM property AS term
            INNER JOIN relation ON (relation.target_ns = term.ns AND relation.id_relation = term.id_concept)
            INNER JOIN namespace ON (term.ns = namespace.id_ns)
        WHERE relation.target_ns != %s AND
            relation.source_ns = %s AND
            relation.id_concept = %s AND
            term.name = "prefLabel" AND
            term.langcode = %s
        ORDER BY term.value
        COLLATE %s ASC""" % (_convertdb(cp_ns), _convertdb(cp_ns), _convertdb(cp_id), _convertdb(lang), collation)

def sql_get_concept_foreign_relations(cp_ns, cp_id, lang, collation):
    """ returns concept's foreign relations
        Currently we only have English labels of the foreign concepts in the database,
        but this could change, and then the 'lang' argument becomes needed.
        Only to be used for HTML output
    """
    return """
        SELECT  foreign_relation.id_type AS concept_relation_type,
            foreign_relation.relation_uri AS foreign_relation_uri,
            foreign_relation.label AS foreign_relation_label,
            property_type.label AS concept_property_label
        FROM foreign_relation
        LEFT JOIN property_type USING (id_type)
        WHERE foreign_relation.source_ns = %s
        AND foreign_relation.id_concept = %s
        AND show_in_html = 1
        ORDER BY property_type.label""" % (_convertdb(cp_ns), _convertdb(cp_id))

def sql_select_all_concepts_themes():
    """ get a concept_theme """
    return """SELECT
                id_concept AS concept_id,
                id_relation AS theme_id
            FROM relation
            WHERE source_ns = 1 AND target_ns = 4"""

def sql_get_all_concepts_groups():
    """ return all relations concept-group """
    return """SELECT
                id_concept AS concept_id,
                id_relation AS group_id
            FROM relation
            WHERE source_ns = 1 AND target_ns = 3"""

def sql_get_group_top_concepts(id_group, lang, collation):
    """ returns all top concepts for a specified group """
    return """SELECT
                concept.id_concept AS concept_id,
                term.value AS concept_name
            FROM concept
                INNER JOIN property AS term ON (concept.id_concept = term.id_concept AND concept.ns = term.ns AND term.name = "prefLabel")
                INNER JOIN relation ON (concept.id_concept = relation.id_concept AND concept.ns = relation.source_ns)
            WHERE concept.id_concept NOT IN (
                        SELECT DISTINCT id_concept
                        FROM relation
                        WHERE id_type='broader'
                            AND source_ns=1 AND target_ns=1)
                AND relation.id_relation = %s
                AND relation.source_ns = 1
                AND relation.target_ns = 3
                AND term.langcode = %s
            ORDER BY term.value COLLATE %s ASC""" % (id_group, _convertdb(lang), collation)

def sql_get_top_concepts(ns, lang, collation):
        """ returns all top concepts """
        return """SELECT
                    concept.id_concept AS concept_id,
                    term.value AS concept_name
                FROM concept
                    INNER JOIN property AS term ON (concept.id_concept = term.id_concept AND concept.ns = term.ns AND term.name = "prefLabel")
                WHERE concept.id_concept NOT IN (SELECT DISTINCT id_concept
                                FROM relation
                                WHERE id_type='broader' AND source_ns = %s AND target_ns = %s)
                    AND concept.ns = %s
                    AND term.langcode = %s
                ORDER BY term.value COLLATE %s ASC""" % (_convertdb(ns), _convertdb(ns), _convertdb(ns), _convertdb(lang), collation)

def sql_get_all_concepts_name(ns, lang):
    """ returns all the concepts name and altLabel's for a given langcode """
    return """
    SELECT
        term.id_concept AS concept_id,
        term.value AS concept_name,
        GROUP_CONCAT(altterm.value SEPARATOR '; ') AS concept_alt_name,
        definition.value AS scope_definition,
        scope_note.value AS scope_note
    FROM property AS term
    LEFT JOIN property AS scope_note ON (
        scope_note.name = 'scopeNote' AND
        term.id_concept = scope_note.id_concept AND
        term.ns = scope_note.ns AND
        term.langcode = scope_note.langcode )
    LEFT JOIN property AS altterm ON (
        altterm.name = 'altLabel' AND
        term.id_concept = altterm.id_concept AND
        term.ns = altterm.ns AND
        term.langcode = altterm.langcode )
    LEFT JOIN property AS definition ON (
        definition.name = 'definition' AND
        term.id_concept = definition.id_concept AND
        term.ns = definition.ns AND
        term.langcode = definition.langcode )
    WHERE
        term.name = "prefLabel" AND
        term.ns = %d AND
        term.langcode = %s
    GROUP BY (concept_id)
    ORDER BY term.id_concept ASC""" % (ns, _convertdb(lang))

def sql_find_concept(cp, lang, collation):
    """ Return all the concepts matching with concept name for a given
    language. Also match concepts with altLabel.

    """

    return """
    SELECT DISTINCT
        term1.id_concept AS concept_id,
        term1.value AS concept_name,
        term2.value AS scope_name,
        GROUP_CONCAT(altterm.value SEPARATOR '; ') AS concept_alt_name
    FROM property AS term1
    LEFT JOIN property AS altterm
    ON (altterm.name = "altLabel" AND
        term1.ns = altterm.ns AND
        term1.id_concept = altterm.id_concept AND
        term1.langcode = altterm.langcode)
    LEFT JOIN relation
    ON (term1.id_concept = relation.id_concept AND
        term1.ns = relation.source_ns AND
        relation.id_type = 'broader')
    LEFT JOIN property AS term2
    ON (term2.name = "prefLabel" AND
        relation.id_relation = term2.id_concept AND
        relation.target_ns = term2.ns AND
        term2.langcode=%(lang)s)
    WHERE
        term1.name = "prefLabel" AND
        (term1.value LIKE CONVERT(_utf8%(term)s USING utf8) OR
        altterm.value LIKE CONVERT(_utf8%(term)s USING utf8))
        AND term1.ns = 1
        AND term2.ns = 1
        AND term1.langcode = %(lang)s
    GROUP BY (concept_id)
    ORDER BY term1.value
    COLLATE %(coll)s ASC""" % {
        'lang': _convertdb(lang),
        'term': _convertdb('%s%%' % cp),
        'coll': collation
    }

def sql_get_concepts_letter(lang, collation, letter=0):
    """ returns concept names based on an langcode """
    return """SELECT
                term.id_concept AS concept_id,
                term.value AS concept_name
            FROM property as term
            WHERE term.name = "prefLabel" AND
                term.langcode = %s AND
                %s
            ORDER BY term.value
            COLLATE %s ASC""" % (_convertdb(lang), _sql_letter(lang, letter), collation)

#------------ Theme -----------------------------------------------------#
def sql_get_themes(ns_id, lang, collation):
    """ returns theme list in a specified language """

    return """
        SELECT
            concept.id_concept AS theme_id,
            term.value AS theme_description,
            acronym.value AS theme_accronym,
            definition.value AS theme_definition
        FROM concept
            INNER JOIN property AS term ON (concept.id_concept = term.id_concept AND
                    concept.ns = term.ns AND term.langcode = %s AND term.name = "prefLabel")
            LEFT JOIN property AS acronym ON (acronym.name = "acronymLabel" AND concept.id_concept = acronym.id_concept AND
                    concept.ns = acronym.ns AND acronym.langcode = term.langcode)
            LEFT JOIN property AS definition ON (definition.name = "definition" AND concept.id_concept = definition.id_concept AND
                    concept.ns = definition.ns AND definition.langcode = term.langcode)
        WHERE concept.ns = %s
        ORDER BY term.value
        COLLATE %s ASC""" % (_convertdb(lang), _convertdb(ns_id), collation)

def sql_get_current_theme(th_id, th_ns, lang):
    """ returns a concept's theme in a specifyed language """
    return """
        SELECT
            concept.id_concept AS theme_id,
            term.value AS theme_description,
            definition.value AS theme_definition,
            acronym.value AS theme_accronym
        FROM concept
            INNER JOIN property AS term ON (term.name = "prefLabel" AND concept.id_concept = term.id_concept AND
                    term.ns = concept.ns AND term.langcode = %s)
            LEFT JOIN property AS acronym ON (acronym.name = "acronymLabel" AND concept.id_concept = acronym.id_concept AND
                    concept.ns = acronym.ns AND acronym.langcode = %s)
            LEFT JOIN property AS definition ON (definition.name = "definition" AND concept.id_concept = definition.id_concept AND
                    concept.ns = definition.ns AND definition.langcode = %s)
        WHERE concept.ns = %s and concept.id_concept = %s
        ORDER BY term.value""" % (_convertdb(lang), _convertdb(lang), _convertdb(lang), _convertdb(th_ns), _convertdb(th_id))

def sql_get_theme_concepts(th_id, th_ns, lang, collation, letter=0):
    """ returns concept names based on an id_theme """

    return """
        SELECT
            term.id_concept AS concept_id,
            term.ns AS concept_ns,
            term.value AS concept_name
        FROM property AS term
            INNER JOIN relation ON (term.id_concept = relation.id_concept AND
                                      term.ns = relation.source_ns AND
                                      relation.target_ns = %s AND
                                      relation.id_relation = %s)
        WHERE term.name = "prefLabel" AND
            term.langcode = %s AND
            %s
        ORDER BY term.value
        COLLATE %s ASC""" % (_convertdb(th_ns), _convertdb(th_id), _convertdb(lang), _sql_letter(lang, letter), collation)

#------------ Group -----------------------------------------------------#

def sql_get_group_name(group_id, lang):
    """ returns the name of a group by it's id """
    return """SELECT
                concept.id_concept AS group_id,
                term.value AS group_description
            FROM concept
                INNER JOIN property AS term ON (term.name = "prefLabel" AND term.id_concept = concept.id_concept AND term.ns = concept.ns)
            WHERE (concept.id_concept = %s) AND (concept.ns = 3)
                AND (term.langcode = %s)""" % (_convertdb(group_id), _convertdb(lang))

def sql_get_supergroups(lang, collation):
    """ returns supergroups by langcode """
    return """SELECT DISTINCT
                concept.id_concept AS group_id,
                term.value AS group_description,
                term.langcode AS langcode
            FROM concept
                INNER JOIN property AS term ON (term.name = "prefLabel" AND term.id_concept = concept.id_concept AND term.ns = concept.ns)
            WHERE (concept.ns = 2) AND (term.langcode = %s)
            ORDER BY term.value
            COLLATE %s ASC""" % (_convertdb(lang), collation)

def sql_get_groups_super(super, lang, collation):
    """ returns groups list, given the supergroup, in the specified language"""
    return """SELECT DISTINCT
                concept.id_concept AS group_id,
                term.value AS group_description,
                term.langcode AS langcode
            FROM concept
                INNER JOIN property AS term ON (term.name = "prefLabel" AND term.id_concept = concept.id_concept AND term.ns = concept.ns)
                INNER JOIN relation ON (concept.id_concept = relation.id_relation AND concept.ns = relation.target_ns)
            WHERE (concept.ns = 3) AND (term.langcode = %s)
                AND (relation.source_ns = 2) AND (relation.id_concept= %s)
            ORDER BY term.value
            COLLATE %s ASC""" % (_convertdb(lang), _convertdb(super), collation)

def sql_get_all_groups(lang):
    """ get all groups (including supergroups) for a given language """
    return """SELECT
                concept_group.id_concept AS group_id,
                term.value AS group_description,
                super_group.id_concept AS super_group_id
            FROM relation
            JOIN concept AS concept_group ON (relation.id_concept = concept_group.id_concept AND
                    relation.source_ns = concept_group.ns AND concept_group.ns = 3)
            JOIN concept AS super_group ON (relation.id_relation = super_group.id_concept AND
                    relation.target_ns = super_group.ns AND super_group.ns = 2)
            JOIN property AS term ON (term.name = "prefLabel" AND
                    term.id_concept = concept_group.id_concept AND term.ns = concept_group.ns)
            WHERE relation.id_type = 'broader' AND term.langcode = %s
            ORDER BY group_id""" % _convertdb(lang)

#------------ Relations -----------------------------------------------------#

def sql_get_relations():
    """ return all relations among concepts """
    return """SELECT
                id_concept AS concept_id,
                id_type AS relation_name,
                id_relation AS relation_id
            FROM relation
            WHERE ((id_type = 'narrower') OR (id_type = 'broader') OR (id_type = 'related')) AND source_ns = 1 AND target_ns = 1
            ORDER BY id_concept"""

def sql_get_foreign_relations():
    """ return all foreign relations relevant to SKOS RDF """
    return """SELECT
                id_concept AS concept_id,
                id_type AS relation_name,
                relation_uri AS relation_id
            FROM foreign_relation
            WHERE
                id_type in ('broadMatch','closeMatch','exactMatch','narrowMatch','relatedMatch')
            AND source_ns = 1
            ORDER BY id_concept"""

def sql_get_relation(cp_ns, cp_id, lang, collation):
    """ get the concept's broader/narrower list in the specified language """
    return """
        SELECT
            relation.id_concept AS concept_id,
            relation.id_relation AS relation_id,
            term.value AS relation_name,
            relation.id_type AS relation_description
        FROM relation
            INNER JOIN property AS term ON (term.name = "prefLabel" AND
                    relation.id_relation = term.id_concept AND relation.target_ns = term.ns)
        WHERE relation.id_concept = %s AND relation.source_ns = %s AND relation.target_ns = %s AND term.langcode = %s
        ORDER BY term.value
        COLLATE %s ASC""" % (cp_id, _convertdb(cp_ns), _convertdb(cp_ns), _convertdb(lang), collation)

def sql_get_concept_relatives(concept_ns, concept_id, target_ns=None, relation_uri=None):
    """ returns the concept parents """
    sql = """
        SELECT
            relation.target_ns AS rel_concept_ns,
            relation.id_relation AS rel_concept_id,
            property_type.uri AS rel_type_uri

        FROM relation
            JOIN property_type ON relation.id_type = property_type.id_type

        WHERE relation.source_ns = %s AND relation.id_concept = %s""" % (_convertdb(concept_ns), _convertdb(concept_id))

    if target_ns:
        sql += " AND target_ns = %s" % target_ns

    if relation_uri:
        sql += " AND property_type.uri = %s" % _convertdb(relation_uri)

    return sql

#------------ language & collation -----------------------------------------------------#
def sql_get_language_collation(lang):
    """ returns a language's name by its code """
    return """SELECT
                charset AS charset
            FROM language
            WHERE langcode = %s""" % _convertdb(lang)

def sql_get_language_dirention(lang):
    """ returns RTL or LTR """
    return """SELECT
                direction AS direction
            FROM language
            WHERE langcode = %s""" % _convertdb(lang)

def sql_get_languages(concept_ns=None, concept_id=None):
    """ select all languages"""

    where = []
    if concept_ns != None:
        where.append('property.ns = %s' % _convertdb(concept_ns))
    if concept_id != None:
        where.append('property.id_concept = %s' % _convertdb(concept_id))

    if where:
        where_clause = 'WHERE %s' % ' AND '.join(where)
    else:
        where_clause = ''

    return """SELECT DISTINCT langcode, language
            FROM language WHERE langcode in (
                SELECT DISTINCT langcode FROM property
                %s
            )
            ORDER BY langcode ASC""" % where_clause

def sql_get_language(lang):
    """ returns a language's name by its code """
    return """SELECT
                `language` AS `language`
            FROM `language`
            WHERE `langcode` = %s""" % _convertdb(lang)

#------------ definition sources ---------------------------------------------------#
def sql_get_definition_sources():
    """ returns the definition sources """
    return """SELECT * FROM `definition_sources`"""

#------------ semantic web ---------------------------------------------------------#
def sql_get_properties_as_rdf(cp_ns, cp_id):
    """ returns all the properties in the property table """
    return """SELECT uri, langcode, value, is_resource
              FROM property, property_type
              WHERE name=id_type AND ns=%s and id_concept=%s
      UNION   SELECT uri, '' as langcode, CONCAT(ns_url,id_relation) AS value, True as is_resource
              FROM relation,property_type,namespace
              WHERE target_ns= id_ns AND relation.id_type = property_type.id_type
              AND source_ns = %s AND id_concept = %s ORDER BY uri""" % (_convertdb(cp_ns), _convertdb(cp_id), _convertdb(cp_ns), _convertdb(cp_id))
