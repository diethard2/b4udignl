## to run this test
## Start in terminal Python3 from product folder b4udignl (above folder)
## Start this unit test with
## >>> exec(open('test/test_all.py').read())

import unittest
from test import test_gml
from test import test_basis
from test import test_imkl
from test import test_wv

def main():
    unit_test_suites = test_gml.unit_test_suites
    unit_test_suites.extend(test_basis.unit_test_suites)
    unit_test_suites.extend(test_imkl.unit_test_suites)
    unit_test_suites.extend(test_wv.unit_test_suites)
    full_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(full_test_suite)
        
if __name__ == "__main__":
    main()
