import requests
from datetime import datetime

BASE_URL = "https://urlhaus-api.abuse.ch/v1/urls/recent/"

def fetch_recent_urls(limit=100):
    payload = {
        "query": "get_urls",
        "limit": limit,
    }
    resp = requests.post(BASE_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    entries = data.get("urls", [])

    iocs = []
    now = datetime.utcnow()
    for e in entries:
        ioc = {
            "ioc_type": "url",
            "value": e.get("url", ""),
            "confidence": 80,
            "source": "URLHaus",
            "first_seen": _parse_iso_date(e.get("date_added")),
            "last_seen": None,
            "related_threat_external_id": "urlhaus_batch",
        }
        iocs.append(ioc)

    threat = {
        "title": "URLHaus Recent Malicious URLs",
        "description": f"Batch of {len(iocs)} malicious URLs",
        "source": "URLHaus",
        "threat_type": "malware_hosting",
        "severity": "high",
        "external_id": "urlhaus_batch",
        "published_date": now,
    }
    return [threat], iocs

def _parse_iso_date(date_str):
    if not date_str:
        return None
    try:
        return datetime.fromisoformat(date_str.replace(" ", "T"))
    except:
        return None