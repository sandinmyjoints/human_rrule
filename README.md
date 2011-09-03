# human_rrule #

rrules (recurrence rules) typically look something like `DTSTART:19970902T090000;RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5`. Friendly? human_rrule prints nice natural language descriptions of rrules created by the dateutil library, turning our friend into (a dictionary-like object that can yield a string a human can easily read, such as) "Every tenth day starting at 09:00 AM, five times".

## Caution ##

human_rrule is not yet fully functional; in fact, it's actively under development. Use at your own caution.

## Notes ##

Note that human_rrule uses as its start datetime the datetime of the actual first occurrence according to the rule, which can be but does not have to be equal to dtstart. According to the iCalendar standard, "The "DTSTART" property defines the first instance in the recurrence set." However, when actually using rrule, you can set a dtstart to be any value, and rrule will extract any missing info it needs to calculate the set of recurrences from dtstart, but if the rrule itself generates a start datetime that comes after dtstart (it can never come before), then it will do so.

An example:

    rrule(YEARLY, dtstart=datetime(2011, 8, 15), count=10, byweekday=TU)

will generate datetime(2011, 8, 16)--not datetime(2011, 8, 15)--as its first occurrence because August 15, 2011, was a Monday, and the rule has a byweekday parameter set to Tuesday.

Same goes for the end datetime. 