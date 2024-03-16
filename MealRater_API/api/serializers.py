from rest_framework import serializers
from .models import Meal,Rating
from django.contrib.auth.models import User



class UserSerializers(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id','username','password')
        # to prevent the password to be returned we we do get request
        extra_kwargs = {'password':{'write_only':True},'required':True}


class MealSerializers(serializers.ModelSerializer):
    class Meta:
        model = Meal
        fields = ('id','title','description','no_of_ratings','avg_rating')


class RatingSerializers(serializers.ModelSerializer):
    class Meta:
        model = Rating
        fields = ('id','stars','user','meal')  



