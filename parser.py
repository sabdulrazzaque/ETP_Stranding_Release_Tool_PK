# parser.py
import re
import logging
import dateparser
from constants import STATUS_ALIVE, STATUS_DEAD
from config import ensure_config, load_config

ensure_config()
CONFIG = load_config()

def extract_facebook_style_timestamp(text):
    for pattern in CONFIG['timestamp_patterns']:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            parsed = dateparser.parse(match.group(0), settings={'PREFER_DATES_FROM': 'past'})
            if parsed:
                return parsed.strftime('%Y-%m-%d')
    return None

def parse_details_from_text(text):
    try:
        text_clean = re.sub(r'\s+', ' ', text.lower())
        name_match = re.search(r'^([A-Z][a-z]+(?:\s[A-Z][a-z]+)*)', text)
        account_name = name_match.group(1).strip() if name_match else None
        post_date = extract_facebook_style_timestamp(text)

        turtle_count = 1 if any(k in text_clean for k in CONFIG['turtle_keywords']) else None

        if any(k in text_clean for k in CONFIG['dead_keywords']):
            status = STATUS_DEAD
        elif any(k in text_clean for k in CONFIG['alive_keywords']):
            status = STATUS_ALIVE
        else:
            status = None

        species = None
        for k, v in CONFIG['species_keywords'].items():
            if k in text_clean:
                species = v
                break

        interaction = None
        for k, v in CONFIG['interaction_keywords'].items():
            if k in text_clean:
                interaction = v
                break

        area, district, province = None, None, None
        for town, dist in CONFIG['location_keywords'].items():
            if town in text_clean:
                area = town.title()
                district = dist
                province = "Balochistan" if dist in ["Gwadar", "Lasbela"] else "Sindh"
                break

        return {
            "account_name": account_name,
            "post_date": post_date,
            "turtle_count": turtle_count,
            "status": status,
            "species": species,
            "interaction": interaction,
            "area": area,
            "district": district,
            "province": province
        }
    except Exception as e:
        logging.error(f"Failed parsing text: {e}")
        return {}
