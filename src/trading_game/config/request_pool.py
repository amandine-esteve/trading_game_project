# Pool of realistic quote request phrases used by traders
# These capture different styles: formal, casual, urgent, brief

QUOTE_REQUEST_PHRASES = [

    # Casual
    "Hi could I pls get a quote for",
    "Hey, can you quote me",
    "Hi, can I get a price for",
    "Hey could you pls quote",
    "Hi, looking for a quote on"

    # Brief/Direct
    "Quote pls for",
    "Price for",
    "Quote on",
    "Can you quote",
    "Looking for",
    "Need a quote on",
    "Interested in",

    # Professional/Trading Floor Style
    "What's your market on",
    "Looking at",
    "Where are you on",
    "Can you show me"
]

RESPONSE_PHRASES = {

    "buy": [
        "Mine ty",
        "Mine, thanks",
        "Mine thank you"
        "I'll buy"
        "Buy",
        "Lift",
        "Lifted",
        "Mine"
        "I'm a buyer ty",
        "That works, mine",
        "Okay mine",
        "Mine pls",
        "Mine please",
        "Buy ty",
        "Lift ty"
    ],

    "sell": [
        "Yours ty",
        "Yours, thanks",
        "Yours thank you",
        "I'll sell",
        "Sell",
        "Hit",
        "Hit it",
        "Yours",
        "I'm a seller ty",
        "That works, yours",
        "Okay yours",
        "Yours pls",
        "Yours please",
        "Hit ty",
        "Sell ty"
    ],

    "pass": [
        "Pass",
        "Pass ty",
        "Pass thanks",
        "I'll pass",
        "Nothing for now",
        "Not for me",
        "Pass for now",
        "No thanks",
        "Nty"
    ]
}


import random
from typing import Literal

def get_random_quote_phrase() -> str:
    """Returns a random quote request phrase"""
    return random.choice(QUOTE_REQUEST_PHRASES)

def get_random_response_phrase(way: Literal['buy', 'sell', 'pass']) -> str:
    """Returns a random response phrase depending on way"""
    return random.choice(RESPONSE_PHRASES[way])