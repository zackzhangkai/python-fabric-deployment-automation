import unittest
import mock
from mock import MagicMock, patch
import inspect, os, sys


utils_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))), '../utils'))
sys.path.append(utils_path)

import managerutils


class testmanagerutils(unittest.TestCase):

        ### called each time before a test method run
        # def setUp(self):
        #        return

        ### called each time before a test method have run
        # def tearDown():
        #        return

        ### called before tests in an individual class run
        # @classmethod
        # def setUpClass():
        #         return

        ### called after tests in an individual class have run
        # @classmethod
        # def tearDownClass():
        #        return

	def test_verify_if_started_deployed(self):
                with mock.patch('managerutils.verifyserverstartup') as MockClass1:       
						MockClass1.return_value = True			
						with mock.patch('managerutils.verifydeployment') as MockClass3:
								MockClass3.return_value = True
								output=managerutils.verify('Test Case')
								self.assertEqual(output, True, 'Started and Deployed')
                return


	def test_verify_if_not_started(self):
		try:
                	with mock.patch('managerutils.verifyserverstartup') as MockClass1:
                        	MockClass1.return_value = False
                                output=managerutils.verify('Test Case')
                                self.assertFail()
		except Exception as inst:		
			self.assertEqual(inst.message, 'Server not starting!', 'Not Started')
                return

	def test_verify_if_started_not_deployed(self):
                with mock.patch('managerutils.verifyserverstartup') as MockClass1:
                        MockClass1.return_value = True                        
						with mock.patch('managerutils.verifydeployment') as MockClass3:
								MockClass3.return_value = False
								output=managerutils.verify('Test Case')
								self.assertEqual(output, False, 'Started and Not Deployed')
                return


suite = unittest.TestLoader().loadTestsFromTestCase(testmanagerutils)
unittest.TextTestRunner(verbosity=2).run(suite)

