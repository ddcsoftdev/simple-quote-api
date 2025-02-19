from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from .models import Quote


class QuoteAPITestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            "test_user", "test_user@test.com", "password1234"
        )
        self.token = AccessToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        Quote.objects.create(author="John Doe", context="Quote 1").save()
        Quote.objects.create(author="Jane Doe", context="Quote 2").save()

        self.ERROR_MSGS = {
            "code": "Status Code Error:",
            "data": "Data Integrity Error:",
            "key": "Expected Key Missing Error:",
        }

    # TODO: delete if not used
    def tearDown(self):
        return super().tearDown()

    def data_integrity_check(self, response, data):
        self.assertIn("id", response, f"{self.ERROR_MSGS["key"]} id")
        self.assertIn("author", response, f"{self.ERROR_MSGS["key"]} author")
        self.assertIn("context", response, f"{self.ERROR_MSGS["key"]} context")
        self.assertIn("created_at", response, f"{self.ERROR_MSGS["key"]} created_at")
    
        self.assertEqual(
            response["id"],
            str(data.id),
            f"{self.ERROR_MSGS["data"]} id",
        )
        self.assertEqual(
            response["author"],
            data.author,
            f"{self.ERROR_MSGS["data"]} author",
        )
        self.assertEqual(
            response["context"],
            data.context,
            f"{self.ERROR_MSGS["data"]} context",
        )
        self.assertEqual(
            response["created_at"],
            data.created_at.strftime('%Y-%m-%dT%H:%M:%S.%fZ'),
            f"{self.ERROR_MSGS["data"]} created_at",
        )

    def test_get_single_quote(self):
        """Get One Quote"""
        quote = Quote.objects.first()
        url = reverse("quote-detail", args=[str(quote.id)])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200, self.ERROR_MSGS["code"])
        self.data_integrity_check(response.data, quote)

    def test_get_all_quotes(self):
        """Get All Quotes"""
        quotes = Quote.objects.all()
        url = reverse("quote-list")
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, 200, self.ERROR_MSGS["code"])
        self.assertEqual(len(response.data["results"]), len(quotes))
        for index, data in enumerate(response.data["results"]):
            self.data_integrity_check(data, quotes[index])
