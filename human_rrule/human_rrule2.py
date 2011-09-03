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
from dateutil.rrule import YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY 
from dateutil.rrule import MO, TU, WE, TH, FR, SA, SU, weekdays
from dateutil.rrule import weekday
from dateutil.rrule import rrule as rr
from dateutil.relativedelta import relativedelta as rd

from int2word import int2word

from rrule_eq import rrule_eq 

VALID_FREQUENCIES = [YEARLY, MONTHLY, WEEKLY, DAILY, HOURLY, MINUTELY, SECONDLY]

INTERVAL_MAP = (
    u'',
    u'each',
    u'every other',
    u'every third',
    u'every fourth',
    u'every fifth',
    u'every sixth',
    u'every seventh',
    u'every eighth',
    u'every ninth',
    u'every tenth',
    u'every eleventh',
    u'every twelfth',
)

PERIOD_MAP = {
    YEARLY: "year",
    MONTHLY: "month", 
    WEEKLY: "week",
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

MONTH_MAP = (
    "",
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December"
)

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
DEFAULT_DATETIME_FORMAT = " ".join([DEFAULT_TIME_FORMAT, DEFAULT_DATE_FORMAT])

        
class human_rrule(dict):
    """Represents a verbal description of an rrule.
    
    Keys: 
    frequency = YEARLY, MONTHLY (interval, represented by period)
    occurrence = 
    period = of the year, of the month, etc. Don't need for HOURLY, MINUTELY, or WEEKLY.
    interval = each, every other, 
    occurrence = eg, first Sunday, third Friday, tenth day, second hour, seventh second, etc.
    begin_time = the start time of each occurrence
    terminal = [ ]
    timezone
    """
    
    def __init__(self, rrule):
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
        """Convenience method for returning a string consisting of all the values of an human_rrule in 
        an order that reflects an English language description of the rrule."""
        
        datetime_format = " ".join([time_format, date_format])
        desc = []
        # desc.append(self["frequency"])
        desc.append(self["interval"])
        desc.append(self["occurrence"])
        desc.append(self["period"])
        desc.append("starting at %s" % self._get_starttime().strftime(datetime_format)) 
        if self["terminal"].startswith("until"):            
            untiltime = self._get_untiltime()
            desc.append(' '.join(["until", untiltime.strftime(datetime_format) if untiltime else ""]))
        else:
            desc.append(self["terminal"])

        if self["timezone"]:
            desc.append("in the %s time zone" % self["timezone"])

        return " ".join(desc).replace("  ", " ")
        
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
        wkst = rr._wkst # Integer representing week start day, ie, an int representing which day of the week starts the week, usually 0 for Sunday or 1 for Monday. Defaults to calendar.firstweekday().
        until = rr._until # datetime until which the recurrence continues. Only it or count is set, not both.
        count = rr._count # Number of times the event happens before it stops. Only it or until is set, not both.
        tzinfo = rr._tzinfo # Time zone information. Defaults to the tzinfo of dtstart.
        bymonth = rr._bymonth # Tuple. Which month a yearly event recurs in.
        byweekno = rr._byweekno # Tuple. Which week number a yearly event recurs in.
        byyearday = rr._byyearday # Tuple. Which day of the year a yearly event recurs in.
        byweekday = rr._byweekday # Tuple. Which weekday an event recurs in.
        bynweekday = rr._bynweekday # Tuple. By the nth weekday, e.g., FR(3) is the third Friday of the period. Only used if freq is < MONTHLY
        byeaster = rr._byeaster # Tuple.
        bymonthday = rr._bymonthday # Tuple. Relative day of the month
        bynmonthday = rr._bynmonthday # Tuple. Relative day of the month, if negative (counting from the end of the month)
        bysetpos = rr._bysetpos # Tuple. For sets of seconds/minutes/hours/days/weeks/months/years, specifies which position in the list to pay attention to.
        byhour = rr._byhour # Tuple. The hour of the occurrence.
        byminute = rr._byminute # Tuple. The minutes of the occurrence.
        bysecond = rr._bysecond # Tuple. The second of the occurrence.
        timeset = rr._timeset # If freq < HOURLY and all three of hour, minute, and second are set, timeset is a tuple of datetime.times representing when the occurrence occurs. None if otherwise.
        # YEARLY needs to have bymonth and bymonthday set
        # MONTHLY needs to have bymonthday set 
        # WEEKLY needs to have byweekday set
        # Or else they will be filled in from dtstart?
        
        # Get the frequency. YEARLY, MONTHLY, etc. 
        # (What I think of as frequency, namely how often this recurrence occurs, e.g.,
        # each time, every other time, every third time, etc., rrule calls interval.)
        # self["frequency"] = FREQUENCY_MAP[freq]
        
        # Initialize the period, which is derived from the frequency. 
        if freq in [HOURLY, MINUTELY, SECONDLY]:
            self["period"] = "" # Expresing periods doesn't make sense for these frequencies (e.g., 
        else:
            self["period"] = ' '.join(["of the", PERIOD_MAP[freq]])
        self["interval"] = INTERVAL_MAP[interval]       
 
                
        if freq == YEARLY:
            self["occurrence"] = self._build_occurrence()

            
        elif freq == MONTHLY:        
            self["occurrence"] = self._build_occurrence()    
            # # bynweekday is a tuple of (weekday, week_in_period) tuples
            # for rule_pair in bynweekday:
            # 
            #     # Get the ordinal. TODO handle multiple ordinals
            #     ord_text = []
            #     ord_text.append(human_rrule.int_as_ordinal(rule_pair[1]))
            # 
            #     #  Get the weekday name
            #     p_weekday = weekday(rule_pair[0])
            #     name = [WEEKDAY_MAP[unicode(p_weekday)]]
            #     ord_text.extend(name)
            #     self["occurrence"] = " ".join(ord_text)                
                                        
        elif freq == WEEKLY:
            self["occurrence"] = self._build_occurrence()
            # check wkst to see which day of week is first
            
            
        elif freq == DAILY:
            self["occurrence"] = "day"
                          
            
        elif freq == HOURLY:
            self["occurrence"] = "hour"

        elif freq == MINUTELY:
            self["occurrence"] = "minute"

        elif freq == SECONDLY:
            self["occurrence"] = "second"
            if bymonthday:                  
                s = "".join(["of the ", human_rrule.int_as_ordinal(bymonthday[0]), " day of the month"]) # TODO work with multiple bymonthdays
                self["occurrence"] = " ".join([self["occurrence"], s])


        else:
            raise human_rruleError, "Frequency value of %s is not valid." % freq
            
        self["begin_time"] = " ".join(["starting at", self._get_starttime().strftime(DEFAULT_DATETIME_FORMAT)])
        
        if count:
            self["terminal"] = "%s times" % int2word(count).rstrip()
        elif until:
            untiltime = self._get_untiltime()
            self["terminal"] = "until %s" % untiltime.strftime(DEFAULT_DATETIME_FORMAT) if untiltime else ""
            
        self["timezone"] = tzinfo and "%s" % tzinfo or None
   
    def _build_occurrence(self):
        """
        Figure out which occurrence values are set and add them to the occurrence.
        Returns a string.
        """
        rr = self.__rrule
        bymonth = rr._bymonth # Tuple. Which month a yearly event recurs in.
        byweekno = rr._byweekno # Tuple. Which week number a yearly event recurs in.
        byyearday = rr._byyearday # Tuple. Which day of the year a yearly event recurs in.
        byweekday = rr._byweekday # Tuple. Which weekday an event recurs in.
        bynweekday = rr._bynweekday # Tuple. By the nth weekday, e.g., FR(3) is the third Friday of the period. Only used if freq is < MONTHLY
        byeaster = rr._byeaster # Tuple.
        bymonthday = rr._bymonthday # Tuple. Relative day of the month
        bynmonthday = rr._bynmonthday # Tuple. Relative day of the month, if negative (counting from the end of the month)
        bysetpos = rr._bysetpos # Tuple. For sets of seconds/minutes/hours/days/weeks/months/years, specifies which position in the list to pay attention to.
        byhour = rr._byhour # Tuple. The hour of the occurrence.
        byminute = rr._byminute # Tuple. The minutes of the occurrence.
        bysecond = rr._bysecond # Tuple. The second of the occurrence.
        
        o = ""
        if bymonth:
            for month in bymonth:
                o = " ".join([o, MONTH_MAP[month]])
                for i, monthday in enumerate(bymonthday):
                    o = "".join([", " if i>0 else "", o, " ", str(monthday)])                  
                    
        if bymonthday:
            if not bymonth:
                s = ""
                for i, monthday in enumerate(bymonthday):
                    s = "".join([" and " if i>0 else "", "the %s day of the month", human_rrule.int_as_ordinal(bymonthday[0])])
                o = "".join([o, s]) # 
        if bynmonthday:
            s = ""
            for i, nmonthday in enumerate(bynmonthday):                    
                s = "".join([" and " if i>0 else "", "the %s to last day of the month" % human_rrule.int_as_ordinal(bynmonthday)])
                o = "".join([o, s]) # 
        if byweekday:
            s = ""
            for i, p_weekday in enumerate(byweekday):
                s = "".join([", " if i>0 else "", WEEKDAY_MAP[unicode(weekday(p_weekday))]])
                o = "".join([o, s])
        if byweekno:
            o = " ".join([o, "the %s week" % human_rrule.int_as_ordinal(byweekno)])
        if byyearday:
            o = " ".join([o, "the %s year" % human_rrule.int_as_ordinal(byyearday)])
        if bynweekday:
            for rule_pair in bynweekday:

                # Get the ordinal. TODO handle multiple ordinals
                ord_text = []
                ord_text.append(human_rrule.int_as_ordinal(rule_pair[1]))

                #  Get the weekday name
                p_weekday = weekday(rule_pair[0])
                name = [WEEKDAY_MAP[unicode(p_weekday)]]
                ord_text.extend(name)
                o = " ".join([o, ord_text[0], ord_text[1]])
        
        return o
        
 
    def _get_starttime(self):
        """Get the actual starttime of the recurrence. dtstart is used as a boundary, but depending on the rules, it may or may not be the actual datetime when the first instance of the recurrence occurs."""
        for d in self.__rrule:
            return d

    def _get_untiltime(self):
        """Get the actual untiltime of the recurrence. until is used as a boundary, but depending on the rules, it may or may not be the actual datetime when the last instance of the recurrence occurs."""        
        last = None
        for d in self.__rrule:
            last = d             
        return last
                
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
        
    def test_secondly(self):
        correct = u"each second starting at 00:00:00 AM August 15, 2011 ten times"
        testrr = rrule_eq(SECONDLY, dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(time_format="%H:%M:%S %p"), correct)
        
        correct = "each second of the twenty first day of the month starting at 00:00:00 AM August 21, 2011 ten times"
        testrr = rrule_eq(SECONDLY, dtstart=datetime(2011, 8, 15), count=10, bymonthday=21)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(time_format="%H:%M:%S %p"), correct)
        
    def test_minutely(self):
        correct = u"each minute starting at 00:00:00 AM August 15, 2011 ten times"
        testrr = rrule_eq(MINUTELY, dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(time_format="%H:%M:%S %p"), correct)
        
    def test_hourly(self):
        correct = u"each hour starting at 00:00:00 AM August 15, 2011 ten times"
        testrr = rrule_eq(HOURLY, dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(time_format="%H:%M:%S %p"), correct)        
        
    def test_daily(self):
        correct = "each day of the month in January starting at 12:00 AM January 1, 2011 until January 31, 2013"
        testrr = rrule_eq(DAILY, dtstart=datetime(2011, 1, 1), until=datetime(2013, 1, 31), bymonth=1)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(time_format="%H:%M:%S %p"), correct)        
    
    def test_weekly(self):
        correct = u"each Monday of the week starting at 12:00 AM August 15, 2011 ten times"
        testrr = rrule_eq(WEEKLY, dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)
        
    def test_yearly(self):
        correct = u"each August 15 of the year starting at 12:00 AM August 15, 2011 ten times"
        testrr = rrule_eq(YEARLY, dtstart=datetime(2011, 8, 15), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)

        correct = u"each Tuesday of the year starting at 12:00 AM August 16, 2011 ten times"
        testrr = rrule_eq(YEARLY, dtstart=datetime(2011, 8, 15), count=10, byweekday=TU)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)

        correct = "each Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, Saturday in January starting at 12:00 AM January 1, 2011 until January 31, 2013"
        testrr = rrule_eq(YEARLY, dtstart=datetime(2011, 1, 1), until=datetime(2013, 1, 31), bymonth=1, byweekday=(SU, MO, TU, WE, TH, FR, SA))
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)

    def test_monthly(self):
        correct = u"each third Friday of the month starting at 12:01 AM August 19, 2011 ten times"
        testrr = rrule_eq(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15, 0, 1), count=10)
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)

        correct = u"every other first Sunday of the month starting at 09:00 PM October 02, 2011 until 09:00 PM August 05, 2012"
        testrr = rrule_eq(MONTHLY, interval=2, byweekday=SU(1), dtstart=datetime(2011, 8, 15, 21, 0, 0), until=datetime(2012, 8, 15))
        hr = human_rrule(testrr)
        self.assertEqual(hr.get_description(), correct)

        correct = u"every other first Sunday of the month starting at 09:00 PM 10/02/2011 until 09:00 PM 08/05/2012"
        self.assertEqual(hr.get_description(date_format="%m/%d/%Y"), correct)

        correct = u"every other first Sunday of the month starting at 21:00 October 02, 2011 until 21:00 August 05, 2012"
        self.assertEqual(hr.get_description(time_format="%H:%M"), correct)
         
         
         
    # def test_get_dict_vals(self):
        # d1 = { 
            # 'a': "I",
            # 'b': {
                # 'a': "am",
                # 'b': "a"
                # },
            # 'c': "recursive",
            # 'd': {
                # "a": "but",
                # "b": "simple"
                # },
            # 'e': "function."
        # } 

        # l = ["I", "am", "a", "recursive", "but", "simple", "function."]
        # dict_vals = human_rrule._get_dict_vals(d1)
        # for i in dict_vals:
            # self.assertIn(i, l)
        # for i in l:
            # self.assertIn(i, dict_vals)

if __name__ == '__main__':
    unittest.main()