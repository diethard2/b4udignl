"""
/***************************************************************************
 basic functions and superclass used to process namespaces found in xml files.
 -------------------
 begin                : june 2015
 copyright            : (C) 2015 by Diethard Jansen
 email                : Diethard.Jansen at Gmail.com
 ***************************************************************************/

/***************************************************************************
 *                                                                         *
 *   This program is free software; you can redistribute it and/or modify  *
 *   it under the terms of the GNU General Public License as published by  *
 *   the Free Software Foundation; either version 2 of the License, or     *
 *   (at your option) any later version.                                   *
 *                                                                         *
 ***************************************************************************/
"""
import re

def clean_tag(tag):
    """Remove namespace from tag"""
    if '}' in tag:
        index = tag.rindex('}')
        tag = tag[index+1:]
        tag = re.sub('([a-zA-Z])', lambda x: x.groups()[0].upper(), tag, 1)
    return tag
        
def find_xml_with_tag(xml_element, search_tag, found_elem):
    """Find in xml_element the element with given search_tag --> xml_element"""
    if found_elem is not None:
        return found_elem
    for i_elem in xml_element:
        tag = clean_tag(i_elem.tag)
##        print 'search_tag: ',search_tag
##        print 'tag:        ',tag
        if search_tag == tag:
            found_elem = i_elem
            break
        else:
            # search deeper in xml-tree
            found_elem = find_xml_with_tag(i_elem, search_tag, found_elem)
    return found_elem

class B_XmlProcessor(object):
    """superclass for all objects that need to process and interprete xml"""
    def __init__(self):
        self.__tag2process = {}

    def _tag2process(self):
        return self.__tag2process

    tag2process = property(fget=_tag2process, doc="tag2process is a dictionary, \
the key is the tag from xml the value the method to process the xml")

    def add_tag_method_to_process(self, a_tag, a_method):
        self.__tag2process[a_tag] = a_method

    def process(self, xml_element):
        """Process an incoming xml_element
        """
        for i_elem in xml_element:
            self.tag = clean_tag(i_elem.tag)
##            print(self.tag)
            if self.tag2process.has_key(self.tag):
                a_process = self.tag2process[self.tag]
##                print(a_process)
                a_process(i_elem)
            
