"""
/***************************************************************************
 Unit test suite to test wv objects
 -------------------
 begin                : 01-09-2018
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
from core.wv import Doc
from core import imkl

class DocTestCaseV1_5(unittest.TestCase):
    """
    unittests to test wv.Doc object, holds full klic message provided in IMKL
    version 1.5 (valid till 1-1-2019).
    """
    def setUp(self):
        """
        For each test create a woonplaats read from xml file woonplaats.xml
        """
        # read the file
        klic_msg_dir = "../testMsg/14G166926_1"
        self.doc = Doc(klic_msg_dir)
        self.maxDiff = None

    def test_version(self):
        self.assertEqual(self.doc.version, '1.5')

    def test_klicnummer(self):
        self.assertEqual(self.doc.klicnummer, '14G166926')
        
    def test_meldingsoort(self):
        self.assertEqual(self.doc.meldingsoort, 'Graafmelding')
                             
    def test_netOwner_names(self):
        netowner_names = [netowner.name for netowner in self.doc.netOwners]
        self.assertEqual(netowner_names,
                         ['Liander', 'APELDOORN','Eurofiber', 'KPN',
                          'Reggefiber', 'Tele2', 'trent', 'upc', 'Vitens'])

    def test_pixel_width_heigth(self):
        rectangle = self.doc.rectangle
        self.assertEqual((rectangle.pixelsWidth,rectangle.pixelsHeight),
                         (1624,910))

    def test_rectange(self):
        rectangle = self.doc.rectangle
        self.assertEqual(repr(rectangle),
                         'Rectangle(Coord(194154.00, 465849.00), Coord(194270.00, 465914.00))')

    def test_themes(self):
        netowner = self.doc.netOwners[0]
        theme_names = []
        for theme in netowner.themes:
            theme_names.append(theme.name)
        self.assertEqual(theme_names,['middenspanning', 'gas lage druk', 'laagspanning'])

    def test_toezichthouders(self):
        personal_info = []
        netowners = self.doc.netOwners
        for netowner in netowners:
            for theme in netowner.themes:
                for supervisor in theme.supervisors:
                    theme = theme.name
                    name = supervisor.name
                    telephone = supervisor.telephone
                    email = supervisor.email
                    fax = supervisor.fax
                    personal_info.append((theme,name,telephone,email,fax))
        self.assertEqual(personal_info,
                         [('middenspanning', None, '0881912211', None, None),
                          ('gas lage druk', None, '0881912211', None, None),
                          ('laagspanning', None, '0881912211', None, None),
                          ('riool vrijverval', 'Rick Verhoof', '14055', 'r.verhoof@apeldoorn.nl', None),
                          ('datatransport', 'KPN KLIC-loket', '030-25 53334',
                           'orderintakeplan@kpn.com', None),
                          ('datatransport', 'monique van baaren', '0318531556',
                           'klic.algemeen@koningenhartman.com', None)])
                    
    def test_thema_layers(self):
        netowner = self.doc.netOwners[0]
        theme_layer_files = []
        file_names = ['AN_middenspanning_Liander_0000574962_14G166926.png',
                      'MV_middenspanning_Liander_0000574962_14G166926.png',
                      'LG_middenspanning_Liander_0000574962_14G166926.png']
        klic_dir = self.doc.path
        file_names = [os.path.join(klic_dir,file_name) for file_name in file_names]
        theme = netowner.themes[0]
        theme_layer_files = [layer.layerFile for layer in theme.layers]
        self.assertEqual(file_names,theme_layer_files)
                    
    def test_thema_docs(self):
        netowner = self.doc.netOwners[0]
        doc_names = []
        for theme in netowner.themes:
            docs = theme.pdf_docs
            doc_names.extend([doc.name for doc in docs])
        self.assertEqual(doc_names,
                         ['HA_laagspanning_Liander_0000574962_14G166926_7334DP_701.pdf'])

    def test_layer_names(self):
        layers = [layer for layer in self.doc.layers.values()]
        layers.sort()
        layer_names = [layer.layerName for layer in layers]
        self.assertEqual(layer_names,
                         ['GB_14G166926.png',
                          'ET_KPN_0000546663_14G166926.png',
                          'ET_Liander_0000574962_14G166926.png',
                          'PT_KPN_0000546663_14G166926.png',
                          'LG_datatransport_KPN_0000546663_14G166926.png',
                          'LG_datatransport_trent_0000585212_14G166926.png',
                          'LG_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'LG_laagspanning_Liander_0000574962_14G166926.png',
                          'LG_middenspanning_Liander_0000574962_14G166926.png',
                          'LG_riool+vrijverval_APELDOORN_0000586326_14G166926.png',
                          'LG_water_Vitens_0000552354_14G166926.png',
                          'MV_datatransport_KPN_0000546663_14G166926.png',
                          'MV_datatransport_trent_0000585212_14G166926.png',
                          'MV_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'MV_laagspanning_Liander_0000574962_14G166926.png',
                          'MV_middenspanning_Liander_0000574962_14G166926.png',
                          'AN_datatransport_KPN_0000546663_14G166926.png',
                          'AN_datatransport_trent_0000585212_14G166926.png',
                          'AN_gas+lage+druk_Liander_0000574962_14G166926.png',
                          'AN_laagspanning_Liander_0000574962_14G166926.png',
                          'AN_middenspanning_Liander_0000574962_14G166926.png',
                          'AN_water_Vitens_0000552354_14G166926.png'])
        
    
_suite_wv_doc_1_5 = unittest.TestLoader().loadTestsFromTestCase(DocTestCaseV1_5)

class DocTestCaseV2_1(unittest.TestCase):
    """
    unittests to test wv.Doc object, holds full klic message provided in IMKL
    version 1.5 (valid till 1-1-2019).
    """
    def setUp(self):
        """
        For each test create a woonplaats read from xml file woonplaats.xml
        """
        # read the file
        klic_msg_dir = "../test/data/18G007160_1"
        self.doc = Doc(klic_msg_dir)
        self.maxDiff = None

    def test_version(self):
        self.assertEqual(self.doc.version, '2.1')

    def test_imkl_elements(self):
        self.assertEqual(sorted(self.doc.imkls.keys()),
                         ['AanduidingEisVoorzorgsmaatregel','Annotatie',
                          'Appurtenance','Beheerder','Belang','Belanghebbende',
                          'Bijlage','BoundedBy','DiepteNAP','DiepteTovMaaiveld','Duct',
                          'EigenTopografie','EisVoorzorgsmaatregelBijlage',
                          'Elektriciteitskabel','ExtraDetailinfo',
                          'ExtraGeometrie','GebiedsinformatieAanvraag',
                          'GebiedsinformatieLevering','Graafpolygoon',
                          'Kabelbed','Kast','Leveringsinformatie','Maatvoering',
                          'Mangat','Mantelbuis','Mast',
                          'OlieGasChemicalienPijpleiding','Overig',
                          'Rioolleiding','TechnischGebouw',
                          'Telecommunicatiekabel','ThermischePijpleiding',
                          'Toren','Utiliteitsnet','UtilityLink','Waterleiding'])
        
    def test_imkl_count_elements(self):
        key_count = []
        for key in sorted(self.doc.imkls.keys()):
            objects = self.doc.imkls[key]
            key_count.append((key,len(objects)))
        self.assertEqual(key_count,
                         [('AanduidingEisVoorzorgsmaatregel', 1),
                          ('Annotatie', 5),('Appurtenance', 31),
                          ('Beheerder', 6),('Belang', 8),('Belanghebbende', 6),
                          ('Bijlage', 3),('BoundedBy', 1),('DiepteNAP', 1),
                          ('DiepteTovMaaiveld', 1),('Duct', 1),
                          ('EigenTopografie', 5),
                          ('EisVoorzorgsmaatregelBijlage', 1),
                          ('Elektriciteitskabel', 1),('ExtraDetailinfo', 3),
                          ('ExtraGeometrie', 15),
                          ('GebiedsinformatieAanvraag', 1),
                          ('GebiedsinformatieLevering', 1),('Graafpolygoon', 1),
                          ('Kabelbed', 1),('Kast', 1),
                          ('Leveringsinformatie', 1),('Maatvoering', 5),
                          ('Mangat', 1),('Mantelbuis', 1),('Mast', 1),
                          ('OlieGasChemicalienPijpleiding', 1),('Overig', 1),
                          ('Rioolleiding', 1),('TechnischGebouw', 1),
                          ('Telecommunicatiekabel', 15),
                          ('ThermischePijpleiding', 1),('Toren', 1),
                          ('Utiliteitsnet', 77),('UtilityLink', 25),
                          ('Waterleiding', 2)])
        
    def test_all_imkl_pipes_have_geometry(self):
        all_ok = True
        for tag in imkl.tags_pipes_and_cables():
            imkl_set = self.doc.imkls[tag]
            for imkl_object in imkl_set:
                if imkl_object.field("geometry").value is None:
                    all_ok = False
                    print(imkl_object.name)
                    break        
        self.assertEqual(all_ok, True)

    def test_geometry_rioolleiding(self):
        leiding = self.doc.imkls[imkl.RIOOLLEIDING][0]
        link_id = leiding.field("link_id").value
        geom = leiding.field("geometry").value
        self.assertEqual((link_id,geom),
                         ('nl.imkl-nbact1.ul00006',
                          'LineString(155058.000 388020.000, 155042.000 388020.000)'))

    def test_thema_kast(self):
        kast = self.doc.imkls[imkl.KAST][0]
        network_id = kast.field("network_id").value
        thema = kast.field("thema").value
        self.assertEqual((network_id,thema),
                         ('nl.imkl-nbact1.un00048', 'datatransport'))

    def test_klicnummer(self):
        self.assertEqual(self.doc.klicnummer, '18G007160')
        
    def test_meldingsoort(self):
        self.assertEqual(self.doc.meldingsoort, 'graafmelding')
                             
    def test_pixel_width_heigth(self):
        rectangle = self.doc.rectangle
        self.assertEqual((rectangle.pixelsWidth,rectangle.pixelsHeight),
                         (1960,2240))

    def test_rectangle(self):
        rectangle = self.doc.rectangle
        self.assertEqual(repr(rectangle),
                         'Rectangle(Coord(154980.00, 387980.00), Coord(155120.00, 388140.00))')

    def test_graafpolygoon(self):
        self.assertEqual(self.doc.graafpolygoon,
                         'Polygon((154980.0 387980.0, 155120.0 387980.0, \
155120.0 388140.0, 154980.0 388140.0, 154980.0 387980.0))')

    def test_netOwner_names(self):
        netowner_names = [(netowner.bronhoudercode, netowner.name) \
                          for netowner in self.doc.netOwners]
        self.assertEqual(netowner_names,
                         [('nbact2','Netbeheerder Actualiseren02'),
                          ('nbact3','Netbeheerder Actualiseren03'),
                          ('nbact4','Netbeheerder Actualiseren04'),
                          ('nbact1','Afd. KLIC Beheer nbact1'),
                          ('KL1031','Enexis 01'),('KN1100','PWN4')])

    def test_netOwner_contact_persons(self):
        contact_list = []
        for netowner in self.doc.netOwners:
            contact = netowner.contactPerson
            name = contact.name
            tel = contact.telephone
            email = contact.email
            contact_list.append((name, tel, email))
        self.assertEqual(contact_list,
                         [('BMK Netbeheerder Actualiseren02','0887891325',
                           'klic_levering@integratie.kadaster.nl'),
                          ('BMK Netbeheerder Actualiseren03','0884891567',
                           'klic_levering@integratie.kadaster.nl'),
                          ('BMK Netbeheerder Actualiseren04','0887895461',
                           'klic_levering@integratie.kadaster.nl'),
                          ('BMK Netbeheerder Actualiseren01', '0885468791',
                           'klic.testers@kadaster.nl'),
                          ('Bmk Enexis 01', '0503091234',
                           'klic.testers@kadaster.nl'),
                          ('Bmk Pwn4', '0881234567', 'klic.testers@kadaster.nl')])

    def test_netOwner_telephone_numbers(self):
        telephone_nrs = [(netowner.telNrDamage, netowner.telNrProblemIT) \
                         for netowner in self.doc.netOwners]
        self.assertEqual(telephone_nrs,
                         [('1234567890', '1234567890'),
                          ('1234567890', '1234567890'),
                          ('1234567890', '1234567890'),
                          ('1234567890', '1234567890'),
                          ('1234567890', '1234567890'),
                          ('1234567890', '1234567890')])

    def test_netOwner_on_code(self):
        netOwners_dict = self.doc.storage.netOwners_on_code
        netOwner = netOwners_dict['nbact1']
        self.assertEqual(netOwner.name,'Afd. KLIC Beheer nbact1')
        
        
    def test_themes(self):
        netowners = self.doc.netOwners
        netowner = None
        for a_netowner in netowners:
            if a_netowner.bronhoudercode == 'KN1100':
                netowner = a_netowner
                break
        theme_names = []
        for theme in netowner.themes:
            theme_names.append(theme.name)
        self.assertEqual((netowner.bronhoudercode,theme_names),
                         ('KN1100',['water']))

    def test_riool_layer(self):
        layers = self.doc.layers
        riool_layer = layers['Rioolleiding']
        field_names = [field.name() for field in riool_layer.fields]
        attributes = [feature.attributes() for feature in riool_layer.features]
        self.assertEqual((riool_layer.layerName, field_names, attributes),
                         ('Rioolleiding',
                          [u'id',u'registratiedatum',u'network_id',
                           u'link_id', u'status', u'validFrom', u'validTo',
                           u'verticalPosition', u'thema', u'geom_id', u'label',
                           u'warningType', u'diameter', u'druk', u'fluid'],
                          [[u'nl.imkl-nbact1.rl00001',
                            u'2001-12-17T09:30:47.0Z',u'nl.imkl-nbact1.un00058',
                            u'nl.imkl-nbact1.ul00006', u'projected',
                            u'2001-12-17T09:30:47.0Z',u'2031-12-17T09:30:47.0Z',
                            u'underground',u'laagspanning',
                            u'nl.imkl-nbact1.xg00010',u'',u'net',u'0',u'0',
                            u'storm']]))

_suite_wv_doc_2_1 = unittest.TestLoader().loadTestsFromTestCase(DocTestCaseV2_1)


unit_test_suites = [_suite_wv_doc_1_5, _suite_wv_doc_2_1]

def main():
    wv_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(wv_test_suite)
        
if __name__ == "__main__":
    main()
