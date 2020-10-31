import os.path
import pickle
from datetime import datetime

from google.auth.transport.requests import Request
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

from meeting import Meeting

categories = [
    # Lavender
    '#a4bdfc',
    # Blueberry
    '#5484ed',
    # Peacock
    '#46d6db',
    # Sage
    '#7ae7bf',
    # Basil
    '#51b749',
    # Tangerine
    '#ffb878',
    # Banana
    '#fbd75b',
    # Flamingo
    '#ff887c',
    # Tomato
    '#dc2127',
    # Mandarine
    '#fa573c',
    # Grape
    '#dbadff',
    # Graphite
    '#e1e1e1',
    '#9fe1e7'
]


EVENTS_TO_LOOK_THROUGH = 60
# If modifying these scopes, delete the file token.pickle.
SCOPES = ['https://www.googleapis.com/auth/calendar.readonly']


def prepare_credentials():
    creds = None
    # The file token.pickle stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server()
        # Save the credentials for the next run
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    return creds


def download_calendar_events(service, start, end):
    events_result = service.events().list(calendarId='primary', timeMin=start, timeMax=end,
                                          maxResults=EVENTS_TO_LOOK_THROUGH, singleEvents=True,
                                          orderBy='startTime').execute()
    colors = service.colors().get(fields='event').execute()
    default_color = (service.calendarList().get(calendarId="primary").execute())['backgroundColor']
    events = events_result.get('items', [])
    meetings = {key: list() for key in categories}

    if not events:
        print('No upcoming events found.')
    for event in events:

        start_string = event['start'].get('dateTime', event['start'].get('date'))
        end_string = event['end'].get('dateTime', event['end'].get('date'))

        name = event['summary']
        try:
            color = colors['event'][event['colorId']]['background']
        except KeyError:
            color = default_color
        meeting = Meeting(name, parse_time(start_string), parse_time(end_string), color)
        meeting.date = parse_time(start_string)
        meeting.get_time_of_task()
        meetings[color].append(meeting)

    return meetings


def get_meetings(day, color):
    """Shows basic usage of the Google Calendar API.
    Prints the start and name of the next 10 events on the user's calendar.
    """

    service = build('calendar', 'v3', credentials=prepare_credentials())

    # Call the Calendar API

    day_start = datetime(day.year, day.month, day.day, 0, 0).isoformat() + 'Z'
    day_end = datetime(day.year, day.month, day.day, 23, 59, 59).isoformat() + 'Z'

    meetings = download_calendar_events(service, day_start, day_end)
    return meetings[color]


def main():
    day = datetime.utcnow()
    for meet in get_meetings(day, '#dc2127'):
        print(meet)
    for meet in get_meetings(day, '#9fe1e7'):
        print(meet)


def parse_time(timestamp):
    # Takes a timestamp string and returns a datetime object
    try:
        time_object = datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%S%z")
    except ValueError:
        # If no start and end time is specified the format string must be different
        time_object = datetime.strptime(timestamp, "%Y-%m-%d")
    return time_object


if __name__ == '__main__':
    main()
