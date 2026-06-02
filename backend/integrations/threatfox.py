import requests
from datetime import datetime

BASE_URL = "https://threatfox-api.abuse.ch/api/v1/"

def fetch_recent_iocs(limit=200):
    payload = {
        "query": "get_iocs",
        "limit": limit,
    }
    resp = requests.post(BASE_URL, json=payload, timeout=30)
    resp.raise_for_status()
    data = resp.json()
    entries = data.get("data", [])

    iocs = []
    now = datetime.utcnow()
    for e in entries:
        ioc_type = _map_type(e.get("ioc_type", ""))
        if not ioc_type:
            continue
        ioc = {
            "ioc_type": ioc_type,
            "value": e.get("ioc_value", ""),
            "confidence": int(e.get("threat_score", 50)),
            "source": "ThreatFox",
            "first_seen": _parse_iso_date(e.get("first_seen_utc")),
            "last_seen": _parse_iso_date(e.get("last_seen_utc")),
            "related_threat_external_id": "threatfox_batch",
        }
        iocs.append(ioc)

    threat = {
        "title": "ThreatFox Recent IOCs",
        "description": f"Batch of {len(iocs)} IOCs from ThreatFox",
        "source": "ThreatFox",
        "threat_type": "aggregated",
        "severity": "medium",
        "external_id": "threatfox_batch",
        "published_date": now,
    }
    return [threat], iocs

def _map_type(tfox_type):
    mapping = {
        "ip": "ip",
        "domain": "domain",
        "url": "url",
        "sha256": "hash",
        "sha1": "hash",
        "md5": "hash",
    }
    return mapping.get(tfox_type.lower())

def _parse_iso_date(date_str):
    if not date_str:
        return None
    try:
        # ThreatFox may return "2025-01-01 12:00:00" or ISO format
        return datetime.fromisoformat(date_str.replace(" ", "T"))
    except:
        return None