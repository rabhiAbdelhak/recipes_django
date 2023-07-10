# tests for models

from django.test import TestCase
from django.contrib.auth import get_user_model
from decimal import Decimal
from core.models import Recipe


class ModelTests(TestCase):
    # test models.

    def test_create_user_with_email_success(self):
        # test creating a user and email is successful
        email = 'test@exemple.com'
        password = 'testpassword'
        user = get_user_model().objects.create_user(email=email, password=password,)

        self.assertEqual(user.email, email)
        self.assertTrue(user.check_password(password))

    def test_new_email_normalized(self):
        # test email is normalized for new users.

        sample_emails = [
            ['test1@EXEMPLE.com', 'test1@exemple.com'],
            ['Test2@Exemple.com', 'Test2@exemple.com'],
            ['TEST3@Exemple.com', 'TEST3@exemple.com'],
            ['test4@Exemple.com', 'test4@exemple.com'],
        ]

        for email, expected in sample_emails:
            user = get_user_model().objects.create_user(email, 'sample123')
            self.assertEqual(user.email, expected)

    def test_new_user_without_email_raises_error(self):
        # test that creating a user without email raises a ValueError
        with self.assertRaises(ValueError):
            get_user_model().objects.create_user('', 'test123')

    def test_create_super_user(self):
        # testing super user creation
        user = get_user_model().objects.create_superuser(
            'email@exemple.com',
            'test1234'
        )

        self.assertTrue(user.is_superuser)
        self.assertTrue(user.is_staff)

    def test_recipe_create_model(self):
        user_info = {
            "name": 'test',
            "email": 'test@gmail.com',
            "password": "testpass123"
        }
        user = get_user_model().objects.create_user(**user_info)
        new_recipe = {
            'title': 'Simple new recipe',
            'time_minute': 22,
            'price': Decimal('5.26'),
            'user': user
        }
        recipe = Recipe.objects.create(**new_recipe)

        self.assertEqual(str(recipe), recipe.title)
