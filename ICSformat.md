# ICS meeting change messages

For the farmers markets and flu clinic applications only 6 ICS paramters are needed to define an event:  

* **DTSTART**, **DTEND**, **RRULE** for event time information.
* **LOCATION**, **DESCRIPTION**, **SUMMARY** for information about the event itself.

The protocol is quite simple:  
Updates and additions are made by simply repeating the field:value pairs.  
The new values overwrite the old.

Additions (invitees, notifications) are simply added to VEVENT record.  
Not sure how deletions are handled.

The unique identifier is the **UID**.  
This is the common thread for a single event.  
This is the look-up key for the event.
  
# VEVENT message structure per event

For each separate event.

| Keyword: | Sample | Description |
| -------- | ------ | ----------- |
| BEGIN: | VEVENT | |
|-|-|-|
| DTSTART;TZID=America/Los_Angeles: | YYYYMMDD**T**HHMMSS | Start of event |
| DTEND;TZID=America/Los_Angeles: | YYYYMMDD**T**HHMMSS | End of event |
|-|-|-|
| RRULE: | FREQ=WEEKLY;UNTIL=YYYYMMDD**T**HHMMSS | Recurring event |
|-|-|-|
| LOCATION: | 251 Stage Road Pescadero\, CA 94060 | One line escaped chars |
| DESCRIPTION: | *description* |  One line escaped chars | 
| SUMMARY: | *summary message* | |
|-|-|-|
| UID: | UniqueSeqNum@example.com | Unique ID for specific event |
| SEQUENCE: | 0 | Number of times event has been updated |
| CREATED: | YYYYMMDD**T**HHMMSS**Z** | |
| LAST-MODIFIED: | YYYYMMDD**T**HHMMSS**Z** | Changed every time event is updated |
|-|-|-|
| DTSTAMP: | YYYYMMDD**T**HHMMSS**Z** | per record/group of records timestamp |
|-|-|-|
| STATUS: | CONFIRMED | Per attendee? Per event? |
| CLASS: | PUBLIC | Public/private |
| TRANSP: | TRANSPARENT/OPAQUE | Busy/available |
|-|-|-|
| ATTENDEE; | | Multipart record |
| CUTYPE= | INDIVIDUAL; | |
| ROLE= | REQ-PARTICIPANT; | |
| PARTSTAT= | ACCEPTED; | |
| CN= | Farmers* Markets; | Name of event |
| X-NUM-GUESTS= | 0: | | X- custom header |
| | mailto:*event/calendar UID*@example.com | Confirmation address |
|-|-|-|
| END: | VEVENT | |

## VCALENDAR ical message structure

Can contain multiple events

The basic format of an ICS attachment

| Keyword | Sample | Description |
| ------- | ------ | ----------- |
| BEGIN: | VCALENDAR | 
| PRODID: | -//Google Inc//Google Calendar 70.9054//EN | Preamble | 
| VERSION: | 2.0 | Preamble | 
| CALSCALE: | GREGORIAN | Preamble, optional | 
| --- | --- | --- | --- |
| METHOD: | PUBLISH | ICS command | 
| --- | --- | --- | --- |
| X-WR-CALNAME: | Farmers' Markets | Custom X- line type |
| X-WR-TIMEZONE: | America/Los_Angeles | from | 
| X-WR-CALDESC: | *description* | google calendar |
| --- | --- | --- | --- |
| BEGIN: | VTIMEZONE | Optional per calendar/event | 
| TZID: | America/Los_Angeles | Used in VEVENT TZID= | 
| (A bunch of TZ related data): | | 
| END: | VTIMEZONE | | 
| --- | --- | --- | --- |
| | | Sequence of VEVENTS: |
| --- | --- | --- | --- |
| END: | VCALENDAR | End of ICS attachment | 

## Various ICS commands/update messages

Diffs of change message commands

DTSTAMP: per record/group of records timestamp

### Change of time:
* &lt; DTSTART:20160611T160000Z  
  &lt; DTEND:20160612T000000Z
* &gt; DTSTART;VALUE=DATE:20160611  
  &gt; DTEND;VALUE=DATE:20160612

### Change public/private:
* &lt; CLASS:PUBLIC
* &gt; CLASS:PRIVATE

* &lt; DESCRIPTION: version 1
* &gt; DESCRIPTION: version 2


### Busy:
* &lt; TRANSP:TRANSPARENT
* &gt; TRANSP:OPAQUE

### Notification:
* &gt; BEGIN:VALARM  
  &gt; ACTION:EMAIL  
  &gt; DESCRIPTION:This is an event reminder  
  &gt; SUMMARY:Alarm notification  
  &gt; ATTENDEE:mailto:harker-opensmc@harker.com  
  &gt; TRIGGER:-P0DT15H0M0S  
  &gt; END:VALARM

### Added recurring event:

Recurring events have a RRULE and a start and stop time

* &gt; RRULE:FREQ=WEEKLY;UNTIL=20160716;BYDAY=SA

### Changed number of events:
* &lt; RRULE:FREQ=WEEKLY;UNTIL=20160716;BYDAY=SA
* &gt; RRULE:FREQ=WEEKLY;COUNT=35;BYDAY=SA

### Canceled the event
* &lt; METHOD:REQUEST
* &gt; METHOD:CANCEL

* &lt; STATUS:CONFIRMED
* &gt; STATUS:CANCELLED

* &lt; ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;RSVP=TRUE  
  &lt;  ;CN=harker@opensmc.org;X-NUM-GUESTS=0:mailto:harker@opensmc.org
* &lt; ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;RSVP=  
  &lt;  TRUE;CN=harker-opensmc@harker.com;X-NUM-GUESTS=0:mailto:harker-opensmc@hark  
  &lt;  er.com

* &gt; ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=ACCEPTED;CN=harker  
  &gt;  @opensmc.org;X-NUM-GUESTS=0:mailto:harker@opensmc.org
* &gt; ATTENDEE;CUTYPE=INDIVIDUAL;ROLE=REQ-PARTICIPANT;PARTSTAT=NEEDS-ACTION;CN=ha  
  &gt;  rker-opensmc@harker.com;X-NUM-GUESTS=0:mailto:harker-opensmc@harker.com  

