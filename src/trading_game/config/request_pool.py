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


import random

def get_random_quote_phrase() -> str:
    """Returns a random quote request phrase"""
    return random.choice(QUOTE_REQUEST_PHRASES)