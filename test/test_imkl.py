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
import sys, os
path_core = os.path.join(os.path.dirname(__file__), '..')
##path_core = os.path.join(path_core, 'core')
sys.path.append(path_core)

import unittest
from core import imkl, gml, xml_utils
import xml.etree.ElementTree as ET

class OlieGasChemicalienPijpleidingTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test gml.Point
        """
        # read the file
        xml_file = open("data/18G007160_1/BuisGevaarlijkeInhoud.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "OlieGasChemicalienPijpleiding", None)
        self.buisGevaarlijkeInhoud = imkl.olieGasChemicalienPijpleiding()
        self.buisGevaarlijkeInhoud.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.field_names(),
                         ['id','registratiedatum','network_id',
                          'link_id', 'status', 'aanwezig_vanaf',
                          'vertical_position','diameter','druk',
                          'fluid', 'geom_id', 'label'])

    def test_field_values(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.field_values(),
                         ['nl.imkl-nbact1.ogc00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00057','nl.imkl-nbact1.ul00005',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z','underground','0.0','0.0',
                          'http://inspire.ec.europa.eu/codelist/OilGasChemicalsProductTypeValue/naturalGas',
                          'nl.imkl-nbact1.xg00009',''])

    def test_csv_header(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.csv_header(),
                         'id;registratiedatum;network_id;link_id;status;\
aanwezig_vanaf;vertical_position;diameter;druk;fluid;geom_id;label')

    def test_as_csv(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.as_csv(),
                         'nl.imkl-nbact1.ogc00001;2001-12-17T09:30:47.0Z;\
nl.imkl-nbact1.un00057;nl.imkl-nbact1.ul00005;\
http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused;\
2001-12-17T09:30:47.0Z;underground;0.0;0.0;http:\
//inspire.ec.europa.eu/codelist/OilGasChemicalsProductTypeValue/naturalGas;\
nl.imkl-nbact1.xg00009;')
    
_suite_olieGasChemicalienPijpleiding = unittest.TestLoader().loadTestsFromTestCase(OlieGasChemicalienPijpleidingTestCase)

class ExtraGeometrieTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.ExtraGeometrie
        """
        # read the file
        xml_file = open("data/18G007160_1/BuisGevaarlijkeInhoud.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "ExtraGeometrie",
                                                       None)
        self.extraGeometrie = imkl.extraGeometrie()
        self.extraGeometrie.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.extraGeometrie.field_names(),
                         ['id','registratiedatum','network_id',
                          'vlakgeometrie'])

    def test_field_values(self):
        self.assertEqual(self.extraGeometrie.field_values(),
                         ['nl.imkl-nbact1.xg00009','2015-10-19T09:30:47.0Z',
                          'nl.imkl-nbact1.un00057',
                          'Polygon((155052.000 388010.000, \
155050.000 388008.000, 155048.000 388010.000, 155050.000 388012.000, \
155052.000 388010.000))'])

    def test_csv_header(self):
        self.assertEqual(self.extraGeometrie.csv_header(),
                         'id;registratiedatum;network_id;vlakgeometrie')

    def test_as_csv(self):
        self.assertEqual(self.extraGeometrie.as_csv(),
                         'nl.imkl-nbact1.xg00009;2015-10-19T09:30:47.0Z;\
nl.imkl-nbact1.un00057;Polygon((155052.000 388010.000, \
155050.000 388008.000, 155048.000 388010.000, 155050.000 388012.000, \
155052.000 388010.000))')
    
_suite_extraGeometrie = unittest.TestLoader().loadTestsFromTestCase(ExtraGeometrieTestCase)

unit_test_suites = [_suite_olieGasChemicalienPijpleiding, _suite_extraGeometrie]

def main():
    imkl_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(imkl_test_suite)
        
if __name__ == "__main__":
    main()        
