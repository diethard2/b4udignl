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

class LeveringsInformatieTestCaseV1_5(unittest.TestCase):

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
     
_suite_leveringsInformatieV1_5 = unittest.TestLoader().loadTestsFromTestCase(LeveringsInformatieTestCaseV1_5)

class LeveringsInformatieTestCaseV2_1(unittest.TestCase):

    def setUp(self):
        """
        unit test to test reading LeveringsInformatie xml-tag
        this is part of the new klic message (after 01-01-2019).
        """
        # read the file
        xml_file = open("../test/data/18G007160_1/LI_18G007160_1.xml")
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
                         ['2.1', None, None, None, None, None, None])
        
    def test_pngFormaat(self):
        obj = self.leveringsinformatie
        omsluitende_rechthoek = obj.field("pngFormaat").value
        self.assertEqual(omsluitende_rechthoek.field_values(),
                         ['Polygon((154980.0 387980.0, 154980.0 388140.0, \
155120.0 388140.0, 155120.0 387980.0, 154980.0 387980.0))', '1960', '2240'])

    def test_bijlagenPerLevering(self):
        obj = self.leveringsinformatie
        bijlagen = obj.field("bijlagenPerLevering").value
        soort_lokatie = []
        for bijlage in bijlagen:
            soort = bijlage.field("soort_bijlage").value
            lokatie = bijlage.field("bestandlocatie").value
            soort_lokatie.append((soort,lokatie))
        self.assertEqual(soort_lokatie,
                         [("achtergrondkaart", "bronnen/GB_18G007160.png"),
                          ("geselecteerdGebied", "bronnen/SEL_18G007160.png"),
                          ('leveringsbrief', 'LI_18G007160_1.pdf'),
                          ('gebiedsinformatieLevering',
                           'GI_gebiedsinformatielevering_18G007160_1.xml')
                          ])

    def test_belanghebbenden(self):
        obj = self.leveringsinformatie
        belanghebbenden = obj.field("belanghebbenden").value
        bronhoudercodes = []
        for belanghebbende in belanghebbenden:
            code = belanghebbende.field("bronhoudercode").value
            bronhoudercodes.append(code)
        self.assertEqual(bronhoudercodes,
                         ['nbact2', 'nbact3', 'nbact4',
                          'nbact1', 'KL1031', 'KN1100'])
        
    def test_bijlagenPerNetbeheerder(self):
        obj = self.leveringsinformatie
        belanghebbenden = obj.field("belanghebbenden").value
        soort_lokatie = []
        for belanghebbende in belanghebbenden:
            bijlagen = belanghebbende.field("bijlagen").value
            if bijlagen is not None:
                for bijlage in bijlagen:
                    soort = bijlage.field("soort_bijlage").value
                    lokatie = bijlage.field("bestandlocatie").value
                    soort_lokatie.append((soort,lokatie))
        self.assertEqual(soort_lokatie,
                         [('algemeen',
                           'bronnen/nbact2/nl.imkl-nbact2_18G007160.algemeen.pdf'),
                          ('nietBetrokken',
                           'bronnen/nbact2/nl.imkl-nbact2_18G007160.nietBetrokken.pdf'),
                          ('algemeen',
                           'bronnen/nbact1/nl.imkl-nbact1_18G007160.filename.pdf'),
                          ('eigenTopo',
                           'bronnen/nbact1/ET_Netbeheerder+Actualiseren01_0000949099_18G007160.png')])

    def test_themabijlagenPerNetbeheerder(self):
        self.maxDiff = None
        obj = self.leveringsinformatie
        thema_soort_lokatie = []
        belanghebbenden = obj.field("belanghebbenden").value
        for belanghebbende in belanghebbenden:
            beheerdersinformatie = belanghebbende.field("beheerdersinformatie").value
            if beheerdersinformatie is not None:
                for informatie in beheerdersinformatie:
                    thema = informatie.field("thema").value
                    thema = thema.split('/')[-1]
                    themabijlagen = informatie.field("themaBijlagen").value
                    for bijlage in themabijlagen:
                        soort = bijlage.field("soort_bijlage").value
                        lokatie = bijlage.field("bestandlocatie").value
                        thema_soort_lokatie.append((thema,soort,lokatie))
        self.assertEqual(thema_soort_lokatie,
                         [("rioolOnderOverOfOnderdruk","ligging","bronnen/nbact1/LG_rioolOnderOverOfOnderdruk_Netbeheerder+Actualiseren01_0000949099_18G007160.png"),
                          ("buisleidingGevaarlijkeInhoud","ligging","bronnen/nbact1/LG_buisleidingGevaarlijkeInhoud_Netbeheerder+Actualiseren01_0000949099_18G007160.png"),
                          ('hoogspanning','ligging','bronnen/nbact1/LG_hoogspanning_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('middenspanning','annotatie','bronnen/nbact1/AN_middenspanning_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('middenspanning','ligging','bronnen/nbact1/LG_middenspanning_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('gasLageDruk','ligging','bronnen/nbact1/LG_gasLageDruk_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('water','ligging','bronnen/nbact1/LG_water_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('petrochemie','ligging','bronnen/nbact1/LG_petrochemie_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('datatransport','ligging','bronnen/nbact1/LG_datatransport_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('datatransport','annotatie','bronnen/nbact1/AN_datatransport_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('datatransport','maatvoering','bronnen/nbact1/MV_datatransport_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('datatransport','aansluiting','bronnen/nbact1/nl.imkl-nbact1_18G007160.filename.pdf'),
                          ('datatransport','profielschets','bronnen/nbact1/nl.imkl-nbact1_18G007160.filename.pdf'),
                          ('datatransport','overig','bronnen/nbact1/nl.imkl-nbact1_18G007160.filename.pdf'),
                          ('gasHogeDruk','ligging','bronnen/nbact1/LG_gasHogeDruk_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('gasHogeDruk','eisVoorzorgsmaatregel','bronnen/nbact1/nl.imkl-nbact1_18G007160.EV_gasHogeDruk_T_risicoHoog_gasHogeDruk.pdf'),
                          ('overig','ligging','bronnen/nbact1/LG_overig_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('warmte','ligging','bronnen/nbact1/LG_warmte_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('rioolVrijverval','ligging','bronnen/nbact1/LG_rioolVrijverval_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('laagspanning','ligging','bronnen/nbact1/LG_laagspanning_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('laagspanning','annotatie','bronnen/nbact1/AN_laagspanning_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('wees','ligging','bronnen/nbact1/LG_wees_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('landelijkHoogspanningsnet','ligging','bronnen/nbact1/LG_landelijkHoogspanningsnet_Netbeheerder+Actualiseren01_0000949099_18G007160.png'),
                          ('water', 'ligging', 'bronnen/KN1100/LG_water_PWN4_0000950324_18G007160.png')])

     
_suite_leveringsInformatieV2_1 = unittest.TestLoader().loadTestsFromTestCase(LeveringsInformatieTestCaseV2_1)

class OlieGasChemicalienPijpleidingTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test reading OlieGasChemicalienPijpleiding XML
        """
        # read the file
        xml_file = open("data/imkl/BuisGevaarlijkeInhoud.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "OlieGasChemicalienPijpleiding", None)
        self.buisGevaarlijkeInhoud = imkl.olieGasChemicalienPijpleiding()
        self.buisGevaarlijkeInhoud.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label','diameter','druk', 'fluid'])

    def test_field_values(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.field_values(),
                         ['nl.imkl-nbact1.ogc00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00057','nl.imkl-nbact1.ul00005',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z',None,'underground',
                          'nl.imkl-nbact1.xg00009','','0.0','0.0',
                          'http://inspire.ec.europa.eu/codelist/OilGasChemicalsProductTypeValue/naturalGas'])

    def test_csv_header(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.csv_header(),
                         'id;registratiedatum;network_id;link_id;status;\
validFrom;validTo;verticalPosition;geom_id;label;diameter;druk;fluid')

    def test_as_csv(self):
        self.assertEqual(self.buisGevaarlijkeInhoud.as_csv(),
                         'nl.imkl-nbact1.ogc00001;2001-12-17T09:30:47.0Z;\
nl.imkl-nbact1.un00057;nl.imkl-nbact1.ul00005;\
http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused;\
2001-12-17T09:30:47.0Z;None;underground;nl.imkl-nbact1.xg00009;;0.0;0.0;http:\
//inspire.ec.europa.eu/codelist/OilGasChemicalsProductTypeValue/naturalGas')
    
_suite_olieGasChemicalienPijpleiding = unittest.TestLoader().loadTestsFromTestCase(OlieGasChemicalienPijpleidingTestCase)

class ExtraGeometrieTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.ExtraGeometrie
        """
        # read the file
        xml_file = open("data/imkl/ExtraGeometrie.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "ExtraGeometrie",
                                                       None)
        self.extraGeometrie = imkl.extraGeometrie()
        self.extraGeometrie.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.extraGeometrie.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum',
                          'network_id', 'vlakgeometrie'])

    def test_field_values(self):
        self.assertEqual(self.extraGeometrie.field_values(),
                         ['nl.imkl-nbact1.xg00009','2015-10-19T09:30:47.0Z',
                          '9999-01-01T09:30:47.0','nl.imkl-nbact1.un00057',
                          'Polygon((155052.000 388010.000, \
155050.000 388008.000, 155048.000 388010.000, 155050.000 388012.000, \
155052.000 388010.000))'])

    def test_csv_header(self):
        self.assertEqual(self.extraGeometrie.csv_header(),
                         'id;registratiedatum;vervaldatum;network_id;vlakgeometrie')

    def test_as_csv(self):
        self.assertEqual(self.extraGeometrie.as_csv(),
                         'nl.imkl-nbact1.xg00009;2015-10-19T09:30:47.0Z;\
9999-01-01T09:30:47.0;nl.imkl-nbact1.un00057;Polygon((155052.000 388010.000, \
155050.000 388008.000, 155048.000 388010.000, 155050.000 388012.000, \
155052.000 388010.000))')
    
_suite_extraGeometrie = unittest.TestLoader().loadTestsFromTestCase(ExtraGeometrieTestCase)

class GraafpolygoonTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.graafpolygoon
        """
        # read the file
        xml_file = open("data/imkl/graafpolygoon.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Graafpolygoon",
                                                       None)
        self.imkl_obj = imkl.graafpolygoon()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'geometrie'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-KA0000._Graafpolygoon_18G007160',
                          'Polygon((154980.0 387980.0, 155120.0 387980.0, \
155120.0 388140.0, 154980.0 388140.0, 154980.0 387980.0))'])

_suite_GraafpolygoonTestCase = unittest.TestLoader().loadTestsFromTestCase(GraafpolygoonTestCase)

class GebiedsinformatieAanvraagTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.gebiedsinformatieAanvraag
        """
        # read the file
        xml_file = open("data/imkl/gebiedsinformatieAanvraag.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "GebiedsinformatieAanvraag",
                                                       None)
        self.imkl_obj = imkl.gebiedsinformatieAanvraag()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','vervaldatum','ordernummer',
                          'positienummer','klicMeldnummer','referentie'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-KA0000._GebiedsinformatieAanvraag_18G007160',
                          '2018-07-19T12:02:03.000+02:00',None,'9806758830',
                          '0000000010','18G007160','Tbv Klicviewer - Graaf'])

    def test_contact_persoon(self):
        aanvragen = self.imkl_obj.field("aanvragers").value
        aanvraag = aanvragen[0]
        persoon = aanvraag.field("contactpersoon").value
        contact = persoon.field("contact").value
        naam = contact.field("naam").value
        telefoon = contact.field("telefoon").value
        email = contact.field("email").value
        self.assertEqual((naam,telefoon,email),
                         ('Niet beschikbaar - TODO','0881234566',
                          'klic.testers@kadaster.nl'))

    def test_contact_organisatie(self):
        aanvragen = self.imkl_obj.field("aanvragers").value
        aanvraag = aanvragen[0]
        organisatie = aanvraag.field("organisatie").value
        organisatie = organisatie[0]
        bezoekadres = organisatie.field("bezoekadres").value
        adres = bezoekadres.field("adres").value
        straat = adres.field("openbareRuimte").value
        huisnummer = adres.field("huisnummer").value
        woonplaats = adres.field("woonplaats").value
        postcode = adres.field("postcode").value
        landcode = adres.field("landcode").value
        self.assertEqual((straat,huisnummer,postcode,woonplaats,landcode),
                         ('Laan van Westenenk','701',
                          '7334DP', 'APELDOORN', 'NL'))
        
_suite_GebiedsinformatieAanvraagTestCase = unittest.TestLoader().loadTestsFromTestCase(GebiedsinformatieAanvraagTestCase)

class AanduidingEVTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.AanduidingEisVoorzorgsmaatregel
        """
        # read the file
        xml_file = open("data/imkl/aanduiding_ev.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "AanduidingEisVoorzorgsmaatregel",
                                                       None)
        self.imkl_obj = imkl.aanduidingEisVoorzorgsmaatregel()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum', 'label',
                          'network_id', 'eisVoorzorgsmaatregel',
                          'netbeheerderNetOmschrijving','netbeheerderWerkAanduiding',
                          'geometrie'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.EV1','2001-12-17T09:30:47.00+01:00',
                          None,
                          'EisVoorzorgsmaatregel GHD-leiding Best-west',
                          'nl.imkl-nbact1.un00054', 'GHD-T-W3',
                          'EV1-gebied transport hoofdleiding','W3-hoog',
                          'Polygon((155104 388038, 155098 388046, 155088 388043, \
155088 388032, 155098 388029, 155104 388038))'])
        
    def test_contact_voorzorgsmaatregel(self):
        contactpersoon = self.imkl_obj.field('contactVoorzorgsmaatregel').value
        contact = contactpersoon.field('contact').value
        naam = contact.field("naam").value
        telefoon = contact.field("telefoon").value
        email = contact.field("email").value
        self.assertEqual((naam,telefoon,email),
                         ('Contactnaam EV1','088-183 1111',
                          'EV1@nbact1.nl'))
  
_suite_AanduidingEVTestCase = unittest.TestLoader().loadTestsFromTestCase(AanduidingEVTestCase)

class BelanghebbendeTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.belanghebbende
        """
        # read the file
        xml_file = open("data/imkl/belanghebbende.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Belanghebbende",
                                                       None)
        self.imkl_obj = imkl.belanghebbende()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','vervaldatum','bronhoudercode',
                          'beheerdersinformatieGeleverd','betrokkenBijAanvraag',
                          'eisVoorzorgsmaatregel','netbeheerderNetOmschrijving',
                          'idGeraaktBelang','idNetbeheerder'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact2._Belanghebbende_18G007160-1',
                          '2018-07-19T12:04:10.000+02:00',None,None,'true',
                          'false','false',None,
                          'nl.imkl-nbact2._Belang_5012613-300',
                          'nl.imkl-nbact2._Beheerder'])

_suite_BelanghebbendeTestCase = unittest.TestLoader().loadTestsFromTestCase(BelanghebbendeTestCase)

class BelangTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.belang
        """
        # read the file
        xml_file = open("data/imkl/belang.xml")
        root = ET.fromstring(xml_file.read())
        tag = imkl.BELANG
        self.xml_element = xml_utils.find_xml_with_tag(root, tag,
                                                       None)
        self.imkl_obj = imkl.belang()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','vervaldatum','omschrijving'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact2._Belang_5012613-300',
                          '2016-08-09T00:00:00.000+02:00',None,
                          '02 in best'])
        
    def test_contactAanvraag(self):
        contactAanvraag = self.imkl_obj.field("contactAanvraag").value
        contact = contactAanvraag.field("aanvraagSoortContact").value
        naam = contact.field("naam").value
        telefoon = contact.field("telefoon").value
        email = contact.field("email").value
        self.assertEqual((naam,telefoon,email),
                         ('BMK Netbeheerder Actualiseren02','0887891325',
                          'klic_levering@integratie.kadaster.nl'))
        
    def test_contactNetinformatie(self):
        contactNetinformatie = self.imkl_obj.field("contactNetinformatie").value
        contact = contactNetinformatie.field("aanvraagSoortContact").value
        naam = contact.field("naam").value
        telefoon = contact.field("telefoon").value
        email = contact.field("email").value
        self.assertEqual((naam,telefoon,email),
                         ('Contact Netinformatie Naam DUMMY','1234567890',
                          'ContactNetinformatieEmailDummy@kadaster.nl'))
    
    def test_contactBeschadiging(self):
        contactBeschadiging = self.imkl_obj.field("contactBeschadiging").value
        contact = contactBeschadiging.field("contact").value
        naam = contact.field("naam").value
        telefoon = contact.field("telefoon").value
        email = contact.field("email").value
        self.assertEqual((naam,telefoon,email),
                         ('Contact Beschadiging Naam DUMMY','1234567890',
                          'ContactBeschadigingEmailDummy@kadaster.nl'))

_suite_BelangTestCase = unittest.TestLoader().loadTestsFromTestCase(BelangTestCase)

class AppurtenanceTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.appurtenance
        """
        # read the file
        xml_file = open("data/imkl/appurtenance.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Appurtenance",
                                                       None)
        self.imkl_obj = imkl.appurtenance()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'network_id',
                          'currentStatus', 'validFrom', 'validTo',
                          'verticalPosition', 'appurtenanceType',
                          'label', 'geometry'])

    def test_field_values(self):
        self.maxDiff = None
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.app00001',
                          '2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00007',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z',
                          '2001-12-17T09:30:47.0Z',
                          'onGroundSurface',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/ElectricityAppurtenanceTypeIMKLValue/aarding',
                          '',
                          'Point(155000.000 388090.000)'])

