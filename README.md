# human_rrule #

rrules (recurrence rules) typically look something like `DTSTART:19970902T090000;RRULE:FREQ=DAILY;INTERVAL=10;COUNT=5`. Friendly? human_rrule prints nice natural language descriptions of rrules created by the dateutil library, turning our friend into (a dictionary-like object that can yield a string a human can easily read, such as) "Every tenth day starting at midnight, five times".

## Caution ##

human_rrule is not yet fully functional; in fact, it's actively under development. Use at your own caution.