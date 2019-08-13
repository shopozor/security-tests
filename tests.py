# -*- coding: utf-8 -*-
"""
Created on Tue Aug 13 16:34:22 2019

@author: tm
"""

import requests
import sys



import unittest
import argparse

global args
global graphQlEndpoint

class TestGraphQL(unittest.TestCase):
    
    def test_server_header(self):
        res = requests.post(graphQlEndpoint, json={"query": "query { me { id } }"})
        with self.assertRaises(KeyError):
            res.headers["Server"]

    def test_ip_resolver(self):
        res = requests.post(graphQlEndpoint, json={"query": "query { me { id } }"})
        with self.assertRaises(KeyError):
            res.headers["X-Resolver-IP"]

    def test_verbs(self):
        res = requests.get(graphQlEndpoint)
        self.assertEqual(res.status_code, 405)
        res = requests.post(graphQlEndpoint)
        self.assertEqual(res.status_code, 400)
        res = requests.put(graphQlEndpoint)
        self.assertEqual(res.status_code, 405)
        res = requests.patch(graphQlEndpoint)
        self.assertEqual(res.status_code, 405)
        res = requests.delete(graphQlEndpoint)
        self.assertEqual(res.status_code, 405)
        res = requests.head(graphQlEndpoint)
        self.assertEqual(res.status_code, 405)

        # TODO find out how to test the other verbs
        
        #res = requests.copy(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.link(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.unlink(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.purge(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.trace(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.lock(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.unlock(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.propfind(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        #res = requests.view(graphQlEndpoint)
        #self.assertEqual(res.status_code, 405)
        
class TestBackend(unittest.TestCase):
    
    def test_http_codes(self):
        res = requests.get(args.domain+"/blabla")
        print("HTTPCodes, status=", res.status_code)
        self.assertEqual(res.status_code, 404)
        
        
if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('domain')
    parser.add_argument('unittest_args', nargs='*')
    args = parser.parse_args()
    
    graphQlEndpoint = args.domain + "/graphql/"


    # Now set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args    
    
    print("Running test against: ", args.domain)
    print("graphql endpoint is: ", graphQlEndpoint)

    unittest.main()
