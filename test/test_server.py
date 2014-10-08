# -*- coding: utf-8 -*-
import time

from application import application as serv
from conf.constants import URI_PARTS as URI
from conf.constants import DATEFMT

from test.apistub import application as apistub

__author__ = 'Yorick Chollet'

import unittest  # Python unit test structure

from webtest import TestApp  # WSGI application tester

server = TestApp(serv)
api = TestApp(apistub)


class TestServerSequence(unittest.TestCase):

    def test_server_up(self):
        response = server.get('/test/', status=200)
        assert len(response.normal_body) > 1

    def test_server_tgroot_status(self):
        response = server.get('/%s/' % URI['G'], status=400)

    def test_server_tmroot_status(self):
        response = server.get('/%s/' % URI['T'], status=400)

    def test_dateOK(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/%s/uri' % URI['G'], headers=ad, status=200)

    def test_dateWRONG(self):
        timestr = time.strftime("å/ンページ/ %s /הצלת", time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/%s/uri' % URI['G'], headers=ad, status=400)

    def test_urlOK(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/%s/http://www.example.com/resource/' % URI['G'], headers=ad, status=200)

    def test_urlTRUNKATED(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/%s/example.com/resource' % URI['G'], headers=ad, status=200)

    def test_urlINEXISTANT(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/%s/http://www.wrong.url/' % URI['G'], headers=ad, status=200)

    def test_urlUNSAFE(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        url = """/timegate/http://www.wrong.url/å/ンページ/  /הצלת/é/"""
        response = server.get(url, headers=ad, status=200)

    def test_urlNOSLASHR(self):
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        url = """/timegatewww.wrong.url"""
        response = server.get(url, headers=ad, status=404)

class TestServerHandlerSeq(unittest.TestCase):

    def test_stub_up(self):
        response = api.get('/test/', status=404)
        assert len(response.normal_body) > 1

    def test_flow(self):
        api = TestApp(apistub)
        timestr = time.strftime(DATEFMT, time.gmtime())
        ad = {'Accept-Datetime': timestr}
        response = server.get('/timegate/example.com/', headers=ad, status=200)


def suite():
    st = unittest.TestSuite()
    # st.addTest(unittest.makeSuite(TestServerSequence))
    st.addTest(unittest.makeSuite(TestServerHandlerSeq))
    return st
