import os
import re
import json
from datetime import date, datetime, timedelta

import numpy as np
import pandas as pd
import requests
import streamlit as st


# ── Persistent station database (Polymarket-verified) ────────────────────────
STATIONS_DB_PATH = os.path.join(os.path.dirname(__file__), "polymarket_stations.json")


@st.cache_resource
def load_stations_db() -> dict:
    """Load the verified Polymarket stations DB committed to the repo."""
    try:
        with open(STATIONS_DB_PATH) as f:
            data = json.load(f)
        return data.get("stations", {})
    except FileNotFoundError:
        return {}
    except Exception:
        return {}


def stations_by_alias() -> dict:
    """Build a lookup: alias → station_info from the JSON DB."""
    db = load_stations_db()
    out = {}
    for icao, info in db.items():
        for alias in info.get("polymarket_aliases", []):
            out[alias.lower()] = {
                "icao": icao,
                "name": f"{info.get('city','')} — {info.get('name','')}",
            }
        out[icao.lower()] = {
            "icao": icao,
            "name": f"{info.get('city','')} — {info.get('name','')}",
        }
    return out
