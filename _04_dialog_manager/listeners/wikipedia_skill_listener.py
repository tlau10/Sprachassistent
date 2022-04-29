from _04_dialog_manager.event import subscribe, post_event
import wikipediaapi
import re

REGEX_FIND_PARENTHESIS_PAIRS = "\(.*?\)"

def handle_wikipedia_search_event(data):
    """
    retrieves page from wikipedia api then posts speech-to-text event
    @param data: term to search for on wikipedia"""
    if len(data) == 0:
        response = "Zu deinem Suchbegriff konnte leider nichts gefunden werden!"
        post_event("text_to_speech", response)
        return

    search_term = data[0]

    # replace whitespaces with an underscore and make the first letter of every word uppercase
    term = search_term.replace(" ", "_").title()

    wikipedia = wikipediaapi.Wikipedia('de')
    wikipedia_page = wikipedia.page(term)

    # not wikipedia page found
    if not wikipedia_page.exists():
        response = "Zu dem Suchbegriff " + search_term + " existiert leider kein Wikipedia-Eintrag!"
        post_event("text_to_speech", response)
        return

    page_summary = wikipedia_page.summary
    page_summary = re.sub(REGEX_FIND_PARENTHESIS_PAIRS, "", page_summary)

    first_sentence = page_summary.split('.')[0]
    post_event("text_to_speech", first_sentence)

def setup_wikipedia_event_handlers():
    """
    subcribes all events 
    """
    subscribe("search_definition", handle_wikipedia_search_event)