_suite_AppurtenanceTestCase = unittest.TestLoader().loadTestsFromTestCase(AppurtenanceTestCase)

class GebiedsinformatieLeveringTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.gebiedsinformatieLevering
        """
        # read the file
        xml_file = open("data/imkl/gebiedsinformatieLevering.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "GebiedsinformatieLevering",
                                                       None)
        self.imkl_obj = imkl.gebiedsinformatieLevering()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum',
                          'leveringsvolgnummer','datumLeveringSamengesteld',
                          'indicatieLeveringCompleet'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-KA0000._GebiedsinformatieLevering_18G007160-1',
                          '2018-07-19T12:07:09.449+02:00',None,'1',
                          '2018-07-19T12:07:09.449+02:00',
                          'true'])

    def test_achtergrondkaart(self):
        kaarten = self.imkl_obj.field("achtergrondkaarten").value
        kaart = kaarten[0]
        soort_ref = kaart.field('achtergrondkaartSoort').value
        i = soort_ref.rindex('/')
        soort = soort_ref[i+1:]
        bron = kaart.field('kaartreferentie').value
        self.assertEqual((soort, bron),
                         ('bgtBestaand','bronnen/GB_18G007160.png'))

_suite_GebiedsinformatieLeveringTestCase = unittest.TestLoader().loadTestsFromTestCase(GebiedsinformatieLeveringTestCase)

class AnnotatieTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.annotatie
        """
        # read the file
        xml_file = open("data/imkl/annotatie.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Annotatie",
                                                       None)
        self.imkl_obj = imkl.annotatie()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum', 'label',
                          'omschrijving', 'network_id', 'annotatieType',
                          'rotatiehoek', 'geometry'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.an00001','1996-05-08T00:00:00+02:00',
                          '9999-01-01T00:00:00+01:00', 'annotatieLabel',
                          'Omschrijving Annotatie nl.imkl-nbact1.an00001',
                          'nl.imkl-nbact1.un00002',
                          'http://definities.geostandaarden.nl/imkl2015/id\
/waarde/AnnotatieTypeValue/annotatiepijlpunt', '45.0',
                          'Point(155000.000 388030.000)'])
        
    def test_label_positie(self):
        obj = self.imkl_obj.field("labelpositie").value[0]
        values = []
        for field_name in ("aangrijpingHorizontaal","aangrijpingVerticaal"):
            value = obj.field(field_name).value
            i = value.rindex('/')
            values.append(value[i+1:])
        self.assertEqual(values, ['0.5','0'])
            

