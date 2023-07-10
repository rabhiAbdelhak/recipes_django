# test for the user api

from django.test import TestCase
from django.contrib.auth import get_user_model
from django.urls import reverse

from rest_framework.test import APIClient
from rest_framework import status

CREATE_USER_URL = reverse("user:create")
TOKEN_URL = reverse("user:token")
ME_URL = reverse('user:mine')


def create_user(**params):
    # creating a user
    return get_user_model().objects.create_user(**params)


class PublicUserAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()

    def test_create_user_success(self):
        # test creating a user is successful
        payload = {
            "email": "abdelwahed@gmail.com",
            "password": "abdou1234",
            "name": "abdelwahed",
        }
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        user = get_user_model().objects.get(email=payload["email"])
        self.assertTrue(user.check_password(payload["password"]))
        self.assertNotIn("password", res.data)

    def test_email_already_existed(self):
        # test that email is already existed error works
        payload = {
            "email": "abdelwahed@gmail.com",
            "password": "abdou1234",
            "name": "abdelwahed",
        }

        create_user(**payload)
        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_password_too_short_error(self):
        # test the password is too short error works
        payload = {
            "email": "abdelwahed@gmail.com",
            "password": "pw",
            "name": "abdelwahed",
        }

        res = self.client.post(CREATE_USER_URL, payload)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

        # test that the users didnt get added to the database
        user_exists = get_user_model().objects.filter(
            email=payload["email"]).exists()
        self.assertFalse(user_exists)

    def test_user_token_creation_valid_credentials(self):
        # test for valid credentials creation
        user_details = {
            'email': 'test@gmail.com',
            'password': 'testpass123',
            'name': 'test_user'
        }
        get_user_model().objects.create_user(**user_details)

        payload = {
            'email': user_details['email'],
            'password': user_details['password']
        }
        res = self.client.post(TOKEN_URL, payload)
        self.assertIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_200_OK)

    def test_user_token_creation_bad_credentials(self):
        # test return error if error does not exist
        get_user_model().objects.create_user(email="test@gmail.com", password="goodpass")

        payload = {
            "email": "testo@testo.com",
            "password": "badpass",
        }

        res = self.client.post(TOKEN_URL, payload)
        self.assertNotIn('token', res.data)
        self.assertEqual(res.status_code, status.HTTP_400_BAD_REQUEST)

    def test_retrieve_user_unauthenticated(self):
        # test if the user unauthenticated case works well
        res = self.client.get(ME_URL)
        self.assertAlmostEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateUserAPITest(TestCase):
    # test the private user api features
    def setUp(self):
        self.user = create_user(name="test",
                                email="test@exemple.com",
                                password="1234")

        self.client = APIClient()

        res = self.client.force_authenticate(user=self.user)

    def test_retrieve_user(self):
        # test retrive user privite case
        res = self.client.get(ME_URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, {"name": "test",
                                    "email": "test@exemple.com", })

    def test_post_me_not_allowed(self):
        # test that the post method is not allowed for the profile route
        res = self.client.post(ME_URL, {})
        self.assertEqual(res.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)

    def test_update_profile_for_authentificated_user(self):
        # test that the authenticated can successffully update his profile
        info_to_update = {
            "name": "new name",
            "email": "new@exemple.com",
            "password": "newpassword"
        }

        res = self.client.patch(ME_URL, info_to_update)
        self.user.refresh_from_db()
        self.assertEqual(self.user.name, info_to_update['name'])
        self.assertTrue(self.user.check_password(info_to_update['password']))
        self.assertEqual(res.status_code, status.HTTP_200_OK)
