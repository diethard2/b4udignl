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
        xml_file = open("data/imkl/ExtraGeometrie.xml")
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
                         ['id', 'registratiedatum','ordernummer',
                          'positienummer', 'klicMeldnummer', 'referentie'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-KA0000._GebiedsinformatieAanvraag_18G007160',
                          '2018-07-19T12:02:03.000+02:00','9806758830',
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
                         ['id', 'registratiedatum', 'label',
                          'network_id', 'eisVoorzorgsmaatregel',
                          'netbeheerderNetOmschrijving','netbeheerderWerkAanduiding',
                          'geometrie'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact1.EV1','2001-12-17T09:30:47.00+01:00',
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
                         ['id', 'bronhoudercode', 'registratiedatum',
                          'beheerdersinformatieGeleverd','betrokkenBijAanvraag',
                          'eisVoorzorgsmaatregel','netbeheerderNetOmschrijving',
                          'idGeraaktBelang','idNetbeheerder'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact2._Belanghebbende_18G007160-1',None,
                          '2018-07-19T12:04:10.000+02:00','true',
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
                         ['id','registratiedatum','omschrijving'])

    def test_field_values(self):
        self.assertEqual(self.imkl_obj.field_values(),
                         ['nl.imkl-nbact2._Belang_5012613-300',
                          '2016-08-09T00:00:00.000+02:00',
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
        pass
    def test_contactBeschadiging(self):
        pass

_suite_BelangTestCase = unittest.TestLoader().loadTestsFromTestCase(BelangTestCase)

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
                    _suite_BelangTestCase]

def main():
    imkl_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(imkl_test_suite)
        
if __name__ == "__main__":
    main()        
