#!/usr/bin/env python
# encoding: utf-8
"""
human_rrule.py

Created by William Bert on 2011-08-12.
Copyright (c) 2011. All rights reserved.
"""

# TODO Add i18n

import sys
import os
import unittest
from datetime import datetime, time

# import dateutil
from dateutil.rrule import YEARLY, MONTHLY, DAILY, HOURLY, MINUTELY, SECONDLY 
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU, weekdays
from dateutil.rrule import weekday
from dateutil.rrule import rrule as rr
from dateutil.relativedelta import relativedelta as rd

from int2word import int2word

from rrule_eq import rrule_eq 

VALID_FREQUENCIES = [YEARLY, MONTHLY, DAILY, HOURLY, MINUTELY, SECONDLY]

INTERVAL_MAP = {
    1: u'each',
    2: u'every other',
    3: u'every third',
    4: u'every fourth',
    5: u'every fifth',
    6: u'every sixth',
    7: u'every seventh',
    8: u'every eighth',
    9: u'every ninth',
    10: u'every tenth',
    11: u'every eleventh',
    12: u'every twelfth',
}

PERIOD_MAP = {
    YEARLY: "year",
    MONTHLY: "month", 
    DAILY: "day", 
    HOURLY: "hour", 
    MINUTELY: "minute", 
    SECONDLY: "second", 
}

WEEKDAY_MAP = {
    u'SU': u"Sunday",
    u'MO': u"Monday",
    u'TU': u"Tuesday",
    u'WE': u"Wednesday",
    u'TH': u"Thursday",
    u'FR': u"Friday",
    u'SA': u"Saturday",
}

INT_ORDINAL_MAP = {
    1: u'first',
    2: u'second',
    3: u'third',
    5: u'fifth',
    8: u'eighth',
    9: u'ninth',
    11: u'eleventh',
    12: u'twelfth',
    20: u'twentieth',
    30: u'thirtieth',
    40: u'fortieth',
    50: u'fiftieth',
    60: u'sixtieth',
    70: u'seventieth',
    80: u'eightieth',
    90: u'ninetieth',    
    -1: u'last'
}

NUM_ORDINAL_MAP = {
    "one": u'first',
    "two": u'second',
    "three": u'third',
    "five": u'fifth',
    "eight": u'eighth',
    "nine": u'ninth',
    "eleven": u'eleventh',
    "twelve": u'twelfth',
    "twenty": u'twentieth',
    "thirty": u'thirtieth',
    "forty": u'fortieth',
    "fifty": u'fiftieth',
    "sixty": u'sixtieth',
    "seventy": u'seventieth',
    "eighty": u'eightieth',
    "ninety": u'ninetieth',    
}

WEEKDAY_LONG_MAP = (
    (7, u'Sunday'),
    (1, u'Monday'),
    (2, u'Tuesday'),
    (3, u'Wednesday'),
    (4, u'Thursday'),
    (5, u'Friday'),
    (6, u'Saturday')
)

