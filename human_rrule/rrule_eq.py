#!/usr/bin/env python
# encoding: utf-8
"""
rrule_eq.py

Created by William Bert on 2011-08-22.
Copyright (c) 2011 __MyCompanyName__. All rights reserved.
"""

import sys
import os
import unittest

from datetime import datetime, time

from dateutil.rrule import rrule as rr
from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY 
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU, weekdays
from dateutil.rrule import weekday


class rrule_eq(rr): 
    """Wrapper class around an rrule that provides __eq__ and __ne__ methods."""
    
    # This is for debugging only
    def __init__(self, freq, dtstart=None,
                 interval=1, wkst=None, count=None, until=None, bysetpos=None,
                 bymonth=None, bymonthday=None, byyearday=None, byeaster=None,
                 byweekno=None, byweekday=None,
                 byhour=None, byminute=None, bysecond=None,
                 cache=False):
        rr.__init__(self, freq, dtstart=dtstart,
                 interval=interval, wkst=wkst, count=count, until=until, bysetpos=bysetpos,
                 bymonth=bymonth, bymonthday=bymonthday, byyearday=byyearday, byeaster=byeaster,
                 byweekno=byweekno, byweekday=byweekday,
                 byhour=byhour, byminute=byminute, bysecond=bysecond,
                 cache=cache) # rrule is an old-style class
        self._pprint()
        
    def __eq__(self, other):
        """Compare two human_rrule instances."""
        
        attrs = [
         '_byeaster',
         '_byhour',
         '_byminute',
         '_bymonth',
         '_bymonthday',
         '_bynmonthday',
         '_bynweekday',
         '_bysecond',
         '_bysetpos',
         '_byweekday',
         '_byweekno',
         '_byyearday',
         '_count',
         '_dtstart',
         '_freq',
         '_interval',
         '_timeset',
         '_tzinfo',
         '_until',
         '_wkst',
        ]
         
        for p in attrs:
            if getattr(self, p) != getattr(other, p):
                return False
            
        return True
        
    def __ne__(self, other):
        return not (self == other)

    def _pprint(self):
        """Temp method"""
        attrs = [
         '_byeaster',
         '_byhour',
         '_byminute',
         '_bymonth',
         '_bymonthday',
         '_bynmonthday',
         '_bynweekday',
         '_bysecond',
         '_bysetpos',
         '_byweekday',
         '_byweekno',
         '_byyearday',
         '_count',
         '_dtstart',
         '_freq',
         '_interval',
         '_timeset',
         '_tzinfo',
         '_until',
         '_wkst',
        ]
         
        for p in attrs:
            print "%s\t\t%s" % (p, getattr(self, p))

class rrule_eqTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_equals(self):
        r1 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15))
        self.assertTrue(r1==r2)

        r1 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        self.assertTrue(r1==r2)

    def test_not_equals(self):
        r1 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule_eq(MONTHLY, dtstart=datetime(2012, 8, 15))
        self.assertFalse(r1==r2)

        r2 = rrule_eq(DAILY, dtstart=datetime(2011, 8, 15))
        self.assertFalse(r1==r2)

        r1 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule_eq(DAILY, dtstart=datetime(2012, 8, 15), byweekday=TU)
        self.assertFalse(r1==r2)
        
if __name__ == '__main__':
	unittest.main()