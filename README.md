# FlowMaster — Trading Game Platform

> **Interactive, market‑realistic trading game for education, training, and talent assessment.**
> Built in **Python** with a robust pricing engine (vanilla options, Greeks, strategy builder) and a competitive game loop.

<p align="center">
  <!-- Optional logo / banner -->
  <!-- <img src="assets/banner.png" width="720" /> -->
</p>

---

## Table of Contents

* [Overview](#overview)
* [Key Features](#key-features)
* [Architecture](#architecture)
* [Quick Start](#quick-start)

  * [Prerequisites](#prerequisites)
  * [Setup (venv / pip)](#setup-venv--pip)
  * [Setup (Poetry)](#setup-poetry)
  * [Setup (Conda / Micromamba)](#setup-conda--micromamba)
* [Usage](#usage)

  * [Run the Game Loop](#run-the-game-loop)
* [Project Structure](#project-structure)
* [Roadmap](#roadmap)
* [Contributing](#contributing)
* [License](#license)
* [Cite & Contact](#cite--contact)

---

## Overview

**FlowMaster** bridges the gap between financial theory and practice by letting users **price instruments, build strategies, and manage risk** in a **time‑pressured, gamified** environment. It is suitable for:

* **Banks / Corporates**: team‑building, onboarding, and skills assessment
* **Universities / Business Schools**: hands‑on labs, simulations, competitions
* **Students / Individuals**: learn markets, options, and risk management by doing

**Go‑to‑Market**: B2B first (licenses + workshops); then selective B2C; possible B2B2C via partners.

---

## Key Features

* **Pricing Engine:** vanilla options, Greeks, basic strategy builder
* **Game Mechanics:** time‑boxed rounds, scoring, leaderboard
* **Risk Views:** P&L vs price, delta aggregation, basic risk dashboard
* **Extensible:** modular design for adding assets (FX, Rates, Credit) and features
* **Education‑Ready:** scenarios, instructor mode, analytics (planned)

> **Status:** MVP complete for option pricing / Greeks / basic gameplay. See [Roadmap](#roadmap).

## Architecture

> The project follows a modular, scalable architecture organized under `src/trading_game/`, separating application logic, configuration pools, pricing engine, and utilities.

```
src/
└── trading_game/
    ├── app/                               # Streamlit web interface
    │   ├── webapp.py                      # Main entry point
    │   │
    │   ├── components/                    # Reusable UI components
    │   │   ├── client_chat.py             # Chat interface for client interactions
    │   │   ├── graphs.py                  # Market & P&L visualizations
    │   │   ├── metrics.py                 # P&L and risk KPIs
    │   │   ├── news_alert.py              # Market news generator
    │   │   ├── option_param_inputs.py     # Inputs for option pricing parameters
    │   │   ├── pricer_tabs.py             # Tabs for pricing tools
    │   │   ├── risk_bar.py                # Real-time risk exposure bar
    │   │   ├── sidebar_header.py          # Sidebar layout (logo, score…)
    │   │   └── trading_tabs.py            # Tabs for manual trading & options trading
    │   │
    │   ├── images/                        # Static assets (logos…)
    │   │   └── logo_vf.jpeg
    │   │
    │   ├── layouts/                       # High-level pages / screens
    │   │   ├── client_requests.py         # Client request generation panel
    │   │   ├── controls.py                # Global app controls
    │   │   ├── current_positions.py       # Current positions & P&L dashboard
    │   │   ├── main_layout.py             # Root layout orchestrating all views
    │   │   ├── market_overview.py         # Market data, shocks, asset info
    │   │   ├── pricer_tool.py             # Option pricing page
    │   │   ├── trading_delta.py           # Delta hedging interface
    │   │   └── trading_options.py         # Options trading interface
    │   │
    │   └── utils/                         # App-specific utilities
    │       ├── client_request_manager.py  # Client request logic (stateful)
    │       ├── functions.py               # Helper functions for UI
    │       ├── state_manager.py           # Streamlit session state manager
    │       └── styling.py                 # CSS & visual formatting
    │
    ├── config/                            # Static configuration & predefined pools
    │   ├── investor_pool.py               # Investor profiles and behaviours
    │   ├── maturity_config.py             # Maturity presets for options
    │   ├── request_pool.py                # Client request templates
    │   ├── settings.py                    # Global settings and constants
    │   ├── shock_pool.py                  # Market shock definitions
    │   ├── stock_pool.py                  # Underlying assets (stocks…)
    │   └── strat_pool.py                  # Predefined trading strategies
    │
    ├── core/                              # Core business logic (model-agnostic)
    │   ├── book.py                        # Portfolio object: trades, positions, P&L
    │   ├── manual_trading.py              # Trade execution engine (market/limit)
    │   ├── option_pricer.py               # Pricing models & Greeks (Black–Scholes…)
    │   └── quote_request.py               # Quote request engine (bid/ask simulation)
    │
    ├── models/                            # Domain models
    │   ├── shock.py                       # Shock structure (vol spikes, gaps…)
    │   ├── stock.py                       # Stock data model
    │   └── street.py                      # Market microstructure abstractions
    │
    └── utils/                             # Global utilities (non-UI)
        └── app_utils.py                   # Logging, seeds, helpers, formatting
                
```

**Design philosophy:**

* **Separation of concerns:** pricing, game logic, and data configuration are independent.
* **Extendability:** easily add new asset types or strategies by updating `config/` and `core/` modules.
* **Scalability:** ready for integration with web front-end (`app/webapp.py`) or external APIs.
* **Maintainability:** structured for testing and continuous deployment later.

---


## Quick Start

### Prerequisites

* macOS/Linux/Windows
* Git

### Setup (venv / pip)

```bash
# 1) Clone
git clone https://github.com/<your-org-or-user>/flowmaster.git
cd flowmaster
micromamba create -f environment.yml
```

### Setup (Poetry)

```bash
# If using Poetry
poetry install
poetry shell
```

### Setup (Conda / Micromamba)

```bash
# Using micromamba (or conda)
micromamba create -n flowmaster python=3.11 -y
micromamba activate flowmaster
```

---

## Usage

### Run the Game Loop

```bash
# streamlit run src/trading_game/app/webapp.py
```
___

## Project Structure

```text

TRADING_GAME_PROJECT/
├── __pycache__/                     # Python bytecode cache (can be ignored)
├── .gitignore                       # Git ignore rules
├── misc.xml                         # IDE (PyCharm / IntelliJ) project config
├── modules.xml                      # IDE module configuration
├── MypyPlugin.xml                   # IDE mypy plugin configuration
├── trading_game_project.iml         # IDE project file
├── vcs.xml                          # IDE VCS configuration
│
└── src/
    └── trading_game/
        ├── __pycache__/             # Package cache (ignored by Git)
        │
        ├── app/                     # Streamlit web interface
        │   ├── webapp.py            # Main application entry point
        │   │
        │   ├── components/          # Reusable UI components
        │   │   ├── __init__.py
        │   │   ├── client_chat.py
        │   │   ├── graphs.py
        │   │   ├── metrics.py
        │   │   ├── news_alert.py
        │   │   ├── option_param_inputs.py
        │   │   ├── pricer_tabs.py
        │   │   ├── risk_bar.py
        │   │   ├── sidebar_header.py
        │   │   └── trading_tabs.py
        │   │
        │   ├── images/              # Static assets (logos…)
        │   │   └── logo_vf.jpeg
        │   │
        │   ├── layouts/             # High-level pages / screens
        │   │   ├── __init__.py
        │   │   ├── client_requests.py
        │   │   ├── controls.py
        │   │   ├── current_positions.py
        │   │   ├── main_layout.py
        │   │   ├── market_overview.py
        │   │   ├── pricer_tool.py
        │   │   ├── trading_delta.py
        │   │   └── trading_options.py
        │   │
        │   └── utils/               # UI & session management helpers
        │       ├── __init__.py
        │       ├── client_request_manager.py
        │       ├── functions.py
        │       ├── state_manager.py
        │       └── styling.py
        │
        ├── config/                  # Static configuration & pools
        │   ├── __init__.py
        │   ├── investor_pool.py
        │   ├── maturity_config.py
        │   ├── request_pool.py
        │   ├── settings.py
        │   ├── shock_pool.py
        │   ├── stock_pool.py
        │   └── strat_pool.py
        │
        ├── core/                    # Core trading & pricing logic
        │   ├── __init__.py
        │   ├── book.py
        │   ├── manual_trading.py
        │   ├── option_pricer.py
        │   └── quote_request.py
        │
        ├── models/                  # Domain models
        │   ├── __init__.py
        │   ├── shock.py
        │   ├── stock.py
        │   └── street.py
        │
        └── utils/                   # Package-level utilities
            ├── __init__.py
            └── app_utils.py

```
---

## Roadmap

* V1 (Go‑to‑Market): UX polish, profiles, scoring, leaderboard
* V2: FX/Rates/Credit modules; VaR & basic risk dashboard
* V3: multiplayer tournaments; AI coach; mobile client

---

## Contributing

Contributions are welcome! Please:

1. Open an issue describing the change/bug.
2. Create a feature branch from `main`.
3. Add tests when appropriate.

---

## License

Choose a license that fits your goals. Common options:

* **Proprietary** (default for B2B): all rights reserved
* **Commercial + source‑available** (e.g., Polyform)
* **Open‑source** (MIT/Apache‑2.0) for limited modules only

---

## Cite & Contact

If you use FlowMaster in research or teaching, please cite this repository.
For partnerships, pilots, or sponsorships: **<contact@flowmaster-project.com>**
LinkedIn: **@FlowMaster** (placeholder)

---

### Maintainers

* Juliette Mary — Co-Founder & Developer
* Amandine Estève — Co-Founder & Developer
* Victor Chardain — Co-Founder & Developer

---

