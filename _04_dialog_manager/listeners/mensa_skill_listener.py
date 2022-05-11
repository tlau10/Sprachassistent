from webbrowser import get
from _04_dialog_manager.event import subscribe, post_event
from voice_assistant_helper import read_from_file, read_json_file, write_json_file
import subprocess
import execjs
from datetime import date, timedelta

SEEZEIT_URL = "https://seezeit.com/essen/speiseplaene/mensa-htwg/"
JS_FILE_PATH = "_04_dialog_manager/mensa_parser/parserDateHelper.js"
HTML_FILE_PATH = "_04_dialog_manager/mensa_parser/seezeit_page.html"
JSON_FILE_PATH = "_04_dialog_manager/mensa_parser/menue.json"

def handle_menue_search_event(slots):
    """
    """
    # only call once a week
    #get_html_page()
    #execute_js()

    # get date of requested day
    date_ = get_date_of_day_by_name(None) if 'time' not in slots else get_date_of_day_by_name(slots['time'])

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
    post_event("text_to_speech", response)

def get_date_of_day_by_name(day_name):
    """
    calculates date of given day by name depending on current day
    e.g. day_name="Mittwoch", current_day="12.05.2022" (Donnerstag), 
    returns "18.05.2022" (date of next wednesday)
    @param day_name: name of day
    @return: date of given day_name as dd.mm
    """
    days = {'montag' : 0, 'dienstag' : 1, 'mittwoch' : 2, 'donnerstag' : 3, 'freitag' : 4, 'samstag' : 5, 'sonntag' : 6}
    date_format = "%d.%m"

    if day_name is None or day_name == "heute":
        return date.today().strftime(date_format)
    elif day_name == "morgen":
        result = date.today() + timedelta(days = 1)
        return result.strftime(date_format)

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

    return result.strftime(date_format)

def get_html_page():
    """
    retrieves html page
    """
    subprocess.run(["curl", SEEZEIT_URL, "-o", HTML_FILE_PATH])

def execute_js():
    """
    reads html from file then executes getData() JS function,
    generates json file with menue as output
    """
    js = read_from_file(JS_FILE_PATH)
    html = read_from_file(HTML_FILE_PATH)

    # compile JS and call function
    js_ctx = execjs.compile(js)
    json_object = js_ctx.call("getData", html)

    # generate dict of json objects 'date' : 'object'
    json_data = dict()
    for obj in json_object:
        json_data[obj['Date']] = obj
    
    write_json_file(file_path = JSON_FILE_PATH, json_object = json_data)


def setup_mensa_event_handlers():
    """
    subscribes all events
    """
    subscribe("search_menue", handle_menue_search_event)
