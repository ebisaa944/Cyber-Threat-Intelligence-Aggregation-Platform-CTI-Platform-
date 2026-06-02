from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from .models import ThreatReport

User = get_user_model()


class ReportPermissionTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user1 = User.objects.create_user(username='user1', password='pass')
        self.user2 = User.objects.create_user(username='user2', password='pass')
        self.admin = User.objects.create_superuser(username='admin', password='pass')

        self.report1 = ThreatReport.objects.create(title='R1', summary='S1', created_by=self.user1)
        self.report2 = ThreatReport.objects.create(title='R2', summary='S2', created_by=self.user2)

    def test_user_sees_only_their_reports(self):
        self.client.login(username='user1', password='pass')
        resp = self.client.get('/api/reports/')
        self.assertEqual(resp.status_code, 200)
        data = resp.json()
        # Should only include report1
        titles = [r['title'] for r in data.get('results', data)]
        self.assertIn('R1', titles)
        self.assertNotIn('R2', titles)

    def test_owner_can_download_pdf(self):
        self.client.login(username='user1', password='pass')
        resp = self.client.get(f'/api/reports/{self.report1.id}/download_pdf/')
        self.assertEqual(resp.status_code, 200)

    def test_other_user_cannot_download(self):
        self.client.login(username='user2', password='pass')
        resp = self.client.get(f'/api/reports/{self.report1.id}/download_pdf/')
        self.assertIn(resp.status_code, (403, 404))

    def test_admin_can_download_any_report(self):
        self.client.login(username='admin', password='pass')
        resp = self.client.get(f'/api/reports/{self.report1.id}/download_pdf/')
        self.assertEqual(resp.status_code, 200)
from django.test import TestCase

# Create your tests here.
