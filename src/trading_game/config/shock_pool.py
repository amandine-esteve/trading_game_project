# Pool of market news with corresponding shock parameters by sector
# Use [STOCK_NAME] placeholder to be replaced with actual stock name

NEWS_SHOCK_POOL = {
    "Technology": [
        # Positive shocks
        {
            "news": "BREAKING: [STOCK_NAME] beats earnings expectations by 25%, raises guidance",
            "shock_type": "positive",
            "price_impact": 0.12,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
        {
            "news": "[STOCK_NAME] announces breakthrough AI chip, stock soars",
            "shock_type": "positive",
            "price_impact": 0.15,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Major tech partnership: [STOCK_NAME] signs $5B cloud deal",
            "shock_type": "positive",
            "price_impact": 0.08,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.18
        },
        {
            "news": "[STOCK_NAME] receives upgrade to 'Strong Buy' from multiple analysts",
            "shock_type": "positive",
            "price_impact": 0.06,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.20
        },
        # Negative shocks
        {
            "news": "ALERT: [STOCK_NAME] faces antitrust investigation, shares plunge",
            "shock_type": "negative",
            "price_impact": -0.14,
            "vol_spike": 2.2,
            "vol_decay_rate": 0.10
        },
        {
            "news": "[STOCK_NAME] misses revenue estimates, cuts workforce by 10%",
            "shock_type": "negative",
            "price_impact": -0.11,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.13
        },
        {
            "news": "Security breach at [STOCK_NAME] exposes millions of user accounts",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.15
        },
        {
            "news": "[STOCK_NAME] loses key product launch to competitor",
            "shock_type": "negative",
            "price_impact": -0.07,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.17
        },
    ],

    "Financial": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] reports record quarterly profits, beats estimates",
            "shock_type": "positive",
            "price_impact": 0.09,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.16
        },
        {
            "news": "Federal Reserve approves [STOCK_NAME] capital return plan",
            "shock_type": "positive",
            "price_impact": 0.07,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.18
        },
        {
            "news": "[STOCK_NAME] announces major acquisition, expands market share",
            "shock_type": "positive",
            "price_impact": 0.11,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.14
        },
        {
            "news": "Strong trading revenues lift [STOCK_NAME] earnings",
            "shock_type": "positive",
            "price_impact": 0.06,
            "vol_spike": 1.2,
            "vol_decay_rate": 0.20
        },
        # Negative shocks
        {
            "news": "BREAKING: [STOCK_NAME] under investigation for fraud allegations",
            "shock_type": "negative",
            "price_impact": -0.16,
            "vol_spike": 2.5,
            "vol_decay_rate": 0.08
        },
        {
            "news": "[STOCK_NAME] faces $2B fine for regulatory violations",
            "shock_type": "negative",
            "price_impact": -0.12,
            "vol_spike": 2.0,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Credit rating downgrade hits [STOCK_NAME] hard",
            "shock_type": "negative",
            "price_impact": -0.10,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] announces higher-than-expected loan losses",
            "shock_type": "negative",
            "price_impact": -0.08,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.16
        },
    ],

    "Healthcare": [
        # Positive shocks
        {
            "news": "FDA fast-tracks [STOCK_NAME]'s breakthrough cancer drug",
            "shock_type": "positive",
            "price_impact": 0.18,
            "vol_spike": 2.0,
            "vol_decay_rate": 0.11
        },
        {
            "news": "[STOCK_NAME] Phase 3 trial shows 90% efficacy, shares surge",
            "shock_type": "positive",
            "price_impact": 0.22,
            "vol_spike": 2.3,
            "vol_decay_rate": 0.10
        },
        {
            "news": "Major insurance deal: [STOCK_NAME] secures nationwide coverage",
            "shock_type": "positive",
            "price_impact": 0.10,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.15
        },
        {
            "news": "[STOCK_NAME] receives FDA approval ahead of schedule",
            "shock_type": "positive",
            "price_impact": 0.14,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.13
        },
        # Negative shocks
        {
            "news": "ALERT: FDA halts [STOCK_NAME] drug trial over safety concerns",
            "shock_type": "negative",
            "price_impact": -0.20,
            "vol_spike": 2.8,
            "vol_decay_rate": 0.09
        },
        {
            "news": "[STOCK_NAME] drug fails to meet primary endpoint in trial",
            "shock_type": "negative",
            "price_impact": -0.17,
            "vol_spike": 2.4,
            "vol_decay_rate": 0.10
        },
        {
            "news": "Patent loss: [STOCK_NAME] faces generic competition",
            "shock_type": "negative",
            "price_impact": -0.13,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.12
        },
        {
            "news": "[STOCK_NAME] recalls product amid contamination fears",
            "shock_type": "negative",
            "price_impact": -0.11,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.14
        },
    ],

    "Consumer": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] holiday sales surge 30% above expectations",
            "shock_type": "positive",
            "price_impact": 0.11,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.14
        },
        {
            "news": "Viral product launch sends [STOCK_NAME] shares soaring",
            "shock_type": "positive",
            "price_impact": 0.13,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.13
        },
        {
            "news": "[STOCK_NAME] expands to emerging markets, raises outlook",
            "shock_type": "positive",
            "price_impact": 0.08,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.16
        },
        {
            "news": "Strong brand momentum: [STOCK_NAME] gains market share",
            "shock_type": "positive",
            "price_impact": 0.07,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.18
        },
        # Negative shocks
        {
            "news": "[STOCK_NAME] faces boycott over labor practices",
            "shock_type": "negative",
            "price_impact": -0.12,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Supply chain crisis hits [STOCK_NAME] hard, margins compress",
            "shock_type": "negative",
            "price_impact": -0.10,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] warns of weak consumer demand, cuts guidance",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
        {
            "news": "Product recall: [STOCK_NAME] pulls items from shelves",
            "shock_type": "negative",
            "price_impact": -0.08,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.16
        },
    ],

    "Automotive": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] unveils revolutionary EV with 1000-mile range",
            "shock_type": "positive",
            "price_impact": 0.16,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Record deliveries: [STOCK_NAME] beats quarterly targets",
            "shock_type": "positive",
            "price_impact": 0.12,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] secures massive government contract",
            "shock_type": "positive",
            "price_impact": 0.10,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.15
        },
        {
            "news": "Partnership announced: [STOCK_NAME] teams with tech giant",
            "shock_type": "positive",
            "price_impact": 0.09,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.16
        },
        # Negative shocks
        {
            "news": "RECALL: [STOCK_NAME] recalls 500K vehicles over safety defect",
            "shock_type": "negative",
            "price_impact": -0.15,
            "vol_spike": 2.2,
            "vol_decay_rate": 0.11
        },
        {
            "news": "[STOCK_NAME] production halted due to parts shortage",
            "shock_type": "negative",
            "price_impact": -0.13,
            "vol_spike": 2.0,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Quality issues plague [STOCK_NAME] new model launch",
            "shock_type": "negative",
            "price_impact": -0.11,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.13
        },
        {
            "news": "[STOCK_NAME] misses delivery targets, shares slide",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
    ],

    "Energy": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] discovers major new oil field, reserves jump",
            "shock_type": "positive",
            "price_impact": 0.14,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.13
        },
        {
            "news": "Oil prices surge 15%, lifting [STOCK_NAME] outlook",
            "shock_type": "positive",
            "price_impact": 0.11,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] announces record production levels",
            "shock_type": "positive",
            "price_impact": 0.09,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.16
        },
        {
            "news": "Major dividend increase announced by [STOCK_NAME]",
            "shock_type": "positive",
            "price_impact": 0.07,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.18
        },
        # Negative shocks
        {
            "news": "BREAKING: Environmental disaster at [STOCK_NAME] facility",
            "shock_type": "negative",
            "price_impact": -0.18,
            "vol_spike": 2.6,
            "vol_decay_rate": 0.09
        },
        {
            "news": "Oil prices crash 20%, [STOCK_NAME] cuts spending",
            "shock_type": "negative",
            "price_impact": -0.15,
            "vol_spike": 2.3,
            "vol_decay_rate": 0.10
        },
        {
            "news": "[STOCK_NAME] project cancelled, $3B writedown expected",
            "shock_type": "negative",
            "price_impact": -0.12,
            "vol_spike": 2.0,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Refinery fire: [STOCK_NAME] operations disrupted",
            "shock_type": "negative",
            "price_impact": -0.10,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.14
        },
    ],

    "Utilities": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] wins approval for rate increase",
            "shock_type": "positive",
            "price_impact": 0.06,
            "vol_spike": 1.2,
            "vol_decay_rate": 0.20
        },
        {
            "news": "Green energy transition: [STOCK_NAME] secures major funding",
            "shock_type": "positive",
            "price_impact": 0.08,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.18
        },
        {
            "news": "[STOCK_NAME] announces strong earnings, raises dividend",
            "shock_type": "positive",
            "price_impact": 0.05,
            "vol_spike": 1.2,
            "vol_decay_rate": 0.22
        },
        {
            "news": "Renewable energy deal boosts [STOCK_NAME] outlook",
            "shock_type": "positive",
            "price_impact": 0.07,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.19
        },
        # Negative shocks
        {
            "news": "ALERT: Major power outage at [STOCK_NAME] facilities",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.14
        },
        {
            "news": "Regulators reject [STOCK_NAME] rate hike request",
            "shock_type": "negative",
            "price_impact": -0.08,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.16
        },
        {
            "news": "[STOCK_NAME] faces costly infrastructure upgrade mandate",
            "shock_type": "negative",
            "price_impact": -0.07,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.17
        },
        {
            "news": "Weather damage forces [STOCK_NAME] plant shutdown",
            "shock_type": "negative",
            "price_impact": -0.06,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.18
        },
    ],

    "Industrial": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] lands $10B defense contract",
            "shock_type": "positive",
            "price_impact": 0.13,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.13
        },
        {
            "news": "Strong manufacturing data lifts [STOCK_NAME]",
            "shock_type": "positive",
            "price_impact": 0.09,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.16
        },
        {
            "news": "[STOCK_NAME] beats on margins, operational efficiency improves",
            "shock_type": "positive",
            "price_impact": 0.08,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.17
        },
        {
            "news": "Order backlog surges at [STOCK_NAME]",
            "shock_type": "positive",
            "price_impact": 0.10,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.15
        },
        # Negative shocks
        {
            "news": "[STOCK_NAME] issues profit warning on weak demand",
            "shock_type": "negative",
            "price_impact": -0.12,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Strike action disrupts [STOCK_NAME] production",
            "shock_type": "negative",
            "price_impact": -0.10,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] factory accident raises safety concerns",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
        {
            "news": "Raw material costs squeeze [STOCK_NAME] margins",
            "shock_type": "negative",
            "price_impact": -0.08,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.16
        },
    ],

    "Telecom": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] wins 5G spectrum auction, shares rally",
            "shock_type": "positive",
            "price_impact": 0.10,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.15
        },
        {
            "news": "Subscriber growth beats estimates at [STOCK_NAME]",
            "shock_type": "positive",
            "price_impact": 0.08,
            "vol_spike": 1.3,
            "vol_decay_rate": 0.17
        },
        {
            "news": "[STOCK_NAME] announces major network expansion",
            "shock_type": "positive",
            "price_impact": 0.07,
            "vol_spike": 1.2,
            "vol_decay_rate": 0.18
        },
        {
            "news": "Merger approved: [STOCK_NAME] deal gets regulatory green light",
            "shock_type": "positive",
            "price_impact": 0.11,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.14
        },
        # Negative shocks
        {
            "news": "BREAKING: Major network outage at [STOCK_NAME]",
            "shock_type": "negative",
            "price_impact": -0.11,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.13
        },
        {
            "news": "[STOCK_NAME] loses subscribers amid fierce competition",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
        {
            "news": "Regulators block [STOCK_NAME] merger on antitrust grounds",
            "shock_type": "negative",
            "price_impact": -0.13,
            "vol_spike": 2.0,
            "vol_decay_rate": 0.12
        },
        {
            "news": "[STOCK_NAME] cuts dividend, cites infrastructure costs",
            "shock_type": "negative",
            "price_impact": -0.08,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.16
        },
    ],

    "Entertainment": [
        # Positive shocks
        {
            "news": "[STOCK_NAME] streaming service hits record subscriber numbers",
            "shock_type": "positive",
            "price_impact": 0.15,
            "vol_spike": 1.8,
            "vol_decay_rate": 0.12
        },
        {
            "news": "Blockbuster releases drive [STOCK_NAME] box office success",
            "shock_type": "positive",
            "price_impact": 0.12,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.14
        },
        {
            "news": "[STOCK_NAME] announces major content deal with top creators",
            "shock_type": "positive",
            "price_impact": 0.10,
            "vol_spike": 1.5,
            "vol_decay_rate": 0.15
        },
        {
            "news": "International expansion pays off for [STOCK_NAME]",
            "shock_type": "positive",
            "price_impact": 0.09,
            "vol_spike": 1.4,
            "vol_decay_rate": 0.16
        },
        # Negative shocks
        {
            "news": "[STOCK_NAME] loses streaming wars, subscribers plunge",
            "shock_type": "negative",
            "price_impact": -0.16,
            "vol_spike": 2.3,
            "vol_decay_rate": 0.11
        },
        {
            "news": "Content costs spiral at [STOCK_NAME], margins pressured",
            "shock_type": "negative",
            "price_impact": -0.12,
            "vol_spike": 1.9,
            "vol_decay_rate": 0.13
        },
        {
            "news": "[STOCK_NAME] faces backlash over controversial content",
            "shock_type": "negative",
            "price_impact": -0.10,
            "vol_spike": 1.7,
            "vol_decay_rate": 0.14
        },
        {
            "news": "Advertising revenue misses at [STOCK_NAME]",
            "shock_type": "negative",
            "price_impact": -0.09,
            "vol_spike": 1.6,
            "vol_decay_rate": 0.15
        },
    ],
}

# Helper functions
import random


def get_random_news_for_sector(sector: str) -> dict:
    """Returns a random news item for the given sector"""
    if sector not in NEWS_SHOCK_POOL:
        raise ValueError(f"Sector '{sector}' not found in news pool")
    return random.choice(NEWS_SHOCK_POOL[sector])


def get_news_by_type(sector: str, shock_type: str) -> dict:
    """Returns a random news item of specific type (positive/negative) for sector"""
    sector_news = NEWS_SHOCK_POOL.get(sector, [])
    filtered = [n for n in sector_news if n["shock_type"] == shock_type]
    if not filtered:
        raise ValueError(f"No {shock_type} news found for sector '{sector}'")
    return random.choice(filtered)


def format_news(news_dict: dict, stock_name: str) -> dict:
    """Replace [STOCK_NAME] placeholder with actual stock name"""
    formatted = news_dict.copy()
    formatted["news"] = news_dict["news"].replace("[STOCK_NAME]", stock_name)
    return formatted

