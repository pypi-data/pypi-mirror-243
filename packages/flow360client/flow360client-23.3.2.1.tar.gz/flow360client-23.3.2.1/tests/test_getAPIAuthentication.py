import hashlib, sys, os
from unittest import TestCase

testDir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(testDir))
import flow360client
assert(os.path.dirname(flow360client.__file__) == os.path.abspath(os.path.join(testDir,'..','flow360client')))
from flow360client.authentication import authentication_api

class TestGetAPIAuthentication(TestCase):
    def test_getAPIAuthentication(self):
        email = 'zhenglei2010fall@gmail.com'
        password = 'Monday@2012'
        salt = '5ac0e45f46654d70bda109477f10c299'
        password = hashlib.sha512(password.encode('utf-8') + salt.encode('utf-8')).hexdigest()
        authentication_api(email, password)
