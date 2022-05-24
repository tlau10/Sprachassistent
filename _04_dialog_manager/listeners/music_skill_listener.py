from _04_dialog_manager.event import subscribe
from pyradios import RadioBrowser
import random
from voice_assistant_helper import write_to_file
from decouple import config

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
            response = f"Der Radiosender {station_name} existiert leider nicht!"
            write_to_file(file_path = config('DIALOG_MANAGER_OUTPUT_PATH'), text = response)
            return
        station_url = radio_station[0]['url']

    print(station_url)

    write_to_file(file_path = config('DIALOG_MANAGER_OUTPUT_PATH'), text = station_url)

def setup_music_event_handlers():
    """
    subscribes all events
    """
    subscribe("play_radio_station", handle_play_radio_station_event)
