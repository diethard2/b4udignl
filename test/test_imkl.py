"""
/***************************************************************************
 Unit test suite to test imkl objects.
 -------------------
 begin                : 01-08-2018
 copyright            : (C) 2018 by Diethard Jansen
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
from core import imkl, gml, xml_utils
import xml.etree.ElementTree as ET

class LeveringsInformatieTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test reading LeveringsInformatie xml-tag
        this is part of the old klic message (before 01-01-2019).
        """
        # read the file
        xml_file = open("../testMsg/14G166926_1/LI_14G166926_1.xml")
        self.xml_element = ET.fromstring(xml_file.read())
        self.leveringsinformatie = imkl.leveringsinformatie()
        self.leveringsinformatie.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.leveringsinformatie.field_names(),
                         ['version', 'klicnummer', 'ordernummer',
                          'meldingsoort','datumTijdAanvraag',
                          'klantReferentie', 'graafpolygoon'])

    def test_field_values(self):
        self.assertEqual(self.leveringsinformatie.field_values(),
                         ['1.5', '14G166926', '9805738757',
                          'Graafmelding', '2014-04-30T14:07:00.000+02:00',
                          'KADASTER TESTMELDING',
                          'Polygon((194154 465912, 194154 465849, 194270 465850, 194269 465914, 194154 465912))'])
        
    def test_omsluitendeRechthoek(self):
        obj = self.leveringsinformatie
        omsluitende_rechthoek = obj.field("omsluitendeRechthoek").value
        self.assertEqual(omsluitende_rechthoek.field_values(),
                         ['Polygon((194154 465849, 194154 465914, \
194270 465914, 194270 465849, 194154 465849))', '1624', '910'])

    def test_layer_names(self):
        obj = self.leveringsinformatie
        netbeheerders = obj.field("netbeheerderLeveringen").value
        layer_names = []
        for netbeheerder in netbeheerders:
            themas = netbeheerder.field("themas").value
            if themas is not None:
                for thema in themas:
                    ligging = thema.field("ligging").value
                    maatvoering = thema.field("maatvoering").value
                    annotatie = thema.field("annotatie").value
                    for theme_layer in (ligging, maatvoering, annotatie):
                        if theme_layer is not None:
                            layer_name = theme_layer.field("bestandsnaam").value
                            layer_names.append(layer_name)
        self.maxDiff = None
        self.assertEqual(layer_names,
                         ['LG_middenspanning_Liander_0000574962_14G166926.png',
                          'MV_middenspanning_Liander_0000574962_14G166926.png',
                          'AN_middenspanning_Liander_0000574962_14G166926.png',
                          'LG_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'MV_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'AN_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'LG_laagspanning_Liander_0000574962_14G166926.png',
                          'MV_laagspanning_Liander_0000574962_14G166926.png',
                          'AN_laagspanning_Liander_0000574962_14G166926.png',
                          'LG_riool+vrijverval_APELDOORN_0000586326_14G166926.png',
                          'LG_datatransport_KPN_0000546663_14G166926.png',
                          'MV_datatransport_KPN_0000546663_14G166926.png',
                          'AN_datatransport_KPN_0000546663_14G166926.png',
                          'LG_datatransport_trent_0000585212_14G166926.png',
                          'MV_datatransport_trent_0000585212_14G166926.png',
                          'AN_datatransport_trent_0000585212_14G166926.png',
                          'LG_water_Vitens_0000552354_14G166926.png',
                          'AN_water_Vitens_0000552354_14G166926.png'])

    def test_pdf_names(self):
        obj = self.leveringsinformatie
        netbeheerders = obj.field("netbeheerderLeveringen").value
        pdfs = []
        pdf_names = []
        for netbeheerder in netbeheerders:
            themas = netbeheerder.field("themas").value
            if themas is not None:
                for thema in themas:
                    aansluitschetsen = thema.field("huisaansluitschetsen").value
                    if aansluitschetsen is not None:
                        pdfs.extend(aansluitschetsen)
                    themabijlagen = thema.field("themaBijlagen").value
                    if themabijlagen is not None:
                        pdfs.extend(themabijlagen)
            bijlagen = netbeheerder.field("bijlagen").value
            if bijlagen is not None:
                pdfs.extend(bijlagen)
            pdf_names = [pdf.field("bestandsnaam").value for pdf in pdfs]
        self.maxDiff = None
        self.assertEqual(pdf_names,
                         ['HA_laagspanning_Liander_0000574962_14G166926_7334DP_701.pdf',
                          'BL_Liander_0000574962_14G166926_BriefAlgemeen.pdf',
                          'BL_Liander_0000574962_14G166926_OntwerpContouren.pdf',
                          'BL_APELDOORN_0000586326_14G166926_Graafantwoord.pdf',
                          'BL_Eurofiber_0000560460_14G166926_Brief-GeenBelang.pdf',
                          'HA_datatransport_KPN_0000546663_14G166926_7334DP_701.PDF',
                          'TB_datatransport_KPN_0000546663_14G166926_Waterkruisingen.PDF',
                          'BL_KPN_0000546663_14G166926_Brief-belang.PDF',
                          'BL_Reggefiber_0000579733_14G166926_Brief-GeenBelang.pdf',
                          'BL_Tele2_0000546705_14G166926_Brief-GeenBelang.pdf',
                          'BL_trent_0000585212_14G166926_brief.pdf',
                          'BL_upc_0000565862_14G166926_brief.pdf',
                          'BL_upc_0000565862_14G166926_voorwaarden.pdf',
                          'HA_water_Vitens_0000552354_14G166926_7334+DP_701.pdf',
                          'BL_Vitens_0000552354_14G166926_BriefAlgemeenMetOverzichtskaart.pdf'
                          ])
     
_suite_leveringsInformatie = unittest.TestLoader().loadTestsFromTestCase(LeveringsInformatieTestCase)

class OlieGasChemicalienPijpleidingTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test reading OlieGasChemicalienPijpleiding XML
        """
        # read the file
        xml_file = open("data/18G007160_1/imkl_elements/BuisGevaarlijkeInhoud.xml")
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
        xml_file = open("data/18G007160_1/imkl_elements/ExtraGeometrie.xml")
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

unit_test_suites = [_suite_leveringsInformatie,
                    _suite_olieGasChemicalienPijpleiding, _suite_extraGeometrie]

def main():
    imkl_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(imkl_test_suite)
        
if __name__ == "__main__":
    main()        
