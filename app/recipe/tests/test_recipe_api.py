from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Recipe
from decimal import Decimal
from recipe.serializers import RecipeSerializer

# function to help create a new recipe each time we need

RECIPES_URL = reverse('recipe:list')


def create_recipe(user, **params):
    defaults = {
        "title": "A simple recipe",
        "time_minute": 22,
        "price": Decimal('10.23'),
        'user': user,
        "link": "https://www.exemples.com/recipe.pdf"
    }
    defaults.update(params)

    recipe = Recipe.objects.create(**defaults)
    return recipe


class PublicRecipeAPITests(TestCase):
    # tests for features that be performed publically
    def setUp(self):
        self.client = APIClient()

    def test_auth_required(self):
        # test that the user can't see the recipes if he is not authenticated

        res = self.client.get(RECIPES_URL)
        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateRecipeApiTest(TestCase):
    # test for the features that require a user to be authenticated
    def setUp(self):
        self.client = APIClient()
        self.user = get_user_model().objects.create_user(
            email='test@exemple.com', password='testpass1234')
        self.client.force_authenticate(self.user)

    def test_retreiving_recipes(self):
        create_recipe(user=self.user)
        create_recipe(user=self.user, params={'title': 'good looking recipe'})

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().order_by('_id')
        serializer = RecipeSerializer(recipes, many=True)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_recipes_for_just_authenticated_user(self):
        second_user = get_user_model().objects.create_user(
            email="test@gmail.com", password='testpass1234')
        create_recipe(user=second_user)
        create_recipe(user=self.user, params={'title': 'good looking recipe'})

        res = self.client.get(RECIPES_URL)

        recipes = Recipe.objects.all().filter(user=self.user)
        serializer = RecipeSerializer(recipes, many=True)

        # assertion
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
