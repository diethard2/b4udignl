"""
/***************************************************************************
 Unit test suite to test basis objects, B_Field and B_Object
 -------------------
 begin                : 14-07-2015
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
sys.path.append(path_core)

import unittest
from core import xml_utils, basis, gml
import xml.etree.ElementTree as ET

class B_FieldRegularTestCase(unittest.TestCase):
    """
    unittests to test Regular text basis Field B_Field
    """

    def setUp(self):
        """
        Setup a test create a regular B_Field.
        """
        self.field = basis.B_Field("naam", "TEXT", "woonplaatsNaam")

    def test_field_name(self):
        self.assertEqual(self.field.name, "naam")

    def test_field_type(self):
        self.assertEqual(self.field.type, "TEXT")

    def test_is_mandatory(self):
        self.assertEqual(self.field.is_mandatory, True)

    def test_is_key_field(self):
        self.assertEqual(self.field.is_key_field, False)
        
    def test_from_tag(self):
        self.assertEqual(self.field.from_tag, "woonplaatsNaam")

    def test_to_object(self):
        self.assertEqual(self.field.to_object, None)

    def test_set_value(self):
        self.field.value = "'s Hertogenbosch"
        self.assertEqual(self.field.value, "'s Hertogenbosch")
        
    def test_sql_value(self):
        self.field.value = "'s Hertogenbosch"
        self.assertEqual(self.field.sql_value(), "'''s Hertogenbosch'")

    def test_is_geometry(self):
        self.assertEqual(self.field.is_geometry(), False)
        
    def test_sql_definition(self):
        self.assertEqual(self.field.sql_definition(), "naam TEXT NOT NULL")
        
_suite_b_field_regular = unittest.TestLoader().loadTestsFromTestCase(B_FieldRegularTestCase)

class B_FieldSpecialTestCase(unittest.TestCase):
    """
    unittests to test special cases of B_Field
    """

    def test_is_key_field(self):
        field = basis.B_Field("id", "INTEGER", "identificatie",
                              is_key_field=True)
        self.assertEqual(field.is_key_field, True)
        
    def test_integer_value_as_sql(self):
        field = basis.B_Field("nr", "INTEGER", "nummer")
        field.value = "20"
        self.assertEqual(field.sql_value(), '20')        

    def test_key_field_definition(self):
        """
        Test a created key field.
        """
        field = basis.B_Field("id", "INTEGER", "identificatie",
                              is_key_field=True)
        self.assertEqual(field.sql_definition(),
                         'id INTEGER NOT NULL PRIMARY KEY')

    def test_is_geometry(self):
        field = basis.B_Field("geometry", "MULTIPOLYGON", "woonplaatsGeometrie")
        self.assertEqual(field.is_geometry(), True)


_suite_b_field_special = unittest.TestLoader().loadTestsFromTestCase(B_FieldSpecialTestCase)

def pngformaat():
    pngFormaat = basis.B_Object("Pngformaat")
    pngFormaat.add_field(basis.B_Field("omsluitendeRechthoek", "POLYGON",
                                       "OmsluitendeRechthoek",
                                       to_object=gml.Envelope))
    pngFormaat.add_field(basis.B_Field("pixelsBreed", "TEXT", "PixelsBreed"))
    pngFormaat.add_field(basis.B_Field("pixelsHoog", "TEXT", "PixelsHoog"))
    pngFormaat.add_tags_to_process()
    return pngFormaat

def thema():
    a_thema = basis.B_Object("Thema")
    a_thema.add_field(basis.B_Field("themanaam", "TEXT", "Themanaam"))
    a_thema.add_field(basis.B_Field("EisVoorzorgmaatregel", "TEXT",
                                    "EisVoorzorgmaatregel"))
    a_thema.add_tags_to_process()
    return a_thema                    

def netbeheerderLevering():
    netbeheerderlevering = basis.B_Object("NetbeheerderLevering")
    netbeheerderlevering.add_field(basis.B_Field("bedrijfsnaam", "TEXT",
                                                 "Bedrijfsnaam"))
    netbeheerderlevering.add_field(basis.B_Field("storingsnummer", "TEXT",
                                                 "Storingsnummer"))
    netbeheerderlevering.add_field(basis.B_Field("themas", "CONTAINER",
                                                 "Themas", to_object=thema))
    netbeheerderlevering.add_tags_to_process()
    return netbeheerderlevering

class B_ObjectTestCase(unittest.TestCase):
    """
    unittests to test basic object, in this case a woonplaats..
    """
    
    def setUp(self):
        """
        For each test create a woonplaats read from xml file woonplaats.xml
        
        This unit_test is actually not an example how to create new objects.
        Objects should be subclassed! But in this case it is tested if it
        can be used to actually process parts of an xml element representing
        an old klic message.
        """
        klic_doc = basis.B_Object("klic_document")
        # to be included in init of derived classes, adding fields..
        klic_doc.add_field(basis.B_Field("klicnummer", "TEXT", "Klicnummer",
                                 is_key_field=True))
        klic_doc.add_field(basis.B_Field("png_formaat", "OBJECT", "Pngformaat",
                                         to_object=pngformaat))
        klic_doc.add_field(basis.B_Field("netbeheerderleveringen", "CONTAINER",
                                         "NetbeheerderLeveringen",
                                         to_object=netbeheerderLevering))
        
                        
        # include also how to process each tag found for object..
        # after creation.. (i.e. using method add_tags_to_process())
        klic_doc.add_tags_to_process()
##        print woonplaats.tag2field
        # to call from reader class (for each xml tag for this object
        # encountered.
        xml_file = open("data/basis/klic_old.xml")
        root = ET.fromstring(xml_file.read())
        xml_elem = root
##        xml_elem = xml_utils.find_xml_with_tag(root,"Leveringsinformatie",
##                                               None)
##        print(xml_woonplaats)
        klic_doc.process(xml_elem)
        self.klic_doc = klic_doc
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.klic_doc.field_names(),
                         ['klicnummer'])

    def test_field_values(self):
        self.assertEqual(self.klic_doc.field_values(),
                         ['14G166926'])

    def test_field_types(self):
        self.assertEqual(self.klic_doc.field_types(),
                         ['TEXT', 'OBJECT', 'CONTAINER'])

    def test_field_names_and_sql_values(self):
        self.assertEqual(self.klic_doc.field_names_and_sql_values(),
                         (['klicnummer'],
                          ["'14G166926'"]))

    def test_csv_header(self):
        self.assertEqual(self.klic_doc.csv_header(),
                         'klicnummer')

    def test_as_csv(self):
        self.assertEqual(self.klic_doc.as_csv(),
                        '14G166926')

    def test_as_sql(self):
        self.assertEqual(self.klic_doc.as_sql(),
                         "INSERT INTO klic_document (klicnummer) \
VALUES ('14G166926')")

    def test_sql_drop_table_statement(self):
        self.assertEqual(self.klic_doc.sql_drop_table_statement(),
                         "DROP TABLE if exists klic_document")

    def test_sql_create_table_statement(self):
        self.assertEqual(self.klic_doc.sql_create_table_statement(),
                         "CREATE TABLE klic_document (klicnummer TEXT NOT NULL \
PRIMARY KEY)")

    def test_value_in_included_object(self):
        an_object = self.klic_doc.field('png_formaat').value
        self.assertEqual(an_object.field_values(),
                         ['Polygon((194154 465849, 194154 465914, 194270 465914,\
 194270 465849, 194154 465849))', '1624', '910'])

    def test_value_in_included_container(self):
        a_container = self.klic_doc.field('netbeheerderleveringen').value
        themes = a_container[0].field("themas").value
        self.assertEqual(len(themes), 3)
        
 ##    def test_sql_add_geometry_statement(self):
##        self.assertEqual(self.klic_doc.sql_add_geometry_statement(),
##                         "SELECT AddGeometryColumn('woonplaats', 'geometry', \
##28992, 'MULTIPOLYGON', 'XY')")

##    def test_sql_create_index_statement(self):
##        self.assertEqual(self.klic_doc.sql_create_index_statement(),
##                         "SELECT CreateSpatialIndex('woonplaats', 'geometry')")
                             
_suite_b_object = unittest.TestLoader().loadTestsFromTestCase(B_ObjectTestCase)

unit_test_suites = [_suite_b_field_regular, _suite_b_field_special,
                    _suite_b_object]

def main():
    basis_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(basis_test_suite)
        
if __name__ == "__main__":
    main()
