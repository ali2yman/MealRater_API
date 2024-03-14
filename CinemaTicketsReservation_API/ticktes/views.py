from django.shortcuts import render
from django.http.response import JsonResponse
from .models import Guest, Movie, Reservation,Post
from rest_framework.decorators import api_view
from .serializers import GuestSerializer, MovieSerializer, ReservationSerializer,PostSerializer
from rest_framework import status, filters
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from rest_framework import generics, mixins, viewsets
from rest_framework.authentication import BasicAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from .permissions import IsAuthorOrReadOnly

# Create your views here.

# All possible Views You can do it


# 1 - without REST and no model query (FBV)
# just converting static data to a json format 
def no_rest_no_model(request):

    guests = [
    {
        'id': 1 ,
        'name' : 'omar',
        'mobile' : 4845,
    },
    {
        'id': 2 ,
        'name' : 'ali',
        'mobile' : 444845,
    }
] 
    return JsonResponse(guests,safe=False)             # set safe to False, you are indicating that you are deliberately returning a non-JSON-serializable object


# 2 - model data default django without rest
def no_rest_from_model(request):
    data = Guest.objects.all()
    response = {
        'guests' : list(data.values('name','mobile'))
    }
    return JsonResponse(response)


# List == GET
# Create == POST
# pk query == GET
# Update == PUT
# Delete destroy == DELETE

# 3 - Function based views
# 3.1 GET-POST
@api_view(['GET','POST'])
def FBV_list(request):
    # GET
    if request.method == 'GET':
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        return Response(serializer.data)
    # POST
    elif request.method == 'POST':
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)

# 3.2 GET-PUT-DELETE
@api_view(['GET','PUT','DELETE'])
def FBV_pk(request,pk):
    try:
        guest = Guest.objects.get(pk=pk)
    except Guest.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)    
    # GET
    if request.method == 'GET':
        serializer = GuestSerializer(guest )
        return Response(serializer.data)
    # PUT
    elif request.method == 'PUT':
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    # DELETE
    if request.method == 'DELETE':
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# CBV class Based views
# 4.1 List and Create == GET and POST
class CBV_List(APIView):
    def get(self,request): 
        guests = Guest.objects.all()
        serializer = GuestSerializer(guests,many=True)
        return Response(serializer.data)
    def post(self,request):
        serializer = GuestSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_201_CREATED)
        return Response(serializer.data,status=status.HTTP_400_BAD_REQUEST)


# 4.2 GET PUT DELETE Class Based View--pk
class CBV_pk(APIView):

    def get_object(self,pk):
        try:
            return Guest.objects.get(pk=pk)
        except Guest.DoesNotExist:
            raise Http404
        
    def get(self,request,pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest)
        return Response(serializer.data)
    
    def put(self,request,pk):
        guest = self.get_object(pk=pk)
        serializer = GuestSerializer(guest,data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status = status.HTTP_202_ACCEPTED)
        return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self,request,pk):
        guest = self.get_object(pk=pk)
        guest.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)



# mixins
# 5.1 mixins list
class mixins_list(mixins.ListModelMixin,mixins.CreateModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request):
        return self.list(request)
    def post(self,request):
        return self.create(request)

# 5.1 mixins get put delete
class mixins_pk(mixins.RetrieveModelMixin,mixins.UpdateModelMixin,mixins.DestroyModelMixin,generics.GenericAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

    def get(self,request,pk):
        return self.retrieve(request)
    def post(self,request,pk):
        return self.update(request)
    def post(self,request,pk):
        return self.destroy(request)



# 6 Generics 
# 6.1 Generics list
class generics_list(generics.ListCreateAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]

# 6.2  Generics get put delete
class generics_pk(generics.RetrieveDestroyAPIView):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer
    authentication_classes = [TokenAuthentication]
    # permission_classes = [IsAuthenticated]


# 7 viewsets 
# end point make all in one 
class viewsets_guest(viewsets.ModelViewSet):
    queryset = Guest.objects.all()
    serializer_class = GuestSerializer

class viewsets_movie(viewsets.ModelViewSet):
    queryset = Movie.objects.all()
    serializer_class = MovieSerializer 
    filter_backends = [filters.SearchFilter]
    search_fields = ['movie']

class viewsets_reservation(viewsets.ModelViewSet):
    queryset = Reservation.objects.all()
    serializer_class = GuestSerializer        



#8 Find movie
@api_view(['GET'])
def find_movie(request):
    movies = Movie.objects.filter(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    serializer = MovieSerializer(movies, many= True)
    return Response(serializer.data)

# 9 create new reservation
@api_view(["POST"])
def new_reservation(request):

    movie = Movie.objects.get(
        hall = request.data['hall'],
        movie = request.data['movie'],
    )
    guest = Guest()
    guest.name = request.data['name']
    guest.mobile = request.data['mobile']
    guest.save()

    reservation = Reservation()
    reservation.guest = guest
    reservation.movie = movie
    reservation.save()

    return Response(status=status.HTTP_201_CREATED)



# 10 post author editor 
class Post_pk(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = [IsAuthorOrReadOnly]
    queryset = Post.objects.all()
    serializer_class = PostSerializer








