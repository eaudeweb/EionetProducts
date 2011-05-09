import re

pattern = re.compile("\(\s*\w+\s*:\s*([^\(\)]+)\s*\)$") #Find \0 and \1

def update_source(self, REQUEST):
    """ This returns an sql file. It doesn't run any update/insert queries.
    Add a new property to the `property` table called `source`
    based on the `definition` of the same concept. Assume that the `definition`
    contains at the end (Source: some/source ) string. Remove it from the end
    and add it as the `source` property.

    Note: Make sure you backup the `property` table before the update

    """
    from Products.GimmeThesaurus.DatabaseManager import DatabaseManager

    if hasattr(self, 'gemet') and self.gemet.meta_type == 'Gimme Thesaurus':
        #Find all definitions that end with (Source: text-text)
        search_definitions_sql = """
        SELECT * FROM `property`
        WHERE `name` = 'definition' AND
              `value` REGEXP '\\\\([[:space:]]*[a-zA-Z]+[[:space:]]*:[[:space:]]*[^\\\\(\\\\)]+[[:space:]]*\\\\)$'
        """
        return_str = u"""

        """
        gemet = getattr(self, 'gemet')
        conn = DatabaseManager()
        conn.openConnection(gemet)
        err, definitions, msg = conn.query(search_definitions_sql)

        insert_sql = u'INSERT INTO `property` (`ns`, `id_concept`, `langcode`, `name`, `value`) VALUES '
        inserts = []
        updates = []
        if definitions and not err:
            for definition in definitions:
                source_text = re.search(pattern,
                                        definition['value'].decode('utf-8')).group(1)
                replace_value = re.sub(pattern, '',
                                    definition['value'].decode('utf-8')).strip()
                inserts.append(u"(%d, %d, '%s', '%s', '%s')" % (
                    definition['ns'],
                    definition['id_concept'],
                    definition['langcode'],
                    u'source',
                    conn._db.escape_string(source_text.encode('utf-8')).decode('utf-8'), ))

                updates.append(u"UPDATE `property` SET `value` = '%s' WHERE `ns` = %d AND `id_concept` = %d AND `langcode` = '%s' AND `name` = '%s'" % (
                    conn._db.escape_string(replace_value.encode('utf-8')).decode('utf-8'),
                    definition['ns'],
                    definition['id_concept'],
                    definition['langcode'],
                    definition['name'], ))

        #Split the inserts into 10 pieces
        for inserts_chunk in [inserts[i::10] for i in range(10)]:
            insert_sql_new = insert_sql
            insert_sql_new += u', '.join(inserts_chunk)
            return_str += insert_sql_new + ";\n"

        for update_sql in updates: #Update one by one
            return_str += update_sql + ";\n"
        REQUEST.RESPONSE.setHeader("content-type", 'text/plain')
        REQUEST.RESPONSE.setHeader('Content-Disposition',
                                   'Attachment; Filename=update_source.sql')
        return return_str
