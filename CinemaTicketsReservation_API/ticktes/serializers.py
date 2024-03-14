from rest_framework import serializers
from ticktes.models import Guest,Movie,Reservation,Post


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = Movie
        fields = "__all__"


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = "__all__"        


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['pk','reservation','name','mobile']

        # pk >> we shouldn't extract pk from database(security) instead we use (uuid-slug)  but this is demo 
        # reservation >> related name we did it in models to get el reservation bta3 el guest and the related movie too


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = '__all__'

