from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import AccessToken
from rest_framework.test import APIClient
from django.urls import reverse
from django.test import TestCase
from .models import Quote
import uuid


class QuoteAPITestCase(TestCase):

    def setUp(self):
        self.user = User.objects.create_user(
            "test_user", "test_user@test.com", "password1234"
        )
        self.token = AccessToken.for_user(self.user)
        self.client = APIClient()
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {self.token}")

        Quote.objects.create(author="John Doe", content="Quote 1")
        Quote.objects.create(author="Jane Doe", content="Quote 2")

        self.ERROR_MSGS = {
            "code": "Status Code Error.",
            "content": "Data Content Integrity Error:",
            "struct": "Data Structure Integrity Error:",
            "missing": "Data Missing:",
        }

    def test_get_single_quote(self):
        """Get One Quote"""
        quote = Quote.objects.first()
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
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

    def test_get_random_quote(self):
        """Get Random Quote"""
        quotes = Quote.objects.all()
        url = reverse("quote-random")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200, self.ERROR_MSGS["code"])
        self.assertIn("id", response.data, f"{self.ERROR_MSGS["struct"]} id")

        quote = quotes.filter(id=response.data["id"]).first()
        self.data_integrity_check(response.data, quote)

    def test_create_quote(self):
        """Create a Quote"""
        url = reverse("quote-list")
        body = {"author": "Teresa Doe", "content": "Quote 3"}
        response = self.client.post(url, body)

        self.assertEqual(response.status_code, 201, self.ERROR_MSGS["code"])
        quote = Quote.objects.filter(
            author=body["author"], content=body["content"]
        ).first()
        self.data_integrity_check(response.data, quote)

    def test_update_quote(self):
        """Update a Quote"""
        quote = Quote.objects.create(author="Teresa Doe", content="Original Quote")
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
        body = {"author": "Marcus Doe", "content": "Modified Quote"}
        response = self.client.put(url, body)

        self.assertEqual(response.status_code, 200, self.ERROR_MSGS["code"])
        quote.refresh_from_db()
        self.data_integrity_check(response.data, quote)

    def test_delete_quote(self):
        """Delete a Quote"""
        quote = Quote.objects.create(author="Max Doe", content="Quote 4")
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 204, self.ERROR_MSGS["code"])
        deleted_quote = Quote.objects.filter(id=quote.id).first()
        self.assertIsNone(deleted_quote, "Register not deleted on DELETE Request")

    def test_create_quote_unauth(self):
        """Create a Quote Unauthorized"""
        self.client.credentials()

        url = reverse("quote-list")
        body = {"author": "Teresa Doe", "content": "Quote 3"}
        response = self.client.post(url, body)

        self.assertEqual(response.status_code, 401, self.ERROR_MSGS["code"])

    def test_update_quote_unauth(self):
        """Update a Quote Unauthorized"""
        self.client.credentials()

        quote = Quote.objects.create(author="Teresa Doe", content="Original Quote")
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
        body = {"author": "Marcus Doe", "content": "Modified Quote"}
        response = self.client.put(url, body)

        self.assertEqual(response.status_code, 401, self.ERROR_MSGS["code"])

    def test_delete_quote_unauth(self):
        """Delete a Quote Unauthorized"""
        self.client.credentials()

        quote = Quote.objects.create(author="Max Doe", content="Quote 4")
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, 401, self.ERROR_MSGS["code"])

    def test_get_quote_not_found(self):
        """Get a Quote that does not exist"""
        wrong_id = str(uuid.uuid4())
        url = reverse("quote-detail", kwargs={"pk": str(wrong_id)})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404, self.ERROR_MSGS["code"])

    def test_update_quote_not_found(self):
        """Update a Quote that does not exist"""
        wrong_id = str(uuid.uuid4())
        url = reverse("quote-detail", kwargs={"pk": str(wrong_id)})
        body = {"author": "Marcus Doe", "content": "Modified Quote"}
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 404, self.ERROR_MSGS["code"])

    def test_delete_quote_not_found(self):
        """Delete a Quote that does not exist"""
        wrong_id = str(uuid.uuid4())
        url = reverse("quote-detail", kwargs={"pk": str(wrong_id)})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, 404, self.ERROR_MSGS["code"])

    def test_create_quote_invalid_body(self):
        """Create a Quote with invalid body"""
        url = reverse("quote-list")
        body = {"data": "Teresa Doe", "content": "Quote 3"}
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400, self.ERROR_MSGS["code"])

    def test_create_quote_incomplete_body(self):
        """Create a Quote with incomplete body"""
        url = reverse("quote-list")
        body = {"content": "Quote 3"}
        response = self.client.post(url, body)
        self.assertEqual(response.status_code, 400, self.ERROR_MSGS["code"])

    def test_update_quote_id(self):
        """Update a Quote's id"""
        quote = Quote.objects.create(author="Teresa Doe", content="Original Quote")
        url = reverse("quote-detail", kwargs={"pk": str(quote.id)})
        body = {"id": str(uuid.uuid4()), "author": "Ana", "content": "Quote"}
        response = self.client.put(url, body)
        self.assertEqual(response.status_code, 400, self.ERROR_MSGS["code"])

    def data_integrity_check(self, response, reference):
        self.assertIsNotNone(response, f"{self.ERROR_MSGS["missing"]} response")
        self.assertIsNotNone(reference, f"{self.ERROR_MSGS["missing"]} reference")

        self.assertIn("id", response, f"{self.ERROR_MSGS["struct"]} id")
        self.assertIn("author", response, f"{self.ERROR_MSGS["struct"]} author")
        self.assertIn("content", response, f"{self.ERROR_MSGS["struct"]} content")
        self.assertIn("created_at", response, f"{self.ERROR_MSGS["struct"]} created_at")

        self.assertEqual(
            response["id"],
            str(reference.id),
            f"{self.ERROR_MSGS["content"]} id",
        )
        self.assertEqual(
            response["author"],
            reference.author,
            f"{self.ERROR_MSGS["content"]} author",
        )
        self.assertEqual(
            response["content"],
            reference.content,
            f"{self.ERROR_MSGS["content"]} content",
        )
        self.assertEqual(
            response["created_at"],
            reference.created_at.strftime("%Y-%m-%dT%H:%M:%S.%fZ"),
            f"{self.ERROR_MSGS["content"]} created_at",
        )
