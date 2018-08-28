"""
/***************************************************************************
 gml contains basic classes to convert typical xml elements that contain
 geometry in gml notation used in xml files holding basis geodata used
 in het Netherlands.
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
from xml_utils import *

def wkt_coords_from_gml(gml_coords):
    wkt_coords = ""
    count = 0
    values = gml_coords.split()
    for value in values:
        count += 1
        if count % 2 == 1:
            wkt_coords += value + ' '
        else:
            wkt_coords += value + ', '
    return wkt_coords[:-2]

def coords_2d_from_3d(gml_coords_text):
    xyz = gml_coords_text.split()
    xy = []
    l_count = 0
    for i_coord in xyz:
        l_count += 1
        if l_count % 3 > 0:
            xy.append(i_coord)
    return ' '.join(xy)

                    
class GmlBase(B_XmlProcessor):

    def __init__(self):
        B_XmlProcessor.__init__(self)

    def as_wkt(self):
        return None

    def as_text(self):
        return self.as_wkt()

    def _text_poslist(self, elem):
        if self._is_poslist_3d(elem):
            return coords_2d_from_3d(elem.text)
        else:
            return ' '.join(elem.text.split())
            
    def _is_poslist_3d(self, elem):
        is_3d = False
        xml_attributes = elem.attrib
        if xml_attributes.has_key('srsDimension'):
            if xml_attributes['srsDimension'] == '3':
                is_3d = True
        return is_3d

class Point(B_XmlProcessor):

    def __init__(self):
        B_XmlProcessor.__init__(self)
        self.coords = ""
        self.add_tag_method_to_process("Point", self.process)
        self.add_tag_method_to_process("pos", self._process_pos)

    def _process_pos(self, elem):
        '''From xml element pos derive the position of a GML Point'''
        coord_text = elem.text
        self.coords = coords_2d_from_3d(elem.text)

    def as_wkt(self):
        """Return valid geom in WKT notation for polygon"""
        wkt = "Point(%s)" % self.coords
        return wkt

class LineString(GmlBase):

    def __init__(self):
        GmlBase.__init__(self)
        self.coords = ""
        self.add_tag_method_to_process("LineString", self.process)
        self.add_tag_method_to_process("posList", self._process_posList)

    def _process_posList(self, elem):
        '''From xml element posList derive the coords'''        
        self.coords = wkt_coords_from_gml(self._text_poslist(elem))

    def as_wkt(self):
        """Return valid geom in WKT notation for polygon"""
        wkt = "LineString(%s)" % self.coords
        return wkt

        
class Envelope(GmlBase):

    def __init__(self):
        GmlBase.__init__(self)
        self.xmin = ""
        self.ymin = ""
        self.xmax = ""
        self.ymax = ""
        self.add_tag_method_to_process("Envelope", self.process)
        self.add_tag_method_to_process("lowerCorner", self._process_lowerCorner)
        self.add_tag_method_to_process("upperCorner", self._process_upperCorner)

    def _process_lowerCorner(self, elem):
        '''From xml element lowerCorner set the xmin and ymin'''
        (self.xmin, self.ymin) = elem.text.split(' ')

    def _process_upperCorner(self, elem):
        '''From xml element lowerCorner set the xmin and ymin'''        
        (self.xmax, self.ymax) = elem.text.split(' ')

    def as_wkt(self):
        """Return envelope as rectangular polygon in WKT notation"""
        xmin = self.xmin
        ymin = self.ymin
        xmax = self.xmax
        ymax = self.ymax
        coords = (xmin, ymin, xmin, ymax, xmax, ymax, xmax, ymin, xmin, ymin)
        wkt = "Polygon(%s %s, %s %s, %s %s, %s %s, %s %s)" % coords
        return wkt

        
class Polygon(GmlBase):
    
    def __init__(self):
        GmlBase.__init__(self)
        self.exterior_ring = ""
        self.interior_rings = []

    def process(self, elem):
        tag = clean_tag(elem.tag)
        if tag == "Polygon":
            # called from MultiPolygon, the incoming element is an xml
            # polygon item.
            self._process_polygon(elem)
        else:
            # called directly, incoming element is an xml geometry item
            for i_elem in elem:
                tag = clean_tag(i_elem.tag)
                if tag == "Polygon":
                    self._process_polygon(i_elem)
                elif tag =="exterior":
                    self._process_exterior(i_elem)
                elif tag == "interior":
                    self._process_interior(i_elem)
                
    def _process_polygon(self, elem):
        for i_elem in elem:
            tag = clean_tag(i_elem.tag)
            if tag == "exterior":
                    self._process_exterior(i_elem)
            elif tag == "interior":
                    self._process_interior(i_elem)

    def _process_exterior(self, elem):
        for i_elem in elem:
            tag = clean_tag(i_elem.tag)
            if tag == "LinearRing":
                self._process_LinearRing(i_elem, exterior=True)
                
    def _process_interior(self, elem):
        for i_elem in elem:
            tag = clean_tag(i_elem.tag)
            if tag == "LinearRing":
                self._process_LinearRing(i_elem, exterior=False)
                
    def _process_LinearRing(self, elem, exterior):
        for i_elem in elem:
            tag = clean_tag(i_elem.tag)
            if tag == "posList":
                if exterior == True:
                    coords_text = self._text_poslist(i_elem)
                    self.exterior_ring = coords_text
                else:
                    coords_text = self._text_poslist(i_elem)
                    self.interior_rings.append(coords_text)

    def wkt_rings(self):
        """Return only the external en internal rings in WKT \
        notation for polygon"""
        wkt = "((" + wkt_coords_from_gml(self.exterior_ring) + ")"
        for int_ring in self.interior_rings:
            wkt += ",(" + wkt_coords_from_gml(int_ring) + ")"
        wkt += ")"
        return wkt
       
    def as_wkt(self):
        """Return valid geom in WKT notation for polygon"""
        wkt = "Polygon" + self.wkt_rings()
        return wkt

class MultiPolygon(GmlBase):
    
    def __init__(self):
        GmlBase.__init__(self)
        self.polygons = []
        self._add_tags_to_process()

    def _add_tags_to_process(self):
        print "in MultiPolygon._add_tags_to_process(self)"
        for i_tag in ("MultiSurface", "surfaceMember"):
            self.add_tag_method_to_process(i_tag, self.process)
        self.add_tag_method_to_process("Polygon", self._process_Polygon)

    def _process_Polygon(self, elem):
        print "in MultiPolygon.process_Polygon()"
        a_polygon = Polygon()
        a_polygon.process(elem)
        self.polygons.append(a_polygon)

    def as_wkt(self):
        wkt = "MultiPolygon("
        count_polygon = 0
        for a_polygon in self.polygons:
            count_polygon += 1
            if count_polygon > 1:
                wkt += ","
            wkt += a_polygon.wkt_rings()
        wkt += ")"
        return wkt