_suite_AnnotatieTestCase = unittest.TestLoader().loadTestsFromTestCase(AnnotatieTestCase)

class MaatvoeringTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.maatvoering
        """
        # read the file
        xml_file = open("data/imkl/maatvoering.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Maatvoering",
                                                       None)
        self.imkl_obj = imkl.maatvoering()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum', 'label',
                          'omschrijving', 'network_id', 'maatvoeringsType',
                          'rotatiehoek', 'geometry'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.mv00002','2001-12-17T09:30:47.0Z',
                          '2021-12-17T09:30:47.0Z','maatvoeringsLabel',
                          'Omschrijving Maatvoering','nl.imkl-nbact1.un00050',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/MaatvoeringsTypeValue/maatvoeringslabel',
                          '45.0','Point(155040.000 388070.000)'])
        
    def test_label_positie(self):
        obj = self.imkl_obj.field("labelpositie").value[0]
        values = []
        for field_name in ("aangrijpingHorizontaal","aangrijpingVerticaal"):
            value = obj.field(field_name).value
            i = value.rindex('/')
            values.append(value[i+1:])
        self.assertEqual(values, ['0.5','0'])
            

_suite_MaatvoeringTestCase = unittest.TestLoader().loadTestsFromTestCase(MaatvoeringTestCase)

class BijlageTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.bijlage
        """
        # read the file
        xml_file = open("data/imkl/bijlage.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Bijlage",
                                                       None)
        self.imkl_obj = imkl.bijlage_v2()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum',
                          'bijlageType', 'bestandlocatie', 'bestandMediaType',
                          'bestandIdentificator'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact2.algemeen',
                          '2001-12-17T09:30:47.0Z', None,
                          'http://definities.geostandaarden.nl/imkl2015/id/\
waarde/BijlageTypeValue/algemeen', 'bronnen/nbact2/nl.imkl-nbact2_18G007160.algemeen.pdf',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/BestandMediaTypeValue/PDF',
                          'nl.imkl-nbact2.algemeen'])

