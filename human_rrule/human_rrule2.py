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


FREQUENCY_MAP = (
    (1, u'each'),
    (2, u'every other'),
    (3, u'every third'),
    (4, u'every fourth'),
    (5, u'every fifth'),
    (6, u'every sixth'),
    (7, u'every seventh'),
    (8, u'every eighth'),
    (9, u'every ninth'),
    (10, u'every tenth'),
    (11, u'every eleventh'),
    (12, u'every twelfth'),
)

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
 
class human_rruleError(ValueError):
    pass
        
class human_rrule(dict):
    """Represents a verbal description of an rrule.
    
    Keys: 
    frequency = YEARLY, MONTHLY
    interval
    period
    time
    terminal
    timezone
    """
    
    def __init__(self, rrule):
        #self["frequency"] 
        super(human_rrule, self).__init__()
        self.__rrule = rrule
        self._refresh_dict()
    
    def _refresh_dict(self):
        # Populate the human_rrule components with values based on the properties of 
        # self.__rrule
        rr = self.__rrule
        
        dtstart = rr._dtstart # datetime of when each occurrence starts. Defaults to now, down to the second.
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
        bynmonthday = rr._bynmonthday # Negative relative day of the month
        bysetpos = rr._bysetpos # For sets of seconds/minutes/hours/days/weeks/months/years, specifies which position in the list to pay attention to.
        byhour = rr._byhour
        byminute = rr._byminute
        bysecond = rr._bysecond
        # YEARLY needs to have bymonth and bymonthday set
        # MONTHLY needs to have bymonthday set 
        # WEEKLY needs to have byweekday set
        # Or else they will be filled in from dtstart?
        
        # Get the frequency. "Each", "Every other", "Every third", etc.
        self["frequency"] = FREQUENCY_MAP[freq-1][1]
        
        # Initialize the period. The rest of this will be determined by the frequency.
        self["period"] = ' '.join(["of the", PERIOD_MAP[freq]])
 
        if byyearday:
            self["interval"] = " ".join(["the ", byyearday, "th day of the year"])
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
                self["interval"] = " ".join(name)
                
                
                self["starting at"] = dtstart
                
                self["lasting to"] = dtstart # TODO fix this
                        
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
            self["terminal"] = "%s %s" % (int2word(count).rstrip(), "times")
        elif until:
            self["terminal"] = ["until", until]
            
        self["timezone"] = "%s" % tzinfo
        
    def get_rrule(self):
        return self.__rule
        
    def set_rrule(self, rrule):
        self.__rule = rule
        self._refresh_dict()
        
    rrule = property(get_rrule, set_rrule)
    
    
    def get_description(self, date_format="%B %d, %Y", time_format="%I:%M %p"):
        """Returns a string consisting of all the values of an human_rrule in 
        an order that reflects an English language description of the rrule."""
        
        desc = []
        desc.append(self["frequency"])
        desc.append(self["interval"])
        desc.append(self["period"])
        desc.append("%s" % self["starting at"].strftime(time_format))
        desc.append("%s" % self["lasting to"].strftime(time_format))
        terminal = ""
        if isinstance(self["terminal"], datetime):
            terminal = self["terminal"].strftime(date_format)
        else:
            terminal = self["terminal"]
        desc.append(terminal)
        desc.append("in the %s time zone" % self["timezone"])

        return " ".join(desc)
        
    def __unicode__(self):
        return map(unicode, self.get_description())
 
    @staticmethod
    def int_as_ordinal(i):
        num = int2word(i)
        last_num = num.split()[-1:][0]
        if last_num in NUM_ORDINAL_MAP:
            d = num.split()[0:-1]
            d.append(NUM_ORDINAL_MAP[last_num])
            return " ".join(d)
            
        return ''.join([num, human_rrule.ordinal_ending(i)])
    
    # @staticmethod
    # def num_as_ordinal(num):

    @staticmethod
    def ordinal_ending(i):

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
        self.assertEqual(human_rrule.int_as_ordinal(278), "two hundred seventy eighth")
        
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
        
        
    # def test_invalid_freq(self):
    #     testrr = human_rrule(8, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(human_rruleError, testrr.text)
    # 
    #     testrr = human_rrule("a", byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(human_rruleError, testrr.text)
    # 
    #     testrr = human_rrule(None, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(human_rruleError, testrr.text)
    #     
    #     
    def test_monthly(self):
        # correct = map(unicode, ["each", "third", "Friday", "at", "12:00 AM", "ten times"])
        correct = "each third Friday of the month starting at 12:00 AM lasting to 1:00 AM ten times"
        testrr = rrule_eq(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
        rd = human_rrule(testrr)
        self.assertEqual(rd.get_description(), correct)
        
        # correct = map(unicode, ["every other", "first", "Sunday", "at", "09:00 PM", "until", "August 15, 2012"])
        # testrr = human_rrule(MONTHLY, interval=2, byweekday=SU(1), dtstart=datetime(2011, 8, 15, 21, 0, 0), until=datetime(2012, 8, 15))
        # self.assertListEqual(testrr.text(), correct)
        #     
        # correct = map(unicode, ["every other", "first", "Sunday", "at", "09:00 PM", "until", "08/15/2012"])
        # self.assertListEqual(testrr.text(date_format="%m/%d/%Y"), correct)
        # 
        # correct = map(unicode, ["every other", "first", "Sunday", "at", "21:00", "until", "August 15, 2012"])
        # self.assertListEqual(testrr.text(time_format="%H:%M"), correct)
    #     
    # def test_yearly(self):
    #     correct = map(unicode, ["each", "third", "Friday", "at", "12:00 AM", "ten times"])
    #     correct = "Each third Friday of the year at 12:00 AM ten times"
    #     correct_dict = {
    #                     frequency: "Each",
    #                     interval: "third Friday",
    #                     period: "of the year",
    #                     time: {
    #                         "at 12:00 AM"
    #                         "to 1:00 AM"
    #                     },
    #                     terminal: "ten times"                        
    #     }
    #     testrr = human_rrule(YEARLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
    #     self.assertListEqual(testrr.text(), correct)
        


if __name__ == '__main__':
    unittest.main()