## to run this text please also download, unzip and place contents in
## directory test\data\18G007160_1

import unittest
import test_basis
import test_gml
import test_imkl
import test_wv

def main():
    unit_test_suites = test_gml.unit_test_suites
    unit_test_suites.extend(test_basis.unit_test_suites)
    unit_test_suites.extend(test_imkl.unit_test_suites)
    unit_test_suites.extend(test_wv.unit_test_suites)
    full_test_suite = unittest.TestSuite(unit_test_suites)
    unittest.TextTestRunner(verbosity=2).run(full_test_suite)
        
if __name__ == "__main__":
    main()
