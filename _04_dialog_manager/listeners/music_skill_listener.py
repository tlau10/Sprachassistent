from _04_dialog_manager.event import subscribe, post_event
from pyradios import RadioBrowser
import vlc
import random

def handle_play_radio_station_event(data):
    """
    retrieves stream url from radio browser api, plays stream using vlc
    @param data: name of radio station to play, plays random german radio station if empty
    """
    radio_browser = RadioBrowser()

    if len(data) == 0:
        # choose random radio station
        radio_stations = radio_browser.stations_by_countrycode("DE")
        radio_station = random.choice(radio_stations)
        station_name = radio_station['name']
        station_url = radio_station['url']
    else:
        # retrieve explicit radio station
        station_name = data[0]
        radio_station = radio_browser.search(name = station_name, name_exact = True)

        # no radio station found
        if not radio_station:
            response = f"Der Radiosender {station_name} existiert leider nicht!"
            post_event("text_to_speech", response)
            return
        station_url = radio_station[3]['url']

    print(station_url)

    response = f"Radiosender {station_name} wird abgespielt!"
    post_event("text_to_speech", response)

    # play stream
    audio = vlc.Instance()
    music_player = audio.media_player_new()
    music_player.set_mrl(station_url)
    music_player.play()

def setup_music_event_handlers():
    """
    subscribes all events
    """
    subscribe("play_radio_station", handle_play_radio_station_event)