_suite_BijlageTestCase = unittest.TestLoader().loadTestsFromTestCase(BijlageTestCase)

class DiepteTovMaaiveldTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.?
        """
        # read the file
        xml_file = open("data/imkl/diepte.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "DiepteTovMaaiveld",
                                                       None)
        self.imkl_obj = imkl.diepteTovMaaiveld()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum','label',
                          'omschrijving','network_id','diepteNauwkeurigheid',
                          'dieptePeil','datumOpmetingDieptePeil',
                          'diepteAangrijpingspunt','geometry'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.dmaai00001','2001-12-17T09:30:47',
                          '2031-12-17T09:30:48','','','nl.imkl-nbact1.un00039',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/NauwkeurigheidDiepteValue/tot50cm',
                          '2.43','2015-12-17T09:30:47',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/DiepteAangrijpingspuntValue/bovenkant',
                          'Point(155030.000 388050.000)'])

_suite_DiepteTovMaaiveldTestCase = unittest.TestLoader().loadTestsFromTestCase(DiepteTovMaaiveldTestCase)

class DiepteNAPTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.?
        """
        # read the file
        xml_file = open("data/imkl/diepte.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "DiepteNAP",
                                                       None)
        self.imkl_obj = imkl.diepteNAP()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum','label',
                          'omschrijving','network_id','diepteNauwkeurigheid',
                          'dieptePeil','datumOpmetingDieptePeil',
                          'diepteAangrijpingspunt','geometry', 'maaiveldPeil',
                          'datumOpmetingMaaiveldPeil'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.dnap00001',
                          '2001-12-17T09:30:47','2031-12-17T09:30:48',
                          'Label DiepteNap','Omschrijving DiepteNap',
                          'nl.imkl-nbact1.un00038',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/NauwkeurigheidDiepteValue/tot50cm',
                          '2.43','2015-12-17T09:30:47',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/DiepteAangrijpingspuntValue/bovenkant',
                          'Point(155030.000 388040.000)',
                          '5.55','2015-11-16T08:00:00'])

