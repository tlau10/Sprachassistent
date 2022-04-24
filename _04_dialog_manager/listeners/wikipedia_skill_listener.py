from _04_dialog_manager.event import subscribe, post_event
import wikipediaapi

def handle_wikipedia_search_event(data):
    """
    retrieves page from wikipedia api then posts speech-to-text event
    @param data: term to search for on wikipedia"""
    if len(data) == 0:
        response = "Zu deinem Suchbegriff konnte leider nichts gefunden werden!"
        post_event("text_to_speech", response)
        return

    search_term = data[0]
    wikipedia = wikipediaapi.Wikipedia('de')
    wikipedia_page = wikipedia.page(search_term)

    # not wikipedia page found
    if not wikipedia_page.exists():
        response = "Zu dem Suchbegriff " + search_term + " existiert leider kein Wikipedia-Eintrag!"
        post_event("text_to_speech", response)
        return

    page_summary = wikipedia_page.summary

    first_sentence = page_summary.split('.')[0]
    post_event("text_to_speech", first_sentence)

def setup_wikipedia_event_handlers():
    """
    subcribes all events 
    """
    subscribe("wikipedia_search", handle_wikipedia_search_event)