DEFAULT_DATE_FORMAT = "%B %d, %Y"
DEFAULT_TIME_FORMAT = "%I:%M %p"

        
class human_rrule(dict):
    """Represents a verbal description of an rrule.
    
    Keys: 
    frequency = YEARLY, MONTHLY (interval, represented by period)
    period = of the year, of the month, etc.
    interval = each, every other, 
    occurrence = eg, first Sunday, third Friday, tenth day, second hour, seventh second, etc.
    begin_time = the start time of each occurrence
    terminal = [ ]
    timezone
    """
    
    def __init__(self, rrule):
        #self["frequency"] 
        super(human_rrule, self).__init__()
        self.__rrule = rrule
        self._refresh_dict()
    
    def get_rrule(self):
        return self.__rrule

    def set_rrule(self, rrule):
        self.__rule = rrule
        self._refresh_dict()

    rrule = property(get_rrule, set_rrule)
    
    def get_description(self, date_format=DEFAULT_DATE_FORMAT, time_format=DEFAULT_TIME_FORMAT):
        """Returns a string consisting of all the values of an human_rrule in 
        an order that reflects an English language description of the rrule."""
        
        desc = []
        # desc.append(self["frequency"])
        desc.append(self["interval"])
        desc.append(self["occurrence"])
        desc.append(self["period"])
        import pdb; pdb.set_trace()
        desc.append("starting at %s" % self.__rrule._timeset.strftime(time_format))
        if self["terminal"].startswith("until"):            
            desc.append(' '.join(["until", self.__rrule._until.strftime(date_format)]))
        else:
            desc.append(self["terminal"])

        if self["timezone"]:
            desc.append("in the %s time zone" % self["timezone"])

        return " ".join(desc)
        
    def __unicode__(self):
        return unicode(self.get_description())

    def _refresh_dict(self):
        # Populate the human_rrule components with values based on the properties of 
        # self.__rrule
        rr = self.__rrule
        dtstart = rr._dtstart # datetime of when each occurrence starts. Defaults to now, down to the second.
        if not rr._freq in VALID_FREQUENCIES:
            raise ValueError, "Invalid frequency in rrule: %s" % rr._freq
        freq = rr._freq # when the recurrence recurs, secondly through yearly. Required.
        interval = rr._interval # how often the recurrence happens, each time through every nth time. Defaults to 1.
        wkst = rr._wkst # Week start day, ie, an int representing which day of the week starts the week, usually Sunday or Monday. Defaults to calendar.firstweekday().
        until = rr._until # datetime until which the recurrence continues. Only it or count is set, not both.
        count = rr._count # Number of times the event happens before it stops. Only it or until is set, not both.
        tzinfo = rr._tzinfo # Time zone information. Defaults to the tzinfo of dtstart.
        bymonth = rr._bymonth # Which month a yearly event recurs in.
        byweekno = rr._byweekno # Which week number a yearly event recurs in.
        byyearday = rr._byyearday # Which day of the year a yearly event recurs in.
        byweekday = rr._byweekday # Which weekday an event recurs in.
        bynweekday = rr._bynweekday # By the nth weekday, e.g., FR(3) is the third Friday of the period
        byeaster = rr._byeaster
        bymonthday = rr._bymonthday # Relative day of the month
        bynmonthday = rr._bynmonthday # Relative day of the month, if negative (counting from the end of the month)
        bysetpos = rr._bysetpos # For sets of seconds/minutes/hours/days/weeks/months/years, specifies which position in the list to pay attention to.
        byhour = rr._byhour
        byminute = rr._byminute
        bysecond = rr._bysecond
        timeset = rr._timeset # The time the occurrence is set to. None if freq >= HOURLY
        # YEARLY needs to have bymonth and bymonthday set
        # MONTHLY needs to have bymonthday set 
        # WEEKLY needs to have byweekday set
        # Or else they will be filled in from dtstart?
        
        # Get the frequency. YEARLY, MONTHLY, etc. 
        # (What I think of as frequency, namely how often this recurrence occurs, e.g.,
        # each time, every other time, every third time, etc., rrule calls interval.)
        # self["frequency"] = FREQUENCY_MAP[freq]
        
        # Initialize the period, which is derived from the frequency. 
        self["period"] = ' '.join(["of the", PERIOD_MAP[freq]])
        self["interval"] = INTERVAL_MAP[interval]
 
        if bynweekday:
            # 
            pass
                
        if freq == YEARLY:
            pass
        elif freq == MONTHLY:            
            # bynweekday is a tuple of (weekday, week_in_period) tuples
            for rule_pair in bynweekday:

                # Get the ordinal. TODO handle multiple ordinals
                ord_text = []
                ord_text.append(human_rrule.int_as_ordinal(rule_pair[1]))

                #  Get the weekday name
                p_weekday = weekday(rule_pair[0])
                name = [WEEKDAY_MAP[unicode(p_weekday)]]
                ord_text.extend(name)
                self["occurrence"] = " ".join(ord_text)                
                
                self["begin_time"] = " ".join(["starting at", str(timeset)])
                                        
        elif freq == WEEKLY:
            # check wkst to see which day of week is first
            pass
            
        elif freq == DAILY:
            pass              
            
        elif freq == HOURLY:
            pass               

        elif freq == MINUTELY:
            pass                

        elif freq == SECONDLY:
            pass               

        else:
            raise human_rruleError, "Frequency value of %s is not valid." % freq
        
        if count:
            self["terminal"] = "%s times" % int2word(count).rstrip()
        elif until:
            self["terminal"] = "until %s" % until.strftime(DEFAULT_DATE_FORMAT)
            
        self["timezone"] = tzinfo and "%s" % tzinfo or None
    
 
    @staticmethod
    def int_as_ordinal(i):
        """Return a string representing an int as an ordinal number."""
        num = int2word(i)
        last_num = num.split()[-1:][0]
        if last_num in NUM_ORDINAL_MAP:
            d = num.split()[0:-1]
            d.append(NUM_ORDINAL_MAP[last_num])
            return " ".join(d)
            
        return ''.join([num, human_rrule._ordinal_ending(i)])
    
    # @staticmethod
    # def num_as_ordinal(num):

    @staticmethod
    def _ordinal_ending(i):

        last_digit = str(i)[-1:]
        if last_digit == '1':
            return "st"
        elif last_digit == '2':
            return "nd"
        elif last_digit == '3':
            return "rd"
        elif last_digit in ['4', '5', '6', '7', '8', '9', '0']:
            return "th"
        else:
            raise ValueError, "%s was not a number." % last_digit
        
    @staticmethod
    def _get_dict_vals(pdict):
        """Recursively includes all and only the values of a dictionary in a string. When it encounters a 
        dictionary, print_dict_vals prints the values of this dictionary, etc including the 
        values of any dictionaries contained within a dictionary.
        
        Returns a list of all the values of the dictionary, including the values of dictionaries
        within the dictionary, recursively."""

        # if pdict is not a dict, return without printing anything
        if not isinstance(pdict, dict):
            return
        list = []
        human_rrule._do_get_dict_vals(pdict, list)
        return list

    @staticmethod
    def _do_get_dict_vals(pdict, list):
        for v in pdict.values():
            if isinstance(v, dict):
                human_rrule._do_get_dict_vals(v, list)
            else:       
                list.append(v)
            
    
