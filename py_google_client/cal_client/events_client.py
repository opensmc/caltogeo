"""
Basic library methods to grab events from a Google Calendar in a very
simple and overdone manner.

You can import these functions, or just run this as a script.
"""

import json
import logging
import requests
import argparse
import collections

from get_api_key import get_key


# Here to standardize data.
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
    """
    Given a recurring event ID we can pull a list of specific events. Use
    that to grab any events that belong to that particular recurring event.

    :param calendar_id: A Google calendar ID
    :param event_id: A Google recurring event ID
    :param key: Google API Key
    :return:
    """
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


def dump_events_to_file(event_list, outfile):
    """
    Take a list of assembled Event namedtuples and
    dump them to a JSON file
    :param event_list:
    :return:
    """
    if not outfile:
        # Nobody wants to do this.
        return

    dict_list = [x._asdict() for x in event_list]

    with open(outfile, 'w') as f:
        json.dump(dict_list, f)


if __name__ == '__main__':
    # Given a calendar ID, get all events attached to it
    # and output the important parts in JSON.
    parser = argparse.ArgumentParser(description='Get Calendar Data')
    parser.add_argument('--secret_file', type=str, default=None)
    parser.add_argument('--output_file', type=str, default='/tmp/out.json',
                        help='File to write JSON to')
    parser.add_argument('--calendar_id', type=str,
                        default=DEFAULT_CALENDAR_ID,
                        help='Google ID of relevant calendar')
    args = parser.parse_args()
    key = get_key(args.secret_file)
    events, recurring_ids = list_events_from_calendar(
        calendar_id=DEFAULT_CALENDAR_ID,
        key=key,
    )
    for recurring_id in recurring_ids:
        new_events = get_instances_from_calendar_for_event(
            calendar_id=DEFAULT_CALENDAR_ID,
            event_id=recurring_id,
            key=key,
        )
        events.extend(new_events)

    logging.info('Processed {} events'.format(len(events)))

    dump_events_to_file(event_list=events,
                        outfile=args.output_file)
