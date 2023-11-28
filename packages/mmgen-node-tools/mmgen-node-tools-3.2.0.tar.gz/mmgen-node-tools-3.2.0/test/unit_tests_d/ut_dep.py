#!/usr/bin/env python3

"""
test.unit_tests_d.ut_dep: dependency unit tests for the MMGen Node Tools

  Test whether dependencies are installed and functional.
  No data verification is performed.
"""

from ..include.common import vmsg

class unit_tests:

	def yahooquery(self,name,ut):
		try:
			from yahooquery import Ticker
			t = Ticker('abc',formatted=True,timeout=1,retry=0,proxies=['http://foo:8118'])
			vmsg(repr(t))
			return True
		except:
			imsg('Unable to initialize Ticker from yahooquery')
			return False
