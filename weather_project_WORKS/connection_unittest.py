import unittest
import app

class TestingReachability(unittest.TestCase):
    app.app.testing = True
    application = app.app.test_client()

    def SetUp(self):
        app.app.testing = True
        self.application = app.app.test_client()

    def test_reachability_with_client(self):
	#taking http response after get request
        result = self.application.get('/')
	#taking number out of result response class
        self.assertEqual(result.status_code, 200)


#To start test: python3 unittest -m testing_reachability.py



