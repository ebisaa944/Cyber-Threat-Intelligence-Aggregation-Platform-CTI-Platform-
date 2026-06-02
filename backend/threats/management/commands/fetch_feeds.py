from django.core.management.base import BaseCommand
from integrations import alienvault_otx, abuseipdb, threatfox, urlhaus, nvd
from threats.models import Threat
from iocs.models import IOC
from cves.models import CVE

class Command(BaseCommand):
    help = 'Fetch threat intelligence from all sources'

    def handle(self, *args, **options):
        self.stdout.write("Starting aggregation...")

        # AlienVault OTX
        try:
            threats, iocs = alienvault_otx.fetch_pulses()
            self._save(threats, iocs)
            self.stdout.write(self.style.SUCCESS(f"OTX: {len(threats)} threats, {len(iocs)} IOCs"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"OTX failed: {e}"))

        # AbuseIPDB
        try:
            threats, iocs = abuseipdb.fetch_blacklist()
            self._save(threats, iocs)
            self.stdout.write(self.style.SUCCESS(f"AbuseIPDB: {len(iocs)} IPs"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"AbuseIPDB failed: {e}"))

        # ThreatFox
        try:
            threats, iocs = threatfox.fetch_recent_iocs()
            self._save(threats, iocs)
            self.stdout.write(self.style.SUCCESS(f"ThreatFox: {len(iocs)} IOCs"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"ThreatFox failed: {e}"))

        # URLHaus
        try:
            threats, iocs = urlhaus.fetch_recent_urls()
            self._save(threats, iocs)
            self.stdout.write(self.style.SUCCESS(f"URLHaus: {len(iocs)} URLs"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"URLHaus failed: {e}"))

        # NVD
        try:
            cve_list = nvd.fetch_recent_cves()
            for cve_data in cve_list:
                CVE.objects.update_or_create(
                    cve_id=cve_data['cve_id'],
                    defaults=cve_data
                )
            self.stdout.write(self.style.SUCCESS(f"NVD: {len(cve_list)} CVEs"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"NVD failed: {e}"))

        self.stdout.write(self.style.SUCCESS("All feeds processed."))

    def _save(self, threats, iocs):
        for threat_data in threats:
            external_id = threat_data.pop('external_id')
            threat_obj, _ = Threat.objects.update_or_create(
                external_id=external_id,
                defaults=threat_data
            )
            for ioc_data in iocs:
                if ioc_data.get('related_threat_external_id') == external_id:
                    ioc_data.pop('related_threat_external_id')
                    ioc_data['related_threat'] = threat_obj
                    IOC.objects.update_or_create(
                        ioc_type=ioc_data['ioc_type'],
                        value=ioc_data['value'],
                        defaults=ioc_data
                    )