class human_rruleTests(unittest.TestCase):
    def setUp(self):
        pass

    def test_int_as_ordinal(self):
        self.assertEqual(human_rrule.int_as_ordinal(1), "first")
        self.assertEqual(human_rrule.int_as_ordinal(11), "eleventh")
        self.assertEqual(human_rrule.int_as_ordinal(30), "thirtieth")
        self.assertEqual(human_rrule.int_as_ordinal(44), "forty fourth")
        self.assertEqual(human_rrule.int_as_ordinal(59), "fifty ninth")
        self.assertEqual(human_rrule.int_as_ordinal(160), "one hundred sixtieth")
        self.assertEqual(human_rrule.int_as_ordinal(200), "two hundredth")
        self.assertEqual(human_rrule.int_as_ordinal(278), "two hundred seventy eighth")    
        
        
    def test_invalid_freq(self):    
        testrr = rrule_eq("a", byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
        self.assertRaises(ValueError, human_rrule, rrule=testrr)
    
        testrr = rrule_eq(None, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
        self.assertRaises(ValueError, human_rrule, rrule=testrr)

    def test_monthly(self):
        correct = u"each third Friday of the month starting at 12:00 AM ten times"
        testrr = rrule_eq(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)
        
        correct = u"every other first Sunday of the month starting at 09:00 PM until August 15, 2012"
        testrr = rrule_eq(MONTHLY, interval=2, byweekday=SU(1), dtstart=datetime(2011, 8, 15, 21, 0, 0), until=datetime(2012, 8, 15))
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)
            
        correct = u"every other first Sunday of the month starting at 09:00 PM until 08/15/2012"
        self.assertEqual(hr.get_description(date_format="%m/%d/%Y"), correct)
        
        correct = u"every other first Sunday of the month starting at 21:00 until August 15, 2012"
        self.assertEqual(hr.get_description(time_format="%H:%M"), correct)
        
    def test_yearly(self):
        correct = u"Each third Friday of the year starting at 12:00 AM ten times"
        testrr = rrule_eq(YEARLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)
        
    def test_get_dict_vals(self):
        d1 = { 
            'a': "I",
            'b': {
                'a': "am",
                'b': "a"
                },
            'c': "recursive",
            'd': {
                "a": "but",
                "b": "simple"
                },
            'e': "function."
        } 

        l = ["I", "am", "a", "recursive", "but", "simple", "function."]
        dict_vals = human_rrule._get_dict_vals(d1)
        for i in dict_vals:
            self.assertIn(i, l)
        for i in l:
            self.assertIn(i, dict_vals)

if __name__ == '__main__':
    unittest.main()