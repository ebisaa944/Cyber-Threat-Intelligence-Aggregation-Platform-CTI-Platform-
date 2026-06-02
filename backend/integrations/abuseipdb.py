import requests
from datetime import datetime
from decouple import config

API_KEY = config('ABUSEIPDB_API_KEY')
BASE_URL = "https://api.abuseipdb.com/api/v2"

def fetch_blacklist(confidence_minimum=90, limit=100):
    headers = {
        "Key": API_KEY,
        "Accept": "application/json",
    }
    params = {
        "confidenceMinimum": confidence_minimum,
        "limit": limit,
        "plaintext": "",
    }
    resp = requests.get(f"{BASE_URL}/blacklist", headers=headers, params=params)
    resp.raise_for_status()
    data = resp.json().get("data", [])

    iocs = []
    now = datetime.utcnow()
    for entry in data:
        ip = entry["ipAddress"]
        ioc = {
            "ioc_type": "ip",
            "value": ip,
            "confidence": entry.get("abuseConfidenceScore", 0),
            "source": "AbuseIPDB",
            "first_seen": now,
            "last_seen": now,
            "related_threat_external_id": "abuseipdb_batch",
        }
        iocs.append(ioc)

    threat = {
        "title": "AbuseIPDB Blacklist (high confidence)",
        "description": f"Batch of {len(iocs)} IPs with confidence >= {confidence_minimum}",
        "source": "AbuseIPDB",
        "threat_type": "blacklist",
        "severity": "high",
        "external_id": "abuseipdb_batch",
        "published_date": now,
    }
    return [threat], iocs