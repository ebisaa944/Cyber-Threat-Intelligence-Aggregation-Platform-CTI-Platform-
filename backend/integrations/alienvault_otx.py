from OTXv2 import OTXv2
from datetime import datetime
from decouple import config

OTX_API_KEY = config('OTX_API_KEY')
otx = OTXv2(OTX_API_KEY)

def fetch_pulses(limit=10):
    threats = []
    iocs = []

    # getall returns a generator of pulse dictionaries
    for i, pulse in enumerate(otx.getall()):
        if i >= limit:
            break
        threat = {
            "title": pulse.get("name", "No title"),
            "description": pulse.get("description", ""),
            "source": "AlienVault OTX",
            "threat_type": "pulse",
            "severity": _map_otx_severity(pulse.get("adversary", "")),
            "external_id": pulse.get("id"),
            "published_date": _parse_otx_date(pulse.get("created")),
        }
        threats.append(threat)

        for ind in pulse.get("indicators", []):
            ioc = {
                "ioc_type": _normalize_ioc_type(ind.get("type", "")),
                "value": ind.get("indicator", ""),
                "confidence": 70,
                "source": "OTX",
                "first_seen": _parse_otx_date(pulse.get("created")),
                "last_seen": None,
                "related_threat_external_id": pulse.get("id"),
            }
            iocs.append(ioc)

    return threats, iocs

def _parse_otx_date(date_str):
    if not date_str:
        return None
    # OTX returns ISO format with 'Z' or timezone
    try:
        return datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    except:
        return None

def _map_otx_severity(adversary):
    if "apt" in adversary.lower():
        return "critical"
    return "medium"

def _normalize_ioc_type(otx_type):
    mapping = {
        "domain": "domain",
        "IPv4": "ip",
        "IPv6": "ip",
        "URL": "url",
        "FileHash-SHA256": "hash",
        "FileHash-SHA1": "hash",
        "FileHash-MD5": "hash",
        "email": "email",
    }
    return mapping.get(otx_type, "ip")