_suite_DiepteNAPTestCase = unittest.TestLoader().loadTestsFromTestCase(DiepteNAPTestCase)

class DuctTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.duct
        """
        # read the file
        xml_file = open("data/imkl/duct.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Duct",
                                                       None)
        self.imkl_obj = imkl.duct()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label', 'utilityDeliveryType',
                          'warningType','ductWidth'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.duct00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00040','nl.imkl-nbact1.ul00001',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z','2001-12-17T09:30:47.0Z',
                          'underground','nl.imkl-nbact1.xg00001','',
                          'http://inspire.ec.europa.eu/codelist/UtilityNetworkTypeValue/electricity',
                          'http://inspire.ec.europa.eu/codelist/WarningTypeValue/net',
                          '1.5'])

_suite_DuctTestCase = unittest.TestLoader().loadTestsFromTestCase(DuctTestCase)

class KabelbedTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.kabelbed
        """
        # read the file
        xml_file = open("data/imkl/kabelbed.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Kabelbed",
                                                       None)
        self.imkl_obj = imkl.kabelbed()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label', 'warningType','ductWidth',
                          'omschrijving'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.kbed00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00047','nl.imkl-nbact1.ul00003',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z','2001-12-17T09:30:47.0Z',
                          'underground','nl.imkl-nbact1.xg00004',
                          'Label KabelBed',
                          'http://inspire.ec.europa.eu/codelist/WarningTypeValue/net',
                          '0','Omschrijving Kabelbed'])

