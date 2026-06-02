import requests
from datetime import datetime, timedelta, timezone
from decouple import config

NVD_API_KEY = config('NVD_API_KEY', default=None)
BASE_URL = "https://services.nvd.nist.gov/rest/json/cves/2.0"

def fetch_recent_cves(hours=24):
    now = datetime.now(timezone.utc)
    start = now - timedelta(hours=hours)

    params = {
        "pubStartDate": start.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "pubEndDate": now.strftime("%Y-%m-%dT%H:%M:%S.000"),
        "resultsPerPage": 50,
        "startIndex": 0,
    }
    headers = {}
    if NVD_API_KEY:
        headers["apiKey"] = NVD_API_KEY

    cve_list = []
    while True:
        resp = requests.get(BASE_URL, headers=headers, params=params)
        resp.raise_for_status()
        data = resp.json()
        vulns = data.get("vulnerabilities", [])

        for vuln in vulns:
            cve_item = vuln.get("cve", {})
            # CVSS v3.1
            cvss_info = {}
            for metric_version in ["cvssMetricV31", "cvssMetricV30", "cvssMetricV2"]:
                metrics = cve_item.get("metrics", {}).get(metric_version, [])
                if metrics:
                    cvss = metrics[0].get("cvssData", {})
                    cvss_info = {
                        "cvss_score": cvss.get("baseScore"),
                        "severity": cvss.get("baseSeverity", "").upper(),
                    }
                    break

            pub_date = None
            if cve_item.get("published"):
                pub_date = datetime.fromisoformat(cve_item["published"].replace("Z", "+00:00"))

            cve_entry = {
                "cve_id": cve_item.get("id", ""),
                "description": cve_item.get("descriptions", [{}])[0].get("value", ""),
                "cvss_score": cvss_info.get("cvss_score"),
                "severity": cvss_info.get("severity", ""),
                "published_date": pub_date,
                "exploit_available": _check_exploit_refs(cve_item),
            }
            cve_list.append(cve_entry)

        total_results = data.get("totalResults", 0)
        params["startIndex"] += params["resultsPerPage"]
        if params["startIndex"] >= total_results:
            break

    return cve_list

def _check_exploit_refs(cve_item):
    refs = cve_item.get("references", [])
    for ref in refs:
        if "exploit" in [tag.lower() for tag in ref.get("tags", [])]:
            return True
    return False