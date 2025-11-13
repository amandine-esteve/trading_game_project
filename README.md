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
  trading_game/
    app/
      webapp.py            # Web interface

    config/
      __init__.py          # Configuration package initializer
      investor_pool.py     # Definitions for investors profiles
      settings.py          # Global configuration and constants
      stock_pool.py        # Available underlyings (stocks...)
      strat_pool.py        # Predefined strategy generator (call spreads, straddles, butterflies...)

    core/
      __init__.py          # Core package initializer
      book.py              # Portfolio object, P&L and trade tracking
      manual_trading.py    # Trading engine: order classes (market, limit), execution logic, and strategy handling
      market.py            # Market model: Stock class with stochastic price evolution
      option_pricer.py     # Option pricing models (e.g., Black-Scholes, Greeks)
      street.py            # Market interaction engine: investor profiles, quote requests, bid/ask simulation, chat-like flow

    utils/
      __init__.py          # Utility helpers (I/O, math, visualization)

.gitignore                 
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
pip install -r requirements.txt
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
.
├─ .idea/                     # IDE configuration files (PyCharm / IntelliJ)
│  ├─ inspectionProfiles/
│  ├─ misc.xml
│  ├─ modules.xml
│  ├─ trading_game_project.iml
│  └─ vcs.xml
│
├─ src/
│  └─ trading_game/
│     ├─ app/                 # Streamlit or FastAPI web interface
│     │   └─ webapp.py
│     │
│     ├─ config/              # Settings, investor pools, stock and strategy definitions
│     │   ├─ __init__.py
│     │   ├─ investor_pool.py
│     │   ├─ settings.py
│     │   ├─ stock_pool.py
│     │   └─ strat_pool.py
│     │
│     ├─ core/                # Core logic: trading, pricing, market simulation, orchestration
│     │   ├─ __init__.py
│     │   ├─ book.py
│     │   ├─ manual_trading.py
│     │   ├─ market.py
│     │   ├─ option_pricer.py
│     │   └─ street.py
│     │
│     └─ utils/               # Utility functions and helpers
│         └─ __init__.py
│
├─ .gitignore                 # Git ignore rules
├─ environment.yml            # Conda or micromamba environment definition
├─ poetry.lock                # Poetry dependency lock file
├─ pyproject.toml             # Project configuration and build system
└─ README.md                  # Documentation
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

