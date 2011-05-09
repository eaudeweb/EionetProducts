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
# The Original Code is ManagedMeetings version 1.0.
#
# The Initial Owner of the Original Code is European Environment
# Agency (EEA).  Portions created by CMG and Finsiel Romania are
# Copyright (C) European Environment Agency.  All
# Rights Reserved.
#
# Contributor(s):
# Søren Roug, EEA
# Cornel Nitu, Finsiel Romania
# Rares Vernica, Finsiel Romania
#

import Globals
from OFS import SimpleItem
from webdav.WriteLockInterface import WriteLockInterface
from Globals import DTMLFile, MessageDialog
from AccessControl import getSecurityManager, Permissions, ClassSecurityInfo
from string import *

class Track(SimpleItem.SimpleItem):
    """
    Track class
    """
    meta_type = 'Meeting Track'
    icon = 'misc_/ManagedMeetings/track.gif'

    manage_options = (
        {'label': 'Properties', 'action': 'manage_editForm',},
        {'label': 'View', 'action': 'index_html',},
    )

    security = ClassSecurityInfo()

    def __setstate__(self,state):
        Track.inheritedAttribute("__setstate__") (self, state)
        if not hasattr(self, "order"): # backwards compatibility
            self.order = 10
        if not hasattr(self, "description"):
            self.description = ""

    def manage_editAction (self, title, order, colour, description='', REQUEST=None):
        "Changes the product values"
        self.title = title
        self.order = order
        self.colour = colour
        self.description = description
        if REQUEST:
            message="Saved changes."
            return self.manage_editForm(self,REQUEST,manage_tabs_message=message)

    index_html = DTMLFile('www/TrackIndex', globals())

    manage_editForm = DTMLFile('www/TrackEditForm', globals())

