# serializers for recipe apis
from rest_framework import serializers
from core.models import Recipe


class RecipeSerializer(serializers.ModelSerializer):
    # serializer for recipes

    class Meta:
        model = Recipe
        fields = ['id', 'title', 'time_minute', 'price', 'description' 'link',]
        read_only_fields = ['id']