_suite_KabelbedTestCase = unittest.TestLoader().loadTestsFromTestCase(KabelbedTestCase)

class KastTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.kast
        """
        # read the file
        xml_file = open("data/imkl/kast.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Kast",
                                                       None)
        self.imkl_obj = imkl.kast()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','network_id','status', 'validFrom','validTo',
                          'verticalPosition','geometry','geom_id', 'label',
                          'bovengrondsZichtbaar','geoNauwkeurigheidXY'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.kast00001','nl.imkl-nbact1.un00048',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/projected',
                          '1996-05-08T00:00:00+02:00',
                          '9999-01-01T00:00:00+01:00','onGroundSurface',
                          'Point(155040.000 388040.000)',
                          'nl.imkl-nbact1.xg00005','','true',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/NauwkeurigheidValue/tot100cm'])

_suite_KastTestCase = unittest.TestLoader().loadTestsFromTestCase(KastTestCase)

class MangatTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.mangat
        """
        # read the file
        xml_file = open("data/imkl/mangat.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Mangat",
                                                       None)
        self.imkl_obj = imkl.mangat()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','network_id','status', 'validFrom','validTo',
                          'verticalPosition','geometry','geom_id', 'label'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.mgat00001','nl.imkl-nbact1.un00054',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z','2001-12-17T09:30:47.0Z',
                          'onGroundSurface','Point(155040.000 388110.000)',
                          'nl.imkl-nbact1.xg00006',''])

_suite_MangatTestCase = unittest.TestLoader().loadTestsFromTestCase(MangatTestCase)

class MastTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.mast
        """
        # read the file
        xml_file = open("data/imkl/mast.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Mast",
                                                       None)
        self.imkl_obj = imkl.mast()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','network_id','status', 'validFrom','validTo',
                          'verticalPosition','geometry','geom_id', 'label',
                          'poleHeight'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.mast00001','nl.imkl-nbact1.un00056',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/functional',
                          '2001-12-17T09:30:47.0Z','2001-12-17T09:30:47.0Z',
                          'onGroundSurface','Point(155050.000 388000.000)',
                          'nl.imkl-nbact1.xg00008','','100.0'])

_suite_MastTestCase = unittest.TestLoader().loadTestsFromTestCase(MastTestCase)

class EigenTopografieTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.eigenTopografie
        """
        # read the file
        xml_file = open("data/imkl/eigen_topo.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "EigenTopografie",
                                                       None)
        self.imkl_obj = imkl.eigenTopografie()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum','label',
                          'omschrijving','status', 'typeTopografischObject',
                          'ligging'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.et00001','2001-12-17T09:30:47.0Z',
                          '9999-01-01T09:30:47.0','Label EigenTopografie',
                          'Omschrijving EigenTopografie',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/EigenTopografieStatusValue/bestaand',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/TopografischObjectTypeValue/hectometerpaal',
                          'Point(155030.000 388070.000)'])

