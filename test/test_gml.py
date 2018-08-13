"""
/***************************************************************************
 Unit test suite to test gml geometry objects.
 -------------------
 begin                : 26-06-2015
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
import unittest
from core import gml
from core.xml_utils import *
import xml.etree.ElementTree as ET

class PointTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test gml.Point
        """
        # read the file
        xml_file = open("test/data/gml/gml_geometries.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = find_xml_with_tag(root, "Point", None)
        self.point = gml.Point()
        self.point.process(self.xml_element)
        xml_file.close()

    def test_coords(self):
        self.assertEqual(self.point.coords, "155000.000 388030.000")

    def test_as_wkt(self):
        self.assertEqual(self.point.as_wkt(),
                         'Point(155000.000 388030.000)')
    
_suite_point = unittest.TestLoader().loadTestsFromTestCase(PointTestCase)

class LineStringTestCase(unittest.TestCase):
    """
    unittest to test GML Polygon
    """
    def setUp(self):
        """
        For each test create the Woonplaats read from xml file woonplaats.xml

        The geometry actually consists of an gml polygon element which includes
        an outer and inner ring.
        """
        xml_file = open("test/data/gml/gml_geometries.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_geometry = find_xml_with_tag(root, "LineString", None)
        self.linestring = gml.LineString()
        self.linestring.process(self.xml_geometry)
        xml_file.close()        

    def test_coords(self):
        self.assertEqual(self.linestring.coords, '155038.000 388070.000, 155022.000 388070.000')

    def test_as_wkt(self):
        self.assertEqual(self.linestring.as_wkt(),
                         'LineString(155038.000 388070.000, 155022.000 388070.000)')  

_suite_linestring = unittest.TestLoader().loadTestsFromTestCase(LineStringTestCase)
                         
class EnvelopeTestCase(unittest.TestCase):
    """
    unittest to test GML Envelope

    as_wkt() returns a Polygon which is bounding box.
    """
    def setUp(self):
        """
        For each test create the Woonplaats read from xml file woonplaats.xml

        The geometry actually consists of an gml polygon element which includes
        an outer and inner ring.
        """
        xml_file = open("test/data/gml/gml_geometries.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_geometry = find_xml_with_tag(root, "Envelope", None)
        self.envelope = gml.Envelope()
        self.envelope.process(self.xml_geometry)
        xml_file.close()        

    def test_extents(self):
        xmin = self.envelope.xmin
        ymin = self.envelope.ymin
        xmax = self.envelope.xmax
        ymax = self.envelope.ymax
        self.assertEqual((xmin,ymin,xmax,ymax),
                         ('154980.0','387980.0','155120.0','388140.0'))

    def test_as_wkt(self):
        self.assertEqual(self.envelope.as_wkt(),
                         'Polygon(154980.0 387980.0, 154980.0 388140.0, \
155120.0 388140.0, 155120.0 387980.0, 154980.0 387980.0)')  

_suite_envelope = unittest.TestLoader().loadTestsFromTestCase(EnvelopeTestCase)
                         
class PolygonTestCase(unittest.TestCase):
    """
    unittest to test GML Polygon
    """
    def setUp(self):
        """
        For each test create the Woonplaats read from xml file woonplaats.xml

        The geometry actually consists of an gml polygon element which includes
        an outer and inner ring.
        """
        xml_file = open("test/data/gml/gml_geometries.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_geometry = find_xml_with_tag(root, "Polygon", None)
        self.polygon = gml.Polygon()
        self.polygon.process(self.xml_geometry)
        xml_file.close()        

    def test_wkt_rings(self):
        self.assertEqual(self.polygon.wkt_rings(), '((80089.798 383288.255, \
81816.255 383744.931, 82005.608 381650.906, 80769.242 381394.722, \
80089.798 383288.255),(80758.104 383310.532, 81704.871 383455.332, \
81348.441 382809.303, 80802.658 382820.441, 80758.104 383310.532))')

    def test_as_wkt(self):
        self.assertEqual(self.polygon.as_wkt(),
                         'Polygon((80089.798 383288.255, \
81816.255 383744.931, 82005.608 381650.906, 80769.242 381394.722, \
80089.798 383288.255),(80758.104 383310.532, 81704.871 383455.332, \
81348.441 382809.303, 80802.658 382820.441, 80758.104 383310.532))')  

_suite_polygon = unittest.TestLoader().loadTestsFromTestCase(PolygonTestCase)
                         
class MultiPolygonTestCase(unittest.TestCase):
    """
    unittest to test MultiPolygon

    Run test from commandline in folder with code with following statement:
    python test_bag.py
    """
    def setUp(self):
        """
        For each test create the Woonplaats read from xml file woonplaats.xml

        The geometry actually consists of an gml polygon element which includes
        an outer and inner ring.
        """
        xml_file = open("test/data/gml/gml_geometries.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_geometry = find_xml_with_tag(root, "MultiSurface", None)
        self.multipolygon = gml.MultiPolygon()
        self.multipolygon.process(self.xml_geometry)
        xml_file.close()        

    def test_as_wkt(self):
        self.assertEqual(self.multipolygon.as_wkt(),
                         'MultiPolygon(((180001.576 580918.246, \
186053.377 581436.193, 186462.283 578137.688, 180328.700 577510.700, \
180001.576 580918.246),(181733.025 579596.742, 181911.214 579873.924, \
182049.805 579576.943, 181733.025 579596.742),(185257.193 579586.843, \
185366.086 579784.830, 185534.375 579636.339, 185257.193 579586.843)),\
((184247.460 577379.288, 185435.382 577735.665, 185544.274 577112.006, \
184445.447 576914.019, 184247.460 577379.288)))')

    def test_polygon(self):
        polygon = gml.Polygon()
        polygon.process(self.xml_geometry)
        self.assertEqual(polygon.wkt_rings(), '(())')

_suite_multipolygon = unittest.TestLoader().loadTestsFromTestCase(MultiPolygonTestCase)

class Polygon3DTestCase(unittest.TestCase):
    """
    First unittest to test Woonplaats

    Run test from commandline in folder with code with following statement:
    python test_bag.py
    """
    def setUp(self):
        """
        For each test create the Woonplaats read from xml file woonplaats.xml

        The geometry actually consists of an gml polygon element which includes
        an outer and inner ring.
        """
        xml_file = open("test/data/gml/pand.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_geometry = find_xml_with_tag(root, "pandGeometrie", None)
        self.polygon = gml.Polygon()
        self.polygon.process(self.xml_geometry)
        xml_file.close()        

    def test_wkt_rings(self):
        self.assertEqual(self.polygon.wkt_rings(), '((253680.97 576716.1, \
253679.11 576736.32, 253667.39 576735.3, 253669.21 576715.11, \
253680.97 576716.1),(253679.875 576724.723, 253671.753 576723.992, \
253671.406 576727.849, 253679.528 576728.58, 253679.875 576724.723))')

    def test_as_wkt(self):
        self.assertEqual(self.polygon.as_wkt(),
                         'Polygon((253680.97 576716.1, \
253679.11 576736.32, 253667.39 576735.3, 253669.21 576715.11, \
253680.97 576716.1),(253679.875 576724.723, 253671.753 576723.992, \
253671.406 576727.849, 253679.528 576728.58, 253679.875 576724.723))')

_suite_polygon3d = unittest.TestLoader().loadTestsFromTestCase(Polygon3DTestCase)

unit_test_suites = [_suite_point, _suite_linestring,_suite_envelope, _suite_polygon, _suite_multipolygon,
                    _suite_polygon3d]

def main():
    gml_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(gml_test_suite)
        
if __name__ == "__main__":
    main()
    

        
