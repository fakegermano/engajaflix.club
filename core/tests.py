from django.test import TestCase
from django.urls import reverse

class IndexViewTestCase(TestCase):
    def setUp(self) -> None:        
        self.url = reverse("index")
        return super().setUp()
    
    def test_view_exists(self):
        resp = self.client.get(self.url)
        self.assertIs(resp.status_code, 200)

    def test_view_mentions_engajaflix(self):
        resp = self.client.get(self.url)
        self.assertIn("engajaflix", resp.content.decode())

    def test_view_has_banner_section(self):
        resp = self.client.get(self.url)
        self.assertIn('<section id="banner">', resp.content.decode())

    def test_view_has_logo(self):
        resp = self.client.get(self.url)
        self.assertIn('logo.png', resp.content.decode())

    def test_view_has_reserve_button(self):
        resp = self.client.get(self.url)
        self.assertIn("Reserve sua vaga", resp.content.decode())

    def test_view_reserve_button_posts(self):
        resp = self.client.get(self.url)
        self.assertIn(f'<button id="reserve" hx-post="{reverse("reserve")}"', resp.content.decode())
        