_suite_EigenTopografieTestCase = unittest.TestLoader().loadTestsFromTestCase(EigenTopografieTestCase)

class ElektriciteitskabelTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.elektriciteitskabel
        """
        # read the file
        xml_file = open("data/imkl/elec_kabel.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Elektriciteitskabel",
                                                       None)
        self.imkl_obj = imkl.elektriciteitskabel()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label', 'warningType',
                          'operatingVoltage','nominalVoltage',
                          'geoNauwkeurigheidXY', 'kabelDiameter'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.el00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00041','nl.imkl-nbact1.ul00002',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/disused',
                          '2001-12-17T09:30:47.0Z',None,'underground',
                          'nl.imkl-nbact1.xg00002',None,
                          'http://inspire.ec.europa.eu/codelist/WarningTypeValue/net',
                          '0.3','100000.0',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/NauwkeurigheidXYvalue/onbekend',
                          '30.0'])

_suite_ElektriciteitskabelTestCase = unittest.TestLoader().loadTestsFromTestCase(ElektriciteitskabelTestCase)

class MantelbuisTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.Mantelbuis
        """
        # read the file
        xml_file = open("data/imkl/mantelbuis.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Mantelbuis",
                                                       None)
        self.imkl_obj = imkl.mantelbuis()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label', 'warningType',
                          'diameter','materiaal'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.mb00001','2001-12-17T09:30:47.0Z',
                          'nl.imkl-nbact1.un00055','nl.imkl-nbact1.ul00004',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/projected',
                          '2001-12-17T09:30:47.0Z','2001-12-17T09:30:47.0Z',
                          'underground','nl.imkl-nbact1.xg00007','',
                          'http://inspire.ec.europa.eu/codelist/WarningTypeValue/net',
                          '100',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/PipeMaterialTypeIMKLValue/asbestos-cement'])

_suite_MantelbuisTestCase = unittest.TestLoader().loadTestsFromTestCase(MantelbuisTestCase)

class OverigTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.overig
        """
        # read the file
        xml_file = open("data/imkl/overig.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "Overig",
                                                       None)
        self.imkl_obj = imkl.overig()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id','registratiedatum','network_id', 'link_id',
                          'status', 'validFrom','validTo', 'verticalPosition',
                          'geom_id', 'label', 'warningType',
                          'geoNauwkeurigheidXY','kabelDiameter','materiaal',
                          'buisDiameter','druk','producttype'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.overig00001','2017-04-24T09:30:47.0Z',
                          'nl.imkl-nbact1.un00079','nl.imkl-nbact1.ul00024',
                          'http://inspire.ec.europa.eu/codelist/ConditionOfFacilityValue/functional',
                          '2017-04-24T09:30:47.0Z','2020-04-24T09:30:47.0Z',
                          'underground','nl.imkl-nbact1.xg00015','Label Overig',
                          'http://inspire.ec.europa.eu/codelist/WarningTypeValue/net',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/NauwkeurigheidXYvalue/tot100cm',
                          '2','http://definities.geostandaarden.nl/imkl2015/id/waarde/PipeMaterialTypeIMKLValue/polyester',
                          '12.5','5.3',
                          'Bierleiding van brouwerij naar grootafnemer'])

_suite_OverigTestCase = unittest.TestLoader().loadTestsFromTestCase(OverigTestCase)

class EVbijlageTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.eisVoorzorgsmaatregelBijlage
        """
        # read the file
        xml_file = open("data/imkl/ev_bijlage.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "EisVoorzorgsmaatregelBijlage",
                                                       None)
        self.imkl_obj = imkl.eisVoorzorgsmaatregelBijlage()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum',
                          'bijlageType', 'bestandlocatie', 'bestandMediaType',
                          'bestandIdentificator','thema',
                          'eisVoorzorgsmaatregel', 'toelichting'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1._EisVoorzorgsmaatregelBijlage_18G007160_gasHogeDruk',
                          '2018-07-19T12:04:12.376+02:00',None,
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/BijlageTypeValue/eisVoorzorgsmaatregel',
                          'bronnen/nbact1/nl.imkl-nbact1_18G007160.EV_gasHogeDruk_T_risicoHoog_gasHogeDruk.pdf',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/BestandMediaTypeValue/PDF',
                          'nl.imkl-nbact1.EV_gasHogeDruk_T_risicoHoog_gasHogeDruk',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/Thema/gasHogeDruk',
                          'GHD-T-W3',
                          'transport_hoofdleiding risico HOOG (bij deze werkzaamheden)'])

