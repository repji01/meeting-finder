# Meeting finder
Two calendars and meeting duration. The output is a meeting suggestion.

#### Sample calendar:
![Alt text](doc/calendar_example.png?raw=true "Title")

#### Sample output:
```
Peter Black is working 09:00 - 20:00. Calendar meetings for today: 09:00-10:30, 12:00-13:00, 16:00-18:00 
John Doe is working 10:00 - 18:30. Calendar meetings for today: 10:00-11:30, 12:30-14:30, 14:30-15:00, 16:00-17:00 
We need meeting for 45 minutes
Times for meeting suggested for Peter and John 15:00-16:00
```

To start use the script you first need to go to https://developers.google.com/calendar/quickstart/python adn press the "ENABLE THE GOOGLE CALENDAR API" to activate it. 
Then you will get a popu with a file called credentials.json, that you will need to download.
After that just add that file to the project root folder and then in the console or terminal you can run it by typing in: python calendarauto.py
