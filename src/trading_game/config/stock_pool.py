# Stock pool with realistic volatility ranges by sector
# Volatility values are annualized (typical range: 0.15 to 0.60+)

STOCK_POOL = [
    # Technology - Higher volatility (0.25-0.45)
    {"name": "Pineapple Inc.", "ticker": "PNPL US", "sector": "Technology", "init_price": 235.50, "init_vol": 0.28},
    {"name": "Macrohard Corporation", "ticker": "MHRD US", "sector": "Technology", "init_price": 425.80,
     "init_vol": 0.26},
    {"name": "GraphixCard Corp.", "ticker": "GRFX US", "sector": "Technology", "init_price": 142.75, "init_vol": 0.45},
    {"name": "FaceSpace Platforms", "ticker": "FACE US", "sector": "Technology", "init_price": 585.20,
     "init_vol": 0.38},
    {"name": "Rainforest.com Inc.", "ticker": "RNFR US", "sector": "Technology", "init_price": 218.35,
     "init_vol": 0.32},
    {"name": "SearchIt Inc.", "ticker": "SRCH US", "sector": "Technology", "init_price": 178.90, "init_vol": 0.29},
    {"name": "DataBase Corporation", "ticker": "DTBS US", "sector": "Technology", "init_price": 165.40,
     "init_vol": 0.31},
    {"name": "CloudForce Inc.", "ticker": "CLDF US", "sector": "Technology", "init_price": 312.60, "init_vol": 0.35},
    {"name": "Semiconductor Advanced", "ticker": "ASMC GY", "sector": "Technology", "init_price": 142.30,
     "init_vol": 0.38},
    {"name": "SoftwareBG GmbH", "ticker": "SWBG GY", "sector": "Technology", "init_price": 28.75, "init_vol": 0.32},
    {"name": "TuneStream AB", "ticker": "TUNE SS", "sector": "Technology", "init_price": 485.60, "init_vol": 0.41},

    # Financial Services - Moderate volatility (0.22-0.35)
    {"name": "J.P. Freeman & Co.", "ticker": "JPFR US", "sector": "Financial", "init_price": 238.75, "init_vol": 0.24},
    {"name": "Bank of the Americas", "ticker": "BOTA US", "sector": "Financial", "init_price": 45.30, "init_vol": 0.28},
    {"name": "Silver Sachs Group", "ticker": "SLVR US", "sector": "Financial", "init_price": 542.15, "init_vol": 0.27},
    {"name": "Freeman Stanley", "ticker": "FRST US", "sector": "Financial", "init_price": 118.90, "init_vol": 0.26},
    {"name": "PayCard Inc.", "ticker": "PYCD US", "sector": "Financial", "init_price": 312.40, "init_vol": 0.23},
    {"name": "ChargePlus Inc.", "ticker": "CHRG US", "sector": "Financial", "init_price": 528.65, "init_vol": 0.24},
    {"name": "Deutsche Finanz AG", "ticker": "DTFN GY", "sector": "Financial", "init_price": 15.85, "init_vol": 0.31},
    {"name": "Banque Nationale Paris", "ticker": "BNPP FP", "sector": "Financial", "init_price": 62.40,
     "init_vol": 0.28},
    {"name": "Credit Helvetica Group", "ticker": "CRHV SE", "sector": "Financial", "init_price": 2.15,
     "init_vol": 0.52},
    {"name": "BarClay Bank plc", "ticker": "BCLR LN", "sector": "Financial", "init_price": 2.35, "init_vol": 0.29},
    {"name": "SantaMaria Bank", "ticker": "STMR SM", "sector": "Financial", "init_price": 4.68, "init_vol": 0.27},
    {"name": "IGN Groep NV", "ticker": "IGNA NA", "sector": "Financial", "init_price": 15.92, "init_vol": 0.26},

    # Healthcare - Moderate volatility (0.20-0.35)
    {"name": "Jackson & Jackson", "ticker": "JJCK US", "sector": "Healthcare", "init_price": 148.25, "init_vol": 0.18},
    {"name": "GlobalHealth Group", "ticker": "GLBH US", "sector": "Healthcare", "init_price": 565.80, "init_vol": 0.22},
    {"name": "PharmaTech Inc.", "ticker": "PHRM US", "sector": "Healthcare", "init_price": 24.15, "init_vol": 0.26},
    {"name": "ModernMed Inc.", "ticker": "MMED US", "sector": "Healthcare", "init_price": 38.90, "init_vol": 0.52},
    {"name": "BioLily Co.", "ticker": "BLLY US", "sector": "Healthcare", "init_price": 895.40, "init_vol": 0.29},
    {"name": "MediCure & Co.", "ticker": "MDCR US", "sector": "Healthcare", "init_price": 98.70, "init_vol": 0.23},
    {"name": "Nova Nordique A/S", "ticker": "NVNQ DC", "sector": "Healthcare", "init_price": 485.20, "init_vol": 0.25},
    {"name": "La Roche Holding AG", "ticker": "LRCH SE", "sector": "Healthcare", "init_price": 265.30,
     "init_vol": 0.20},
    {"name": "Sanopharm SA", "ticker": "SNPH FP", "sector": "Healthcare", "init_price": 98.45, "init_vol": 0.22},
    {"name": "AstroZeneca PLC", "ticker": "AZEC LN", "sector": "Healthcare", "init_price": 125.80, "init_vol": 0.24},

    # Consumer - Variable volatility (0.20-0.50)
    {"name": "Edison Motors Inc.", "ticker": "EDIS US", "sector": "Automotive", "init_price": 342.80, "init_vol": 0.55},
    {"name": "Swoosh Athletics", "ticker": "SWSH US", "sector": "Consumer", "init_price": 72.45, "init_vol": 0.28},
    {"name": "CoffeeBeans Corp.", "ticker": "CFBN US", "sector": "Consumer", "init_price": 92.30, "init_vol": 0.27},
    {"name": "BurgerQueen Inc.", "ticker": "BRGR US", "sector": "Consumer", "init_price": 285.60, "init_vol": 0.21},
    {"name": "Pepsi-Free Company", "ticker": "PFRE US", "sector": "Consumer", "init_price": 58.75, "init_vol": 0.19},
    {"name": "Consumer & Hygiene Co.", "ticker": "CNHY US", "sector": "Consumer", "init_price": 168.20,
     "init_vol": 0.17},
    {"name": "MegaMart Inc.", "ticker": "MGMT US", "sector": "Consumer", "init_price": 95.85, "init_vol": 0.22},
    {"name": "LVHM", "ticker": "CM FP", "sector": "Consumer", "init_price": 685.40, "init_vol": 0.26},
    {"name": "Three Stripes Sport AG", "ticker": "TSTR GY", "sector": "Consumer", "init_price": 218.50,
     "init_vol": 0.30},
    {"name": "ChocoPowder SA", "ticker": "CHCP SE", "sector": "Consumer", "init_price": 92.15, "init_vol": 0.16},
    {"name": "FastFashion SA", "ticker": "FSFH SM", "sector": "Consumer", "init_price": 48.25, "init_vol": 0.24},
    {"name": "UniLever Consumer", "ticker": "UNLV LN", "sector": "Consumer", "init_price": 48.90, "init_vol": 0.18},

    # Automotive - Higher volatility (0.30-0.55)
    {"name": "VolksCar AG", "ticker": "VLKC GY", "sector": "Automotive", "init_price": 98.45, "init_vol": 0.35},
    {"name": "Bavarian Motor Works", "ticker": "BMWK GY", "sector": "Automotive", "init_price": 85.60,
     "init_vol": 0.32},
    {"name": "MegaAuto NV", "ticker": "MGAT IM", "sector": "Automotive", "init_price": 13.75, "init_vol": 0.38},
    {"name": "Reno Automobiles", "ticker": "RENO FP", "sector": "Automotive", "init_price": 42.30, "init_vol": 0.40},

    # Energy - Higher volatility (0.30-0.50)
    {"name": "XtraPower Corp.", "ticker": "XPWR US", "sector": "Energy", "init_price": 118.45, "init_vol": 0.32},
    {"name": "Petroleum Corporation", "ticker": "PTRL US", "sector": "Energy", "init_price": 155.30, "init_vol": 0.31},
    {"name": "Continental Oil", "ticker": "COIL US", "sector": "Energy", "init_price": 108.75, "init_vol": 0.38},
    {"name": "DrillTech Ltd.", "ticker": "DRLT US", "sector": "Energy", "init_price": 42.60, "init_vol": 0.42},
    {"name": "SeaShell Petroleum plc", "ticker": "SSHL LN", "sector": "Energy", "init_price": 28.95, "init_vol": 0.28},
    {"name": "Totally SE", "ticker": "TPWR FP", "sector": "Energy", "init_price": 62.80, "init_vol": 0.26},
    {"name": "Brit Petroleum Co", "ticker": "BRPT LN", "sector": "Energy", "init_price": 5.15, "init_vol": 0.30},
    {"name": "NordicOil ASA", "ticker": "NOIL NO", "sector": "Energy", "init_price": 25.40, "init_vol": 0.27},

    # Utilities - Lower volatility (0.15-0.25)
    {"name": "FutureGrid Inc.", "ticker": "FGRD US", "sector": "Utilities", "init_price": 56.90, "init_vol": 0.20},
    {"name": "PowerDuke Corp.", "ticker": "PWDK US", "sector": "Utilities", "init_price": 108.35, "init_vol": 0.18},
    {"name": "Regional Electric Co.", "ticker": "RGNL US", "sector": "Utilities", "init_price": 82.15,
     "init_vol": 0.17},
    {"name": "PowerState Inc.", "ticker": "PWST US", "sector": "Utilities", "init_price": 54.80, "init_vol": 0.19},
    {"name": "PowerOn Energy AG", "ticker": "PWON GY", "sector": "Utilities", "init_price": 12.85, "init_vol": 0.21},
    {"name": "IberElectric Utilities", "ticker": "IBER SM", "sector": "Utilities", "init_price": 13.20,
     "init_vol": 0.19},
    {"name": "NationGrid plc", "ticker": "NGRD LN", "sector": "Utilities", "init_price": 10.45, "init_vol": 0.18},

    # Industrial - Moderate volatility (0.23-0.35)
    {"name": "AeroPlane Company", "ticker": "AERO US", "sector": "Industrial", "init_price": 172.50, "init_vol": 0.42},
    {"name": "TractorPillar Inc.", "ticker": "TRCT US", "sector": "Industrial", "init_price": 385.20, "init_vol": 0.29},
    {"name": "Universal Machines", "ticker": "UNVM US", "sector": "Industrial", "init_price": 178.65, "init_vol": 0.35},
    {"name": "Industrial Solutions", "ticker": "INDS US", "sector": "Industrial", "init_price": 132.90,
     "init_vol": 0.26},
    {"name": "SkyBus Industries SE", "ticker": "SKYB FP", "sector": "Industrial", "init_price": 158.30,
     "init_vol": 0.35},
    {"name": "Siewomen's Industrie AG", "ticker": "SIEM GY", "sector": "Industrial", "init_price": 178.90,
     "init_vol": 0.28},
    {"name": "PowerSwitch Electric", "ticker": "PWSW FP", "sector": "Industrial", "init_price": 242.60,
     "init_vol": 0.26},

    # Telecommunications - Lower-moderate volatility (0.20-0.30)
    {"name": "TeleCom Inc.", "ticker": "TLCM US", "sector": "Telecom", "init_price": 22.40, "init_vol": 0.24},
    {"name": "PhoneZone Wireless", "ticker": "PHNZ US", "sector": "Telecom", "init_price": 41.85, "init_vol": 0.22},
    {"name": "CellConnect Inc.", "ticker": "CELL US", "sector": "Telecom", "init_price": 235.70, "init_vol": 0.28},
    {"name": "TeleKom AG", "ticker": "TLKM GY", "sector": "Telecom", "init_price": 24.85, "init_vol": 0.23},
    {"name": "CitrusTel SA", "ticker": "CTRS FP", "sector": "Telecom", "init_price": 10.15, "init_vol": 0.25},

    # Entertainment/Media - Higher volatility (0.30-0.45)
    {"name": "Streamflix Inc.", "ticker": "STRM US", "sector": "Entertainment", "init_price": 895.30, "init_vol": 0.41},
    {"name": "MagicKingdom Co.", "ticker": "MGKD US", "sector": "Entertainment", "init_price": 92.15, "init_vol": 0.31},
    {"name": "MediaCorp Studios", "ticker": "MDCP US", "sector": "Entertainment", "init_price": 8.25, "init_vol": 0.48},
    {"name": "MediaVision SA", "ticker": "MDVS FP", "sector": "Entertainment", "init_price": 9.85, "init_vol": 0.32},
    {"name": "SevenSat Media", "ticker": "SVST GY", "sector": "Entertainment", "init_price": 5.40, "init_vol": 0.45},
]

# Helper function to randomly select a stock
import random


def get_random_stock():
    """Returns a random stock from the pool"""
    return random.choice(STOCK_POOL)


def get_stock_by_ticker(ticker: str):
    """Returns a specific stock by ticker symbol"""
    return next((s for s in STOCK_POOL if s["ticker"] == ticker), None)


def get_stocks_by_sector(sector: str):
    """Returns all stocks from a specific sector"""
    return [s for s in STOCK_POOL if s["sector"] == sector]