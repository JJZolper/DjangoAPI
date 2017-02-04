import requests
import coreapi

from django.contrib.auth.models import User
from djangoapi.serializers import UserSerializer, FavoriteSerializer

from rest_framework import status
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from rest_framework_swagger.renderers import OpenAPIRenderer, SwaggerUIRenderer
from rest_framework.decorators import api_view, renderer_classes
from rest_framework import response

from favorites.models import Favorite, RedditPost

# Register with the API
@api_view(['POST'])
def register(request):
    serialized = UserSerializer(data=request.data)
    if serialized.is_valid():
        username = serialized.validated_data['username']
        password = serialized.validated_data['password']
        user = User.objects.create_user(username=username, password=password)
        user.save()
        token = Token.objects.get(user_id=user.id)
        return Response("Your access token is: " + token.key, status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

# Login with user credentials
@api_view(['POST'])
def login(request):
    try:
        user = User.objects.get(username__iexact=request.data['username'])
        if user.check_password(request.data['password']):
            token = Token.objects.get(user_id=user.id)
            return Response("Your access token is: " + token.key, status=status.HTTP_200_OK)
        return Response("Incorrect password", status=status.HTTP_400_BAD_REQUEST)
    except:
        return Response("You need to register", status=status.HTTP_400_BAD_REQUEST)

# Get results from reddit
@api_view(['GET'])
def reddit(request):
    access_token = request.query_params.get('access_token', None)
    token = Token.objects.get(key=access_token)
    # Check if the token is valid
    if token:
        result = []
        while True:
            try:
                r = requests.get('https://www.reddit.com/hot.json')
                data = r.json()
                if r.status_code == 200 and data["data"]:
                    break
                else:
                    continue
            except requests.exceptions.RequestException as e:
                return "Error: {}".format(e)
        # Data is a dictionary ingested from the json response
        datalen = len(data["data"])
        # List of dictionaries with the results
        for i in range(datalen):
            rinstance = {}
            rinstance["reddit_id"] = data["data"]["children"][i]["data"]["subreddit_id"]
            rinstance["permalink"] = data["data"]["children"][i]["data"]["permalink"]
            rinstance["url"] = data["data"]["children"][i]["data"]["url"]
            rinstance["author"] = data["data"]["children"][i]["data"]["author"]
            if not RedditPost.objects.filter(reddit_id=rinstance["reddit_id"]).exists():
                redditpost = RedditPost(reddit_id=rinstance["reddit_id"], permalink=rinstance["permalink"],
                                        url=rinstance["url"], author=rinstance["author"])
                redditpost.save()
            result.append(rinstance)
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)

# Create a new favorite
@api_view(['POST'])
def favorite(request):
    serialized = FavoriteSerializer(data=request.data)
    if serialized.is_valid():
        access_token = serialized.validated_data['access_token']
        reddit_id = serialized.validated_data['reddit_id']
        tag_name = serialized.validated_data['tag_name']
        token = Token.objects.get(key=access_token)
        user = User.objects.get(id=token.user_id)
        redditpost = RedditPost.objects.get(reddit_id=reddit_id)
        favorite = Favorite(user=user, access_token=access_token, reddit_id=reddit_id, permalink=redditpost.permalink,
                            url=redditpost.url, author=redditpost.url, tag_name=tag_name)
        favorite.save()
        return Response("Favorite saved!", status=status.HTTP_201_CREATED)
    else:
        return Response(serialized._errors, status=status.HTTP_400_BAD_REQUEST)

# Given an access token return the favorites
@api_view(['GET'])
def favorites(request):
    access_token = request.query_params.get('access_token', None)
    token = Token.objects.get(key=access_token)
    # Check if the token is valid
    if token:
        # Use token to get the user's favorites
        favorites = Favorite.objects.filter(access_token=access_token)
        result = []
        # List of dictionaries with the results
        for i in range(len(favorites)):
            rinstance = {}
            rinstance["reddit_id"] = favorites[i].reddit_id
            rinstance["permalink"] = favorites[i].permalink
            rinstance["url"] = favorites[i].url
            rinstance["author"] = favorites[i].author
            rinstance["tag_name"] = favorites[i].tag_name
            result.append(rinstance)
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)

# Given a tag name return the posts that are tagged as such
@api_view(['GET'])
def tag(request):
    access_token = request.query_params.get('access_token', None)
    token = Token.objects.get(key=access_token)
    tag_name = request.query_params.get('tag_name', None)
    # Check if the token is valid
    if token:
        # Use token to get the user's favorites
        favorites = Favorite.objects.filter(tag_name=tag_name).filter(access_token=access_token)
        result = []
        # List of dictionaries with the results
        for i in range(len(favorites)):
            rinstance = {}
            rinstance["reddit_id"] = favorites[i].reddit_id
            rinstance["permalink"] = favorites[i].permalink
            rinstance["url"] = favorites[i].url
            rinstance["author"] = favorites[i].author
            rinstance["tag_name"] = favorites[i].tag_name
            result.append(rinstance)
        return Response(result, status=status.HTTP_200_OK)
    else:
        return Response("Invalid token", status=status.HTTP_400_BAD_REQUEST)

# API Schema
schema = coreapi.Document(
    title='Django API',
    content={
        'register': coreapi.Link(
            url='/register/',
            action='post',
            fields=[
                coreapi.Field(
                    name='username',
                    required=True,
                    location='form',
                    description='The user name to register'
                ),
                coreapi.Field(
                    name='password',
                    required=True,
                    location='form',
                    description='The password to register'
                )
            ],
            description='Register'
        ),
        'login': coreapi.Link(
            url='/login/',
            action='post',
            fields=[
                coreapi.Field(
                    name='username',
                    required=True,
                    location='form',
                    description='The user name for login'
                ),
                coreapi.Field(
                    name='password',
                    required=True,
                    location='form',
                    description='The password for login'
                )
            ],
            description='Login'
        ),
        'reddit': coreapi.Link(
            url='/reddit/',
            action='get',
            fields=[
                coreapi.Field(
                    name='access_token',
                    required=True,
                    location='query',
                    description='Your access token'
                )
            ],
            description='Reddit'
        ),
        'favorite': coreapi.Link(
            url='/favorite/',
            action='post',
            fields=[
                coreapi.Field(
                    name='access_token',
                    required=True,
                    location='form',
                    description='Your access token'
                ),
                coreapi.Field(
                    name='reddit_id',
                    required=True,
                    location='form',
                    description='The id of your favorite reddit'
                ),
                coreapi.Field(
                    name='tag_name',
                    required=True,
                    location='form',
                    description='Tag your favorite reddit'
                )
            ],
            description='Favorite'
        ),
        'favorites': coreapi.Link(
            url='/favorites/',
            action='get',
            fields=[
                coreapi.Field(
                    name='access_token',
                    required=True,
                    location='query',
                    description='Your access token'
                )
            ],
            description='Favorites'
        ),
        'tag': coreapi.Link(
            url='/tag/',
            action='get',
            fields=[
                coreapi.Field(
                    name='access_token',
                    required=True,
                    location='query',
                    description='Your access token'
                ),
                coreapi.Field(
                    name='tag_name',
                    required=True,
                    location='query',
                    description='Your tag name'
                )
            ],
            description='Tags'
        )
    }
)

# API Schema
@api_view()
@renderer_classes([SwaggerUIRenderer, OpenAPIRenderer])
def schema_view(request):
    return response.Response(schema)


