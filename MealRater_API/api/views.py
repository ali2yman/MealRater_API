from django.shortcuts import render
from rest_framework import viewsets,status,request
from .models import Meal,Rating
from .serializers import MealSerializers,RatingSerializers,UserSerializers
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import AllowAny,IsAuthenticated,IsAdminUser,IsAuthenticatedOrReadOnly
from rest_framework.authtoken.models import Token

# Create your views here.



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    # authentication_classes = (TokenAuthentication,)
    permission_classes = (AllowAny,)
# to create and responde to the user with it's token 
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        token, created = Token.objects.get_or_create(user=serializer.instance)
        return Response({
                    'token': token.key, 
                    }, 
        status=status.HTTP_201_CREATED)
        
    def list(self, request, *args, **kwargs):
        response = {'message': 'You cant create rating like that'}
        return Response(response, status=status.HTTP_400_BAD_REQUEST)




class MealViewSet(viewsets.ModelViewSet):
    queryset = Meal.objects.all()
    serializer_class = MealSerializers

    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)


    @action(detail=True,methods=['post'])   # for ad-hoc function you need to create and accsess
    def rate_meal(self,request,pk=None):
        if 'stars' in request.data:
            '''
            Create or update
            '''
            meal = Meal.objects.get(id=pk)
            stars = request.data['stars']
            # username = request.data['username']
            # user = User.objects.get(username=username)
            user = request.user 
            try:
                # update
                rating = Rating.objects.get(user=user.id,meal=meal.id)    # this is an given specific rate 
                rating.stars = stars
                rating.save()
                serializer = RatingSerializers(rating,many=False)
                json={
                    'message':"Meal Rate Updated",
                    'result':serializer.data
                } 
                return Response(json,status=status.HTTP_400_BAD_REQUEST)
            except:
                # create if the rate is not existed 
                rating = Rating.objects.create(stars=stars,meal=meal,user=user)
                serializer = RatingSerializers(rating,many=False)
                json={
                    'message':"Meal Rate Created",
                    'result':serializer.data
                } 
                return Response(json,status=status.HTTP_200_OK)
            
        else:
            json = {
                'message': 'stars not provided'
            }
            return Response(json , status=status.HTTP_400_BAD_REQUEST)





class RatingViewSet(viewsets.ModelViewSet):
    queryset = Rating.objects.all()
    serializer_class = RatingSerializers

    # to make the rating process to Authontecated users 
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)

    # we made the update and create in mealviewset and we need to stop the create and update(exist by defult in viewset) here to prevent user to make it here so we will override it 
    def update(self, request, *args, **kwargs):
        response = {
            'message': 'This is not how you should create - update rating',
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        response = {
            'message': 'This is not how you should create - update rating',
        }
        return Response(response,status=status.HTTP_400_BAD_REQUEST)        









