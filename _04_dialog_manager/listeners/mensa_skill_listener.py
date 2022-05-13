from _04_dialog_manager.event import subscribe, post_event
from voice_assistant_helper import read_json_file
from datetime import date, timedelta

JSON_FILE_PATH = "_04_dialog_manager/mensa_parser/menue.json"

def handle_menue_search_event(slots):
    """
    retrieves menue data from json file then generates text and posts dialog_manager_output event
    @param slots: dict of recognized slot values 'slotName' : 'slotValue'
    """
    # get date of requested day
    time = slots.get('time')
    date_, index = get_date_of_day_by_name(time)

    # check if time is saturday or sunday, and also check index of weekday
    if time == "samstag" or time == "sonntag" or index == 5 or index == 6:
        time = "samstag" if index == 5 else "sonntag"
        response = f"Am {time} hat die Mensa geschlossen"
        post_event("dialog_manager_output", response)
        return

    # retrieve json object for calculated date
    menue = read_json_file(file_path = JSON_FILE_PATH)
    menue_of_day = menue[date_]

    # retrieve menue descriptions
    menue_descriptions = dict()
    for key,value in menue_of_day['Menu'].items():
        menue_descriptions[key] = value['Description']
    del menue_descriptions['Pastastand vegetarisch']
    del menue_descriptions['Beilagen']

    print(menue_descriptions)

    # generate text
    response = [f"{key} {menue_descriptions[key]}" for key in menue_descriptions]

    chosen_menue = slots.get('menue')
    available_menues = ["Seezeit-Teller", "hin&weg", "KombinierBar", "Pastastand"]
    if chosen_menue is not None and chosen_menue in available_menues:
        response = menue_descriptions[slots['menue']]
    else:
        response = "".join(response)

    response = f"Am {date_} gibt es {response}"
    post_event("dialog_manager_output", response)

def get_date_of_day_by_name(day_name):
    """
    calculates date of given day by name depending on current day
    e.g. day_name="Mittwoch", current_day="12.05.2022" (Donnerstag), 
    returns "18.05.2022" (date of next wednesday)
    @param day_name: name of day
    @return: tuple (date as dd.mm, index of date) of given day_name
    """
    days = {'montag' : 0, 'dienstag' : 1, 'mittwoch' : 2, 'donnerstag' : 3, 'freitag' : 4, 'samstag' : 5, 'sonntag' : 6}
    date_format = "%d.%m"

    # return current day if no day_name was given, if it is an invalid day_name or if it is "heute"
    if day_name is None or day_name not in days or day_name == "heute":
        result = date.today()
        index_target = result.weekday()
        return result.strftime(date_format), index_target
    elif day_name == "morgen":
        result = date.today() + timedelta(days = 1)
        index_target = result.weekday()
        return result.strftime(date_format), index_target

    index_today = date.today().weekday()
    index_target = days.get(day_name)
    days_diff = abs(index_today - index_target)

    if index_today == index_target:
        result = date.today() + timedelta(weeks = 1)
    # target day is in future
    elif index_today < index_target:
        result = date.today() + timedelta(days = days_diff)
    # target day is in past
    elif index_today > index_target:
        result = date.today() + timedelta(days = -days_diff, weeks = 1)
    # otherwise return current date
    else:
        result = date.today()

    return result.strftime(date_format), index_target

def setup_mensa_event_handlers():
    """
    subscribes all events
    """
    subscribe("search_menue", handle_menue_search_event)