_suite_EVbijlageTestCase = unittest.TestLoader().loadTestsFromTestCase(EVbijlageTestCase)

class ExtraDetailinfoTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.extraDetailinfo
        """
        # read the file
        xml_file = open("data/imkl/extra_detail_info.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "ExtraDetailinfo",
                                                       None)
        self.imkl_obj = imkl.extraDetailinfo()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['id', 'registratiedatum', 'vervaldatum',
                          'label','omschrijving','network_id','extraInfoType',
                          'bestandIdentificator','ligging'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.edi00001','2015-10-15T09:30:47.0Z',
                          '9999-01-01T10:30:47.0Z','Label ExtraDetailInfo',
                          'Omschrijving ExtraDetailInfo',
                          'nl.imkl-nbact1.un00042',
                          'http://definities.geostandaarden.nl/imkl2015/id/waarde/ExtraDetailInfoTypeValue/aansluiting',
                          'nl.imkl-nbact1.filename',
                          'Point(155030.000 388110.000)'])

    def test_adres(self):
        adres = self.imkl_obj.field("adres").value
        adres = adres[0]
        straat = adres.field("openbareRuimte").value
        huisnummer = adres.field("huisnummer").value
        woonplaats = adres.field("woonplaats").value
        postcode = adres.field("postcode").value
        self.assertEqual((straat,huisnummer,postcode,woonplaats),
                         ('Een openbareruimte naam','701',
                          '7334DP', 'Apeldoorn'))        

_suite_ExtraDetailinfoTestCase = unittest.TestLoader().loadTestsFromTestCase(ExtraDetailinfoTestCase)

class BoundsTestCase(unittest.TestCase):

    def setUp(self):
        """
        unit test to test imkl.?
        """
        # read the file
        xml_file = open("data/imkl/gml_envelope.xml")
        root = ET.fromstring(xml_file.read())
        self.xml_element = xml_utils.find_xml_with_tag(root, "BoundedBy",
                                                       None)
        self.imkl_obj = imkl.boundedBy()
        self.imkl_obj.process(self.xml_element)
        xml_file.close()

    def test_field_names(self):
        self.assertEqual(self.imkl_obj.field_names(),
                         ['envelope'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['Polygon((154980.0 387980.0, 154980.0 388140.0, \
155120.0 388140.0, 155120.0 387980.0, 154980.0 387980.0))'])

_suite_BoundsTestCase = unittest.TestLoader().loadTestsFromTestCase(BoundsTestCase)

##class TestCase(unittest.TestCase):
##
##    def setUp(self):
##        """
##        unit test to test imkl.?
##        """
##        # read the file
##        xml_file = open("data/imkl/.xml")
##        root = ET.fromstring(xml_file.read())
##        self.xml_element = xml_utils.find_xml_with_tag(root, "",
##                                                       None)
##        self.imkl_obj = imkl.()
##        self.imkl_obj.process(self.xml_element)
##        xml_file.close()
##
##    def test_field_names(self):
##        self.assertEqual(self.imkl_obj.field_names(),
##                         ['id', ''])
##
##    def test_field_values(self):
##        self.assertEqual(self.imkl_obj.field_values(),
##                         ['',
##                          ''])
##
##_suite_TestCase = unittest.TestLoader().loadTestsFromTestCase(TestCase)

unit_test_suites = [_suite_leveringsInformatieV1_5, _suite_leveringsInformatieV2_1,
                    _suite_olieGasChemicalienPijpleiding, _suite_extraGeometrie,
                    _suite_GraafpolygoonTestCase, _suite_GebiedsinformatieAanvraagTestCase,
                    _suite_AanduidingEVTestCase, _suite_BelanghebbendeTestCase,
                    _suite_BelangTestCase, _suite_AppurtenanceTestCase,
                    _suite_GebiedsinformatieLeveringTestCase,
                    _suite_AnnotatieTestCase, _suite_MaatvoeringTestCase,
                    _suite_BijlageTestCase, _suite_DiepteTovMaaiveldTestCase,
                    _suite_DiepteNAPTestCase, _suite_DuctTestCase,
                    _suite_KabelbedTestCase, _suite_KastTestCase,
                    _suite_MangatTestCase, _suite_EigenTopografieTestCase,
                    _suite_ElektriciteitskabelTestCase,_suite_EVbijlageTestCase,
                    _suite_ExtraDetailinfoTestCase, _suite_BoundsTestCase,
                    _suite_MantelbuisTestCase, _suite_MastTestCase,
                    _suite_OverigTestCase]

def main():
    imkl_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(imkl_test_suite)
        
if __name__ == "__main__":
    main()        
