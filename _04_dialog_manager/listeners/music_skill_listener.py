import random
from pyradios import RadioBrowser
from decouple import config
from _04_dialog_manager.event import post_event, subscribe
from _04_dialog_manager.manual_learning.voice_assistant_bot_helper import lookup_entry
from voice_assistant_helper import write_to_file

def handle_play_radio_station_event(slots):
    """
    retrieves stream url from radio browser api then writes output to file
    @param slots: dict of recognized slot values 'slotName' : 'slotValue'
    """
    radio_browser = RadioBrowser()

    if len(slots) == 0:
        # choose random radio station
        radio_stations = radio_browser.stations_by_countrycode(code = "DE")
        radio_station = random.choice(radio_stations)
        station_name = radio_station['name']
        station_url = radio_station['url']
    else:
        # retrieve explicit radio station
        station_name = slots['radio_station']
        radio_station = radio_browser.search(name = station_name, name_exact = True)

        # no radio station found
        if not radio_station:
            ###Learning###
            new_station_name = lookup_entry()
            print(f"new_station_name {new_station_name}")

            # check if something in entries was found
            if new_station_name:
                radio_station = radio_browser.search(name = new_station_name, name_exact = True)

            # nothing was found for radio_station from entries or no entry was found
            if not radio_station or not new_station_name:
                response = f"Der Radiosender {station_name} existiert leider nicht!"
                write_to_file(file_path = config('DIALOG_MANAGER_OUTPUT_PATH'), text = response)
                post_event("start_learning", 3)
                return
            ###Learning###
        station_url = radio_station[0]['url']

    print(station_url)

    write_to_file(file_path = config('DIALOG_MANAGER_OUTPUT_PATH'), text = station_url)

    ###Learning###
    post_event("start_learning", 2)
    ###Learning###

def setup_music_event_handlers():
    """
    subscribes all events
    """
    subscribe("play_radio_station", handle_play_radio_station_event)
