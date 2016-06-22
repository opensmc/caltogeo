import requests
import collections

from get_api_key import get_key


Event = collections.namedtuple('Event', [
    'event_id',
    'event_name',
    'address',
    'start_time',
    'end_time',
    'link',
    ]
)

INSTANCES_URL = ('https://www.googleapis.com/calendar/v3/calendars/'
                 '{calendar_id}/events/{event_id}/instances')

EVENT_LIST_URL = ('https://www.googleapis.com/calendar/v3/'
                  'calendars/{calendar_id}/events')

DEFAULT_CALENDAR_ID = (
    'opensmc.org_tgq2v29akgb52a3a0jqq4ti67c%40group.calendar.google.com'
)
DEFAULT_EVENT_ID = 'c86a793khmflcqsss9qj2tpr5g'


def list_events_from_calendar(calendar_id, key):
    """
    Grab everything from a given calendar.

    For reasons I don't understand, this includes both
    event objects with recurrence rules AND recurring event
    IDs. This confuses me.

    :param calendar_id:
    :param key:
    :return:
    """
    url = EVENT_LIST_URL.format(calendar_id=calendar_id)
    r = requests.get(url=url, params={'key': key})
    recurring_ids = set()
    events = []

    for raw_event in r.json()['items']:
        if 'recurringEventId' in raw_event:
            recurring_ids.add(raw_event['recurringEventId'])
            continue
        event = Event(
            event_id=raw_event.get('event_id'),
            address=raw_event.get('location'),
            start_time=raw_event.get('start', {}).get('dateTime'),
            end_time=raw_event.get('end', {}).get('dateTime'),
            event_name=raw_event.get('summary'),
            link=raw_event.get('htmlLink'),
        )
        events.append(event)

    return events, recurring_ids


def get_instances_from_calendar_for_event(calendar_id, event_id, key):
    url = INSTANCES_URL.format(event_id=event_id,
                               calendar_id=calendar_id)
    r = requests.get(url=url, params={'key': key})
    data = r.json()

    events = []
    for raw_event in data['items']:
        event = Event(
            event_id=raw_event.get('event_id'),
            address=raw_event.get('location'),
            start_time=raw_event.get('start', {}).get('dateTime'),
            end_time=raw_event.get('end', {}).get('dateTime'),
            event_name=raw_event.get('summary'),
            link=raw_event.get('htmlLink'),
        )
        events.append(event)
    return events


if __name__ == '__main__':
    key = get_key()
    print(list_events_from_calendar(calendar_id=DEFAULT_CALENDAR_ID,
                                    key=key))
    #results = get_instances_from_calendar_for_event(
    #    calendar_id=DEFAULT_CALENDAR_ID,
    #    event_id=DEFAULT_EVENT_ID,
    #    key=key
    #)
    #print(results)
