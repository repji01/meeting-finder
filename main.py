# This is a sample Python script.

# Press Shift+F10 to execute it or replace it with your code.
# Press Double Shift to search everywhere for classes, files, tool windows, actions, and settings.
from person import Person


def time_to_minutes(time_str):
    h, m = time_str.replace(" ", "").split(":")
    return 60 * int(h) + int(m)


def compare_time(time1, time2):
    t1_minutes = time_to_minutes(time1)
    t2_minutes = time_to_minutes(time2)
    if t1_minutes > t2_minutes:
        ret = 1
    elif t1_minutes < t2_minutes:
        ret = -1
    else:
        ret = 0
    return ret


def combine_calendars(person, other_person):
    meetings = list()
    if compare_time(person.work_start, other_person.work_start) == -1:
        meetings_start = other_person.work_start
    else:
        meetings_start = person.work_start
    meetings.append([meetings_start, meetings_start])
    if compare_time(person.work_end, other_person.work_end) == 1:
        meetings_end = other_person.work_end
    else:
        meetings_end = person.work_end
    person_idx, other_person_idx = 0, 0
    while compare_time(meetings_start, person.calendar[person_idx][0]) == 1 and person_idx < len(person.calendar):
        person_idx += 1
    while compare_time(meetings_start, other_person.calendar[other_person_idx][0]) == 1 and other_person_idx < len(
            other_person.calendar):
        other_person_idx += 1

    while person_idx < len(person.calendar) and other_person_idx < len(other_person.calendar):
        person_meet_entry = person.calendar[person_idx]
        other_person_meet_entry = other_person.calendar[other_person_idx]
        if compare_time(person_meet_entry[0], other_person_meet_entry[0]) == -1:

            if compare_time(person_meet_entry[1], meetings_end) < 1:
                meetings.append(person_meet_entry)
            person_idx += 1
        else:

            if compare_time(other_person_meet_entry[1], meetings_end) < 1:
                meetings.append(other_person_meet_entry)
            other_person_idx += 1
    for idx in range(person_idx, len(person.calendar)):
        person_meet_entry = person.calendar[idx]
        # if compare_time(person_meet_entry[0], meetings[-1][1]) == 1:
        if compare_time(person_meet_entry[0], meetings_end) < 1:
            meetings.append(person_meet_entry)
    for idx in range(other_person_idx, len(other_person.calendar)):
        other_person_meet_entry = other_person.calendar[idx]
        # if compare_time(other_person_meet_entry[0], meetings[-1][1]) == 1:
        if compare_time(other_person_meet_entry[0], meetings_end) < 1:
            meetings.append(other_person_meet_entry)
    meetings.append([meetings_end, meetings_end])
    return meetings


def suggest_meeting(person, other_person, minutes):
    combined_meetings = combine_calendars(person, other_person)
    reduced_meetings = combined_meetings[:1]
    for meeting_idx in range(1, len(combined_meetings)):
        if meeting_idx < len(combined_meetings):
            if compare_time(combined_meetings[meeting_idx][0], reduced_meetings[-1][1]) < 1:
                reduced_meetings[-1][1] = combined_meetings[meeting_idx][1]
            else:
                reduced_meetings.append(combined_meetings[meeting_idx])
    times_suggested = list()
    for meeting_idx in range(0, len(reduced_meetings) - 1):
        meeting_gap_duration = time_to_minutes(reduced_meetings[meeting_idx + 1][0]) - time_to_minutes(
            reduced_meetings[meeting_idx][1])
        if meeting_gap_duration >= minutes:
            times_suggested.append([reduced_meetings[meeting_idx][1], reduced_meetings[meeting_idx + 1][0]])
    return times_suggested


def main():
    peter = Person("Peter", "Black", "09:00", "20:00", "09:00 - 10:30, 12:00 - 13:00, 16:00 - 18:00")
    john = Person("John", "Doe", "10:00", "18:30", "10:00 - 11:30, 12:30 - 14:30, 14:30 - 15:00, 16:00 - 17:00")
    meeting_duration = 45
    print(peter)
    print(john)
    print(f"We need meeting for {meeting_duration} minutes")
    print(f"Times for meeting suggested for {peter.name} and {john.name} " +
          ", ".join(f"{meet[0]}-{meet[1]}" for meet in suggest_meeting(peter, john, meeting_duration)))


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()
