from django.contrib.auth.models import User
from rest_framework import serializers
from .models import Movie, ExtraInfo, Rate, Actor


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']


class ExtraInfoSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExtraInfo
        fields = ['time', 'kind']

class RateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Rate
        fields = ['id', 'descript', 'stars','movie']
        #depth = 1
    def update(self, instance, validated_data):
        instance.descript =  validated_data.get('descript', instance.descript)
        instance.stars = validated_data.get('stars', instance.descript)
        instance.save()

        return instance




class MovieSerializer(serializers.ModelSerializer):
    extra_info = ExtraInfoSerializer(many=False)
    rates = RateSerializer(many=True)
    class Meta:
        model = Movie
        fields = ['id', 'title', 'content', 'after_prem',
                  'premiere','year','imdb_rating','name','extra_info','rates']




class ActorSerializer(serializers.ModelSerializer):
    movies = MovieSerializer(many=True, read_only=True)
    class Meta:
        model = Actor
        fields = ['id','name', 'surname', 'movies']

