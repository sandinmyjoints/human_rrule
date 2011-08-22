#!/usr/bin/env python
# encoding: utf-8
"""
rrule2text.py

Created by William Bert on 2011-08-12.
Copyright (c) 2011. All rights reserved.
"""

# TODO Add i18n

import sys
import os
import unittest
from datetime import datetime, time

import dateutil
from dateutil.rrule import * # gets DAILY, WEEKLY, MONTHLY, etc.
from dateutil.rrule import weekday
from dateutil.rrule import rrule as rr
from dateutil.relativedelta import relativedelta as rd

from int2word import int2word

        
class Rrule2textError(ValueError):
    pass

class rrule2text(rr): 
    """Provide methods that return natural language descriptions of a dateutil.rrule 
    (aka a recurrence rule). Useful for describing recurring events in a calendar or
    event app.
    
    `rr` 
    Recurrence rule to get a natural language description of.
    
    """
    
    WEEKDAY_MAP = {
        u'SU': u"Sunday",
        u'MO': u"Monday",
        u'TU': u"Tuesday",
        u'WE': u"Wednesday",
        u'TH': u"Thursday",
        u'FR': u"Friday",
        u'SA': u"Saturday",
    }
    
    ORDINAL = (
        (1,  u'first'),
        (2,  u'second'),
        (3,  u'third'),
        (4,  u'fourth'),
        (-1, u'last')
    ) 
    
    WEEKDAY_LONG = (
        (7, u'Sunday'),
        (1, u'Monday'),
        (2, u'Tuesday'),
        (3, u'Wednesday'),
        (4, u'Thursday'),
        (5, u'Friday'),
        (6, u'Saturday')
    )
    
    INTERVAL = (
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

    def text(self, date_format="%B %d, %Y", time_format="%I:%M %p"):
        """Return a recurrence rule in plain English (or whatever language, once translation
        is supported. :)
        
        `date_format`
        An optional argument that specifies the format to print dates using strftime 
        formatting rules.
        
        `time_format`
        An optional argument that specifies the format to print times using strftime
        formatting rles.
        """
        
        dtstart = self._dtstart # datetime of when each occurrence starts. Defaults to now, down to the second.
        freq = self._freq # when the recurrence recurs, secondly through yearly. Required.
        interval = self._interval # how often the recurrence happens, each time through every nth time. Defaults to 1.
        wkst = self._wkst # Week start day, ie, an int representing which day of the week starts the week, usually Sunday or Monday. Defaults to calendar.firstweekday().
        until = self._until # datetime until which the recurrence continues. Only it or count is set, not both.
        count = self._count # Number of times the event happens before it stops. Only it or until is set, not both.
        tzinfo = self._tzinfo # Time zone information. Defaults to the tzinfo of dtstart.
        bymonth = self._bymonth # Which month a yearly event recurs in.
        byweekno = self._byweekno # Which week number a yearly event recurs in.
        byyearday = self._byyearday # Which day of the year a yearly event recurs in.
        byweekday = self._byweekday # Which weekday an event recurs in.
        bynweekday = self._bynweekday # 
        byeaster = self._byeaster
        bymonthday = self._bymonthday # Relative day of the month
        bynmonthday = self._bynmonthday # Negative relative day of the month
        bysetpos = self._bysetpos # For sets of seconds/minutes/hours/days/weeks/months/years, specifies which position in the list to pay attention to.
        byhour = self._byhour
        byminute = self._byminute
        bysecond = self._bysecond
        # YEARLY needs to have bymonth and bymonthday set
        # MONTHLY needs to have bymonthday set 
        # WEEKLY needs to have byweekday set
        
        text_description = []
        
        if freq == YEARLY:
            pass
        elif freq == MONTHLY:
            
            # Get the interval. "Each", "Every other", "Every third", etc.
            p_interval = rrule2text.INTERVAL[interval-1][1]
            text_description.append(p_interval)

            # bynweekday is a tuple of (weekday, week_in_month) tuples
            for rule_pair in bynweekday:

                # Get the ordinal.
                for ord in rrule2text.ORDINAL:
                    if ord[0] == rule_pair[1]:
                        text_description.append(ord[1])
                        break

                #  Get the weekday name
                p_weekday = weekday(rule_pair[0])
                name = rrule2text.WEEKDAY_MAP[unicode(p_weekday)]
                text_description.append(name)
                
                text_description.append("at")
                
                text_description.append(dtstart.strftime(time_format))
                
                # tack on "and interval" for the next item in the list
                text_description.extend(["and", p_interval])

            # remove the last "and interval" because it's hanging off the end
            # TODO improve this
            text_description = text_description[:-2]
        
        elif freq == WEEKLY:
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
            raise Rrule2textError, "Frequency value of %s is not valid." % freq
        
        if count:
            text_description.append("%s %s" % (int2word(count).rstrip(), "times"))
        elif until:
            text_description.extend(["until", until.strftime(date_format)])
            
        return map(unicode, text_description)
        
    def __eq__(self, other):
        """Compare two rrule2text instances."""
        
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
        
class rr_dict(dict):
    """Represents a verbal description of an rrule.
    
    Keys: 
    frequency
    interval
    period
    time
    terminal
    """
    
    def __init__(self, rrule):
        #self["frequency"] 
        super(rr_dict, self).__init__()
        self.__rrule = rrule
        self._refresh_dict()
    
    def _refresh_dict(self):
        # Populate the rr_dict components with values based on the properties of 
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
        bynweekday = rr._bynweekday # By negative weekday
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
                
        if freq == YEARLY:
            pass
        elif freq == MONTHLY:
            
            # Get the interval. "Each", "Every other", "Every third", etc.
            p_interval = rrule2text.INTERVAL[interval-1][1]
            self["frequency"] = p_interval

            # bynweekday is a tuple of (weekday, week_in_month) tuples
            for rule_pair in bynweekday:

                # Get the ordinal. TODO handle multiple ordinals
                ord_text = []
                for ord in rrule2text.ORDINAL:
                    if ord[0] == rule_pair[1]:
                        ord_text.append(ord[1])
                        break

                #  Get the weekday name
                p_weekday = weekday(rule_pair[0])
                name = [rrule2text.WEEKDAY_MAP[unicode(p_weekday)]]
                ord_text.extend(name)
                self["interval"] = " ".join(name)
                
                self["period"] = "of the month"                
                
                self["starting at"] = dtstart
                
                self["lasting to"] = dtstart # TODO fix this
                        
        elif freq == WEEKLY:
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
            raise Rrule2textError, "Frequency value of %s is not valid." % freq
        
        if count:
            self["terminal"] = "%s %s" % (int2word(count).rstrip(), "times")
        elif until:
            self["terminal"] = ["until", until]
        
    def get_rrule(self):
        return self.__rule
        
    def set_rrule(self, rrule):
        self.__rule = rule
        self._refresh_dict()
        
    rrule = property(get_rrule, set_rrule)
    
    
    def get_description(self, date_format="%B %d, %Y", time_format="%I:%M %p"):
        """Returns a string consisting of all the values of an rr_dict in 
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

        return " ".join(desc)
        
    def __unicode__(self):
        return map(unicode, self.get_description())
        
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
        rr_dict._do_get_dict_vals(pdict, list)
        return list

    @staticmethod
    def _do_get_dict_vals(pdict, list):
        for v in pdict.values():
            if isinstance(v, dict):
                rr_dict._do_get_dict_vals(v, list)
            else:       
                list.append(v)
            
    
class rrule2textTests(unittest.TestCase):
    def setUp(self):
        pass

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
        dict_vals = rr_dict._get_dict_vals(d1)
        for i in dict_vals:
            self.assertIn(i, l)
        for i in l:
            self.assertIn(i, dict_vals)
                
        
    def test_equals(self):
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        self.assertTrue(r1==r2)
        
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        self.assertTrue(r1==r2)
        
    def test_not_equals(self):
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15))
        r2 = rrule2text(MONTHLY, dtstart=datetime(2012, 8, 15))
        self.assertFalse(r1==r2)
        
        r2 = rrule2text(DAILY, dtstart=datetime(2011, 8, 15))
        self.assertFalse(r1==r2)
        
        r1 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=MO)
        r2 = rrule2text(DAILY, dtstart=datetime(2012, 8, 15), byweekday=TU)
        self.assertFalse(r1==r2)
        
        
    # def test_invalid_freq(self):
    #     testrr = rrule2text(8, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(Rrule2textError, testrr.text)
    # 
    #     testrr = rrule2text("a", byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(Rrule2textError, testrr.text)
    # 
    #     testrr = rrule2text(None, byweekday=MO, dtstart=datetime(2011, 8, 15), until=datetime(2012, 8, 15))
    #     self.assertRaises(Rrule2textError, testrr.text)
    #     
    #     
    def test_monthly(self):
        # correct = map(unicode, ["each", "third", "Friday", "at", "12:00 AM", "ten times"])
        correct = "each third Friday of the month starting at 12:00 AM lasting to 1:00 AM ten times"
        testrr = rrule2text(MONTHLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
        rd = rr_dict(testrr)
        self.assertEqual(rd.get_description(), correct)
        
        # correct = map(unicode, ["every other", "first", "Sunday", "at", "09:00 PM", "until", "August 15, 2012"])
        # testrr = rrule2text(MONTHLY, interval=2, byweekday=SU(1), dtstart=datetime(2011, 8, 15, 21, 0, 0), until=datetime(2012, 8, 15))
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
    #     testrr = rrule2text(YEARLY, byweekday=FR(3), dtstart=datetime(2011, 8, 15), count=10)
    #     self.assertListEqual(testrr.text(), correct)
        


if __name__ == '__main__':
    unittest.main()