# Taken from X Windows and weeded
    convenience_colours = (
        ["#FFFFFF", "White"],
        ["#FFFAFA", "Snow"],
        ["#F8F8FF", "Ghost White"],
        ["#FFFFF0", "Ivory"],
        ["#F5FFFA", "Mint Cream"],
        ["#F0FFFF", "Azure"],
        ["#FFFAF0", "Floral White"],
        ["#F0F8FF", "Alice Blue"],
        ["#FFF0F5", "Lavender Blush"],
        ["#FFF5EE", "Seashell"],
        ["#F5F5F5", "White Smoke"],
        ["#F0FFF0", "Honeydew"],
        ["#FFFFE0", "Light Yellow"],
        ["#E0FFFF", "Light Cyan"],
        ["#FDF5E6", "Old Lace"],
        ["#FFF8DC", "Cornsilk"],
        ["#FAF0E6", "Linen"],
        ["#FFFACD", "Lemon Chiffon"],
        ["#FAFAD2", "Light Goldenrod Yellow"],
        ["#F5F5DC", "Beige"],
        ["#E6E6FA", "Lavender"],
        ["#FFE4E1", "Misty Rose"],
        ["#FFEFD5", "Papaya Whip"],
        ["#FAEBD7", "Antique White"],
        ["#FFEBCD", "Blanched Almond"],
        ["#FFE4C4", "Bisque"],
        ["#FFE4B5", "Moccasin"],
        ["#DCDCDC", "Gainsboro"],
        ["#FFDAB9", "Peach Puff"],
        ["#AFEEEE", "Pale Turquoise"],
        ["#FFDEAD", "Navajo White"],
        ["#FFC0CB", "Pink"],
        ["#F5DEB3", "Wheat"],
        ["#EEE8AA", "Pale Goldenrod"],
        ["#D3D3D3", "Light Gray"],
        ["#FFB6C1", "Light Pink"],
        ["#B0E0E6", "Powder Blue"],
        ["#D8BFD8", "Thistle"],
        ["#ADD8E6", "Light Blue"],
        ["#F0E68C", "Khaki"],
        ["#EE82EE", "Violet"],
        ["#DDA0DD", "Plum"],
        ["#B0C4DE", "Light Steel Blue"],
        ["#7FFFD4", "Aquamarine"],
        ["#87CEFA", "Light Sky Blue"],
        ["#EEDD82", "Light Goldenrod"],
        ["#C0C0C0", "Silver"],
        ["#87CEEB", "Sky Blue"],
        ["#98FB98", "Pale Green"],
        ["#DA70D6", "Orchid"],
        ["#DEB887", "Burlywood"],
        ["#FF69B4", "Hot Pink"],
        ["#FFA07A", "Light Salmon"],
        ["#D2B48C", "Tan"],
        ["#90EE90", "Light Green"],
        ["#FFFF00", "Yellow"],
        ["#FF00FF", "Magenta"],
        ["#00FFFF", "Cyan"],
        ["#A9A9A9", "Dark Gray"],
        ["#E9967A", "Dark Salmon"],
        ["#F4A460", "Sandy Brown"],
        ["#8470FF", "Light Slate Blue"],
        ["#F08080", "Light Coral"],
        ["#40E0D0", "Turquoise"],
        ["#FA8072", "Salmon"],
        ["#6495ED", "Cornflower Blue"],
        ["#48D1CC", "Medium Turquoise"],
        ["#BA55D3", "Medium Orchid"],
        ["#BDB76B", "Dark Khaki"],
        ["#DB7093", "Pale Violet Red"],
        ["#9370DB", "Medium Purple"],
        ["#66CDAA", "Medium Aquamarine"],
        ["#ADFF2F", "Green Yellow"],
        ["#BC8F8F", "Rosy Brown"],
        ["#8FBC8F", "Dark Sea Green"],
        ["#FFD700", "Gold"],
        ["#7B68EE", "Medium Slate Blue"],
        ["#FF7F50", "Coral"],
        ["#00BFFF", "Deep Sky Blue"],
        ["#A020F0", "Purple"],
        ["#1E90FF", "Dodger Blue"],
        ["#FF6347", "Tomato"],
        ["#FF1493", "Deep Pink"],
        ["#FFA500", "Orange"],
        ["#DAA520", "Goldenrod"],
        ["#00CED1", "Dark Turquoise"],
        ["#5F9EA0", "Cadet Blue"],
        ["#9ACD32", "Yellow Green"],
        ["#778899", "Light Slate Gray"],
        ["#9932CC", "Dark Orchid"],
        ["#8A2BE2", "Blue Violet"],
        ["#00FA9A", "Medium Spring Green"],
        ["#CD853F", "Peru"],
        ["#6A5ACD", "Slate Blue"],
        ["#FF8C00", "Dark Orange"],
        ["#4169E1", "Royal Blue"],
        ["#CD5C5C", "Indian Red"],
        ["#D02090", "Violet Red"],
        ["#808080", "Gray"],
        ["#708090", "Slate Gray"],
        ["#7FFF00", "Chartreuse"],
        ["#00FF7F", "Spring Green"],
        ["#4682B4", "Steel Blue"],
        ["#20B2AA", "Light Sea Green"],
        ["#7CFC00", "Lawn Green"],
        ["#9400D3", "Dark Violet"],
        ["#C71585", "Medium Violet Red"],
        ["#3CB371", "Medium Sea Green"],
        ["#D2691E", "Chocolate"],
        ["#B8860B", "Dark Goldenrod"],
        ["#FF4500", "Orange Red"],
        ["#B03060", "Maroon"],
        ["#696969", "Dim Gray"],
        ["#32CD32", "Lime Green"],
        ["#A0522D", "Sienna"],
        ["#6B8E23", "Olive Drab"],
        ["#8B008B", "Dark Magenta"],
        ["#008B8B", "Dark Cyan"],
        ["#483D8B", "Dark Slate Blue"],
        ["#2E8B57", "Sea Green"],
        ["#808000", "Olive"],
        ["#FF0000", "Red"],
        ["#00FF00", "Green"],
        ["#0000FF", "Blue"],
        ["#A52A2A", "Brown"],
        ["#B22222", "Firebrick"],
        ["#556B2F", "Dark Olive Green"],
        ["#8B4513", "Saddle Brown"],
        ["#228B22", "Forest Green"],
        ["#2F4F4F", "Dark Slate Gray"],
        ["#0000CD", "Medium Blue"],
        ["#191970", "Midnight Blue"],
        ["#8B0000", "Dark Red"],
        ["#00008B", "Dark Blue"],
        ["#000080", "Navy Blue"],
        ["#006400", "Dark Green"],
        ["#000000", "Black"],
    )

manage_addTrackForm = DTMLFile('www/TrackAddForm', globals())

def manage_addTrack(self, id, title, order, colour, description='', REQUEST=None):
    "Add a Track to a meeting."
    ob=Track()
    ob.id=id
    ob.title = title
    ob.order = order
    ob.colour = colour
    ob.description = description
    self._setObject(id, ob)
    ob=self._getOb(id)
    if REQUEST is not None:
        return MessageDialog(
            title = 'Created',
            message = "The Track %s has been created!" % ob.id,
            action = 'manage_main?update_menu=1',
            )
