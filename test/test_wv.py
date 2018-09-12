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
from wv import Doc, Company

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
        layer_names = [layer.layerName() for layer in self.doc.layers]
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

_suite_wv_doc_2_1 = unittest.TestLoader().loadTestsFromTestCase(DocTestCaseV2_1)


unit_test_suites = [_suite_wv_doc_1_5, _suite_wv_doc_2_1]

def main():
    wv_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(wv_test_suite)
        
if __name__ == "__main__":
    main()
