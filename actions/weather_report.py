# actions/weather_report.py

import webbrowser
from urllib.parse import quote_plus


def weather_action(
    parameters: dict,
    player=None,
    session_memory=None
):
    """
    Weather report action.
    Opens a Google weather search and gives a short spoken confirmation.
    """

    city = parameters.get("city")
    time = parameters.get("time")
    if not city or not isinstance(city, str):
        msg = "Für den Wetterbericht fehlt die Stadt."
        _speak_and_log(msg, player)
        return msg

    city = city.strip()

    if not time or not isinstance(time, str):
        time = "heute"
    else:
        time = time.strip()

    search_query = f"weather in {city} {time}"
    encoded_query = quote_plus(search_query)
    url = f"https://www.google.com/search?q={encoded_query}"

    try:
        webbrowser.open(url)
    except Exception:
        msg = "Ich konnte den Browser für den Wetterbericht nicht öffnen."
        _speak_and_log(msg, player)
        return msg

    msg = f"Ich zeige das Wetter für {city}, {time}."
    _speak_and_log(msg, player)

    if session_memory:
        try:
            session_memory.set_last_search(
                query=search_query,
                response=msg
            )
        except Exception:
            pass  

    return msg


def _speak_and_log(message: str, player=None):
    if player:
        try:
            player.write_log(f"Brahma AI: {message}")
        except Exception:
            pass
