from django.contrib.auth.models import User
from rest_framework import viewsets, filters
from rest_framework.response import Response
from api.serializers import UserSerializer
from .models import Movie, Rate, Actor
from .serializers import MovieSerializer, RateSerializer, ActorSerializer
from django.http.response import HttpResponseNotAllowed
from rest_framework.decorators import action
from rest_framework.pagination import PageNumberPagination
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated, DjangoModelPermissions


class LargeResultsSetPagination(PageNumberPagination):
    page_size = 5
    page_size_query_param = 'page_size'
    max_page_size = 10



class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by('-date_joined')
    serializer_class = UserSerializer
    serializer_class = UserSerializer

class MovieViewSet(viewsets.ModelViewSet):
    serializer_class = MovieSerializer
    filterset_fields = ['title', 'content','year']
    search_fields = ['title', 'content']
    filter_backends = [filters.OrderingFilter]
    ordering_fields = '__all__'
    ordering = ('year',)
    pagination_class = LargeResultsSetPagination
    authentication_classes = (TokenAuthentication, )
    permission_classes = (DjangoModelPermissions,)


    def get_queryset(self):
        #year = self.request.query_params.get('year', None)
        #title = self.request.query_params.get('title', None)
        #if year and title:
            #qs = Movie.objects.filter(year=year, title=title)
        #else:
            #qs = Movie.objects.all()
        qs = Movie.objects.all()
        return qs
   # def list(self, request, *args, **kwargs):
        #queryset = self.get_queryset()
        #title = self.request.query_params.get('title', None)
        #qs = Movie.objects.filter(title__contains=title)
        #qs = Movie.objects.filter(premiere__lte="2020-07-10")
        #serializer = MovieSerializer(qs, many=True)
        #return Response(serializer.data)
    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = MovieSerializer(instance)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        #if request.user.is_staff:
        movie = Movie.objects.create(title=request.data['title'],
                                         content=request.data['content'],
                                         after_prem=request.data['after_prem'],
                                     year=request.data['year']
                                     )
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)
        #else:
        #return HttpResponseNotAllowed('Not allowed')
    def update(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.title = request.data['title']
        movie.content = request.data['content']
        movie.after_prem = request.data['after_prem']
        movie.year = request.data['year']
        movie.save()
        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        movie = self.get_object()
        movie.delete()
        return Response('Deleted movie')

    @action(detail=True)
    def premiere(self, request, **kwargs):
        movie = self.get_object()
        movie.after_prem = True
        movie.save()

        serializer = MovieSerializer(movie, many=False)
        return Response(serializer.data)

    @action(detail=False, methods=['post'])
    def premiere_all(self, request, **kwargs):
        movies = Movie.objects.all()
        movies.update(after_prem=request.data['after_prem'])

        serializer = MovieSerializer(movies, many=True)
        return Response(serializer.data)

class RateViewSet(viewsets.ModelViewSet):
    queryset = Rate.objects.all()
    serializer_class = RateSerializer

class ActorViewSet(viewsets.ModelViewSet):
    queryset = Actor.objects.all()
    serializer_class = ActorSerializer
    @action(detail=True, methods=['post'])
    def connect(self, request, **kwargs):
        actor = self.get_object()
        movie = Movie.objects.get(id=request.data['movie'])
        actor.movies.add(movie)
        serializer = ActorSerializer(actor, many=False)
        return Response(serializer.data)


