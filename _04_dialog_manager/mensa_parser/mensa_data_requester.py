import subprocess
import execjs
from voice_assistant_helper import read_from_file, write_json_file

SEEZEIT_URL = "https://seezeit.com/essen/speiseplaene/mensa-htwg/"
JS_FILE_PATH = "_04_dialog_manager/mensa_parser/parserDateHelper.js"
HTML_FILE_PATH = "_04_dialog_manager/mensa_parser/seezeit_page.html"
JSON_FILE_PATH = "_04_dialog_manager/mensa_parser/menue.json"

def get_html_page():
    """
    retrieves html page
    """
    subprocess.run(["curl", SEEZEIT_URL, "-o", HTML_FILE_PATH], check = True)

def execute_js():
    """
    reads html from file then executes getData() JS function,
    generates json file with menue as output
    """
    js_code = read_from_file(file_path = JS_FILE_PATH)
    html = read_from_file(file_path = HTML_FILE_PATH)

    # compile JS and call function
    js_ctx = execjs.compile(source = js_code)
    json_object = js_ctx.call("getData", html)

    # generate dict of json objects 'date' : 'object'
    json_data = dict()
    for obj in json_object:
        json_data[obj['Date']] = obj

    write_json_file(file_path = JSON_FILE_PATH, json_object = json_data)


if __name__ == "__main__":
    get_html_page()
    execute_js()
