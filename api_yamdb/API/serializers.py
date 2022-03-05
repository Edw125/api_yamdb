from django.contrib.auth import get_user_model
from rest_framework import serializers

from django.db.models import Avg


from titles.models import Genres, Сategories, Titles

# from user.models import User

User = get_user_model()

class GenresSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genres
        fields = ('__all__')


class GenresCustomSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Genres
        fields = ('name', 'slug',)


class СategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Сategories
        fields = ('__all__')

class СategoriesCustomSerializer(serializers.ModelSerializer):

    class Meta:
        model = Сategories
        fields = ('name', 'slug',)


class TitlesSerializer(serializers.ModelSerializer):
    genre = GenresCustomSerializer(many=True, required=False)
    category = СategoriesCustomSerializer(required=False)
    avg_rating = serializers.SerializerMethodField() # это добавил ОШИБКА

    class Meta:
        model = Titles
        fields = ('name', 'year', 'category', 'rating',
                  'description', 'genre', 
                  'avg_rating',
                  )
    
    def get_avg_rating(self, ob):
        # reverse lookup on Reviews using item field
        return ob.reviews.all().aggregate(Avg('score'))['rating__avg']