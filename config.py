# config.py
import os
import json
import logging

CONFIG_FILE = 'config/keywords.json'

DEFAULT_CONFIG = {
    "timestamp_patterns": [
        "\\d{1,2}\\s+(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*[,]?\\s*\\d{4}",
        "(jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\\s+\\d{1,2}[,]?\\s*\\d{4}",
        "(january|february|march|april|may|june|july|august|september|october|november|december)\\s+\\d{1,2}(?:,\\s*\\d{4})?",
        "\\d{1,2}\\s+(january|february|march|april|may|june|july|august|september|october|november|december)"
    ],
    "turtle_keywords": ["green turtle", "olive ridley", "#greenturtle", "#oliveridley", "\u06a9\u0686\u0648\u06d2"],
    "dead_keywords": ["dead", "washed up", "\u06c1\u0644\u0627\u06a9"],
    "alive_keywords": ["released", "rescued", "\u0622\u0632\u0627\u062f"],
    "species_keywords": {
        "green turtle": "Green Turtle",
        "olive ridley": "Olive Ridley",
        "leatherback": "Leatherback",
        "loggerhead": "Loggerhead",
        "hawksbill": "Hawksbill"
    },
    "interaction_keywords": {
        "stranded": "Stranded",
        "sighted": "Sighted",
        "bycatch": "Bycatch"
    },
    "location_keywords": {
        "jiwani": "Gwadar",
        "ganz": "Gwadar",
        "pishukan": "Gwadar",
        "sur bandar": "Gwadar",
        "pasni": "Gwadar",
        "ormara": "Gwadar",
        "west bay gwadar": "Gwadar",
        "east bay gwadar": "Gwadar",
        "astola": "Gwadar",
        "bandari beach": "Gwadar",
        "karachi": "Karachi",
        "sonmiani": "Lasbela"
    }
}

def ensure_config():
    os.makedirs('config', exist_ok=True)
    if not os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(DEFAULT_CONFIG, f, indent=4, ensure_ascii=False)
        logging.info("Created default keywords config.")

def load_config():
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
        return json.load(f)
