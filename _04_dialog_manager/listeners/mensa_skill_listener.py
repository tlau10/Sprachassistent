from _04_dialog_manager.event import subscribe, post_event
from voice_assistant_helper import read_from_file, write_to_file
import subprocess
import execjs
from datetime import date, timedelta

SEEZEIT_URL = "https://seezeit.com/essen/speiseplaene/mensa-htwg/"
JS_FILE_PATH = "_04_dialog_manager/mensa_parser/parserDateHelper.js"
HTML_FILE_PATH = "04_dialog_manager/mensa_parser/seezeit_page.html"
JSON_FILE_PATH = "04_dialog_manager/mensa_parser/menue.json"

def handle_menue_search_event(data):
    """
    """
    # get date
    # if date empty assume current day
    # if date "morgen" assume current day+1
    # else call get_date_...()

    # retrieve json object for calculated date

    # retrieve json object for given menue from formerly retrieven object

def get_date_of_day_by_name(day_name):
    """
    calculates date of given day by name depending on current day
    e.g. day_name="Mittwoch", current_day="12.05.2022" (Donnerstag), 
    returns "18.05.2022" (date of next wednesday)
    @param day_name: name of day
    @return: date of given day_name
    """
    days = {'Montag' : 0, 'Dienstag' : 1, 'Mittwoch' : 2, 'Donnerstag' : 3, 'Freitag' : 4, 'Samstag' : 5, 'Sonntag' : 6}

    index_today = date.today().weekday()
    index_target = days.get(day_name)
    days_diff = abs(index_today - index_target)

    if index_today == index_target:
        return date.today() + timedelta(weeks = 1)
    # target day is in future
    elif index_today < index_target:
        return date.today() + timedelta(days = days_diff)
    # target day is in past
    elif index_today > index_target:
        return date.today() + timedelta(days = -days_diff, weeks = 1)
    # otherwise return current date
    else:
        return date.today()

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

    js_ctx = execjs.compile(js)
    json_object = js_ctx.call("getData", html)

    write_to_file(JSON_FILE_PATH, json_object)

def setup_mensa_event_handlers():
    """
    subscribes all events
    """
    subscribe("search_menue", handle_menue_search